"""Launch the tic-tac-toe world, OpenManipulator-X, MoveIt, and controller."""

import os
import xml.etree.ElementTree as ET
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    RegisterEventHandler,
    SetEnvironmentVariable,
    TimerAction,
)
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import xacro


def generate_launch_description():
    project_share = get_package_share_directory('project2')
    description_share = get_package_share_directory('open_manipulator_description')

    world = LaunchConfiguration('world')
    start_rviz = LaunchConfiguration('start_rviz')
    start_pick_place = LaunchConfiguration('start_pick_place')
    start_vision = LaunchConfiguration('start_vision')
    start_referee = LaunchConfiguration('start_referee')

    declared_arguments = [
        DeclareLaunchArgument(
            'world',
            default_value=PathJoinSubstitution(
                [FindPackageShare('project2'), 'world', 'empty_world.sdf']
            ),
            description='Absolute path to the tic-tac-toe Gazebo world.',
        ),
        DeclareLaunchArgument(
            'start_rviz',
            default_value='false',
            description='Start RViz with the OpenManipulator MoveIt configuration.',
        ),
        DeclareLaunchArgument(
            'start_pick_place',
            default_value='true',
            description='Start the PlacePiece action server.',
        ),
        DeclareLaunchArgument(
            'start_vision',
            default_value='false',
            description='Start the gripper-camera ArUco TF publisher.',
        ),
        DeclareLaunchArgument(
            'start_referee',
            default_value='false',
            description='Start the temporary camera referee/action client.',
        ),
    ]

    resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=[
            str(Path(project_share).parent),
            ':' + os.path.join(project_share, 'models'),
            ':' + str(Path(description_share).parent),
        ],
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py',
            )
        ),
        launch_arguments={'gz_args': ['-r ', world]}.items(),
    )

    xacro_file = os.path.join(
        description_share,
        'urdf',
        'open_manipulator_x',
        'open_manipulator_x.urdf.xacro',
    )
    robot_description = xacro.process_file(
        xacro_file,
        mappings={'use_sim': 'true'},
    ).toxml()

    # Gazebo Sim's physics engine does not support the gripper mimic
    # constraint. Add one controllable detachable joint per robot piece so
    # the simulation can explicitly attach on grasp and detach on release.
    robot_root = ET.fromstring(robot_description)
    gazebo_plugins = ET.SubElement(robot_root, 'gazebo')
    for marker_id in range(6, 11):
        piece_name = f'robot_cube_{marker_id}'
        plugin = ET.SubElement(
            gazebo_plugins,
            'plugin',
            {
                'filename': 'gz-sim-detachable-joint-system',
                'name': 'gz::sim::systems::DetachableJoint',
            },
        )
        ET.SubElement(plugin, 'parent_link').text = 'link5'
        ET.SubElement(plugin, 'child_model').text = piece_name
        ET.SubElement(plugin, 'child_link').text = 'cube_link'
        ET.SubElement(plugin, 'detach_topic').text = (
            f'/{piece_name}/detach'
        )
        ET.SubElement(plugin, 'attach_topic').text = (
            f'/{piece_name}/attach'
        )
        ET.SubElement(plugin, 'output_topic').text = (
            f'/{piece_name}/attachment_state'
        )
    robot_description = ET.tostring(robot_root, encoding='unicode')

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[
            {'robot_description': robot_description},
            {'use_sim_time': True},
        ],
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=[
            '-string',
            robot_description,
            '-x',
            '0.0',
            '-y',
            '0.0',
            '-z',
            '0.0',
            '-name',
            'open_manipulator_x',
            '-allow_renaming',
            'true',
        ],
    )

    joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            '--controller-manager',
            '/controller_manager',
        ],
        output='screen',
    )
    arm_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['arm_controller'],
        output='screen',
    )
    gripper_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['gripper_controller'],
        output='screen',
    )

    controller_startup = [
        RegisterEventHandler(
            OnProcessExit(
                target_action=spawn_robot,
                on_exit=[joint_state_broadcaster],
            )
        ),
        RegisterEventHandler(
            OnProcessExit(
                target_action=joint_state_broadcaster,
                on_exit=[arm_controller, gripper_controller],
            )
        ),
    ]

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/gripper_camera/camera_info@sensor_msgs/msg/CameraInfo'
            '[gz.msgs.CameraInfo',
            '/gripper_camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image',
        ] + [
            f'/robot_cube_{marker_id}/{command}@std_msgs/msg/Empty]'
            'gz.msgs.Empty'
            for marker_id in range(6, 11)
            for command in ('attach', 'detach')
        ] + [
            '/world/tictactoe_world/set_pose@'
            'ros_gz_interfaces/srv/SetEntityPose'
        ],
        output='screen',
    )

    moveit = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('open_manipulator_moveit_config'),
                'launch',
                'open_manipulator_x_moveit.launch.py',
            )
        ),
        launch_arguments={
            'use_sim': 'true',
            'start_rviz': start_rviz,
            'publish_robot_description_semantic': 'true',
            'warehouse_sqlite_path': '/tmp/project2_warehouse.sqlite',
        }.items(),
    )

    manipulation_config = PathJoinSubstitution(
        [FindPackageShare('project2'), 'config', 'manipulation.yaml']
    )
    pick_place_controller = TimerAction(
        period=5.0,
        actions=[
            Node(
                package='project2',
                executable='pick_place_controller',
                output='screen',
                parameters=[manipulation_config],
                condition=IfCondition(start_pick_place),
            )
        ],
    )

    vision = Node(
        package='project2',
        executable='multi_aruco_tf_sub',
        output='screen',
        condition=IfCondition(start_vision),
    )

    referee = TimerAction(
        period=6.0,
        actions=[
            Node(
                package='project2',
                executable='tic_tac_toe_referee',
                output='screen',
                parameters=[{'use_sim_time': True}],
                condition=IfCondition(start_referee),
            )
        ],
    )

    return LaunchDescription(
        declared_arguments
        + [
            resource_path,
            gazebo,
            robot_state_publisher,
            spawn_robot,
            bridge,
            moveit,
            pick_place_controller,
            vision,
            referee,
        ]
        + controller_startup
    )
