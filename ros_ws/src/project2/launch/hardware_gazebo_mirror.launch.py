"""Show the real OpenManipulator-X joint motion in a passive Gazebo twin."""

import os
import xml.etree.ElementTree as ET
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.actions import SetEnvironmentVariable, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import xacro


JOINTS = (
    'joint1',
    'joint2',
    'joint3',
    'joint4',
    'gripper_left_joint',
    'gripper_right_joint',
)


def _mirror_robot_description():
    description_share = get_package_share_directory(
        'open_manipulator_description'
    )
    xacro_file = os.path.join(
        description_share,
        'urdf',
        'open_manipulator_x',
        'open_manipulator_x.urdf.xacro',
    )
    root = ET.fromstring(
        xacro.process_file(xacro_file, mappings={'use_sim': 'true'}).toxml()
    )

    for control in root.findall('ros2_control'):
        root.remove(control)

    for joint_name in ('joint1', 'joint2', 'joint3', 'joint4'):
        joint = root.find(f"./joint[@name='{joint_name}']")
        if joint is not None:
            limit = joint.find('limit')
            if limit is not None:
                limit.set('lower', '-3.141592653589793')
                limit.set('upper', '3.141592653589793')

    for gazebo in root.findall('gazebo'):
        for plugin in list(gazebo.findall('plugin')):
            gazebo.remove(plugin)

    plugins = ET.SubElement(root, 'gazebo')
    # Keep the same piece-attachment behavior as the Pick & Place Gazebo
    # launch.  The real robot remains the motion source; Gazebo only mirrors
    # its measured joint state and visualizes the held piece.
    for marker_id in range(6, 11):
        piece_name = f'robot_cube_{marker_id}'
        plugin = ET.SubElement(
            plugins,
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

    for joint in JOINTS:
        is_gripper = joint.startswith('gripper_')
        plugin = ET.SubElement(
            plugins,
            'plugin',
            {
                'filename': 'gz-sim-joint-position-controller-system',
                'name': 'gz::sim::systems::JointPositionController',
            },
        )
        ET.SubElement(plugin, 'joint_name').text = joint
        ET.SubElement(plugin, 'topic').text = (
            f'/digital_twin/{joint}/cmd_pos'
        )
        ET.SubElement(plugin, 'p_gain').text = (
            '80.0' if is_gripper else '1000.0'
        )
        ET.SubElement(plugin, 'i_gain').text = '0.0'
        ET.SubElement(plugin, 'd_gain').text = (
            '2.0' if is_gripper else '30.0'
        )
        ET.SubElement(plugin, 'cmd_max').text = (
            '10.0' if is_gripper else '1000.0'
        )
        ET.SubElement(plugin, 'cmd_min').text = (
            '-10.0' if is_gripper else '-1000.0'
        )

    ET.SubElement(
        plugins,
        'plugin',
        {
            'filename': 'gz-sim-joint-state-publisher-system',
            'name': 'gz::sim::systems::JointStatePublisher',
        },
    )
    return ET.tostring(root, encoding='unicode')


def generate_launch_description():
    project_share = get_package_share_directory('project2')
    description_share = get_package_share_directory(
        'open_manipulator_description'
    )
    world = LaunchConfiguration('world')
    robot_description = _mirror_robot_description()

    declared_arguments = [
        DeclareLaunchArgument(
            'world',
            default_value=PathJoinSubstitution(
                [FindPackageShare('project2'), 'world', 'empty_world.sdf']
            ),
            description=(
                'Pick-and-place Gazebo world used for the passive digital twin.'
            ),
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
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=[
            '-string',
            robot_description,
            '-name',
            'open_manipulator_x_mirror',
            '-allow_renaming',
            'false',
        ],
    )

    command_bridges = [
        f'/digital_twin/{joint}/cmd_pos@std_msgs/msg/Float64]gz.msgs.Double'
        for joint in JOINTS
    ]
    piece_bridges = [
        f'/robot_cube_{marker_id}/{command}@std_msgs/msg/Empty]gz.msgs.Empty'
        for marker_id in range(6, 11)
        for command in ('attach', 'detach')
    ]
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/world/tictactoe_world/model/open_manipulator_x_mirror/'
            'joint_state@sensor_msgs/msg/JointState[gz.msgs.Model',
        ] + command_bridges + piece_bridges + [
            '/world/tictactoe_world/set_pose@'
            'ros_gz_interfaces/srv/SetEntityPose'
        ],
        remappings=[
            (
                '/world/tictactoe_world/model/open_manipulator_x_mirror/'
                'joint_state',
                '/digital_twin/joint_states',
            )
        ],
        output='screen',
    )
    mirror = TimerAction(
        period=2.0,
        actions=[
            Node(
                package='project2',
                executable='digital_twin_robot',
                output='screen',
            )
        ],
    )

    return LaunchDescription(
        declared_arguments
        + [resource_path, gazebo, spawn_robot, bridge, mirror]
    )
