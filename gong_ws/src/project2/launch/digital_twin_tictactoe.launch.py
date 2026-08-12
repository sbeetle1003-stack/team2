"""Run the real OpenManipulator-X and its Gazebo digital twin together."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    TimerAction,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    project_share = get_package_share_directory('project2')
    bringup_share = get_package_share_directory('open_manipulator_bringup')
    moveit_share = get_package_share_directory(
        'open_manipulator_moveit_config'
    )

    port_name = LaunchConfiguration('port_name')
    start_rviz = LaunchConfiguration('start_rviz')
    start_pick_place = LaunchConfiguration('start_pick_place')
    start_board_sync = LaunchConfiguration('start_board_sync')
    start_vision = LaunchConfiguration('start_vision')
    start_referee = LaunchConfiguration('start_referee')

    declared_arguments = [
        DeclareLaunchArgument(
            'port_name',
            default_value='/dev/ttyUSB0',
            description='U2D2/OpenCR serial port for the real robot.',
        ),
        DeclareLaunchArgument(
            'start_rviz',
            default_value='false',
            description='Start MoveIt RViz.',
        ),
        DeclareLaunchArgument(
            'start_pick_place',
            default_value='true',
            description='Start the PlacePiece action server.',
        ),
        DeclareLaunchArgument(
            'start_board_sync',
            default_value='true',
            description='Mirror integration /board_state messages into Gazebo.',
        ),
        DeclareLaunchArgument(
            'start_vision',
            default_value='false',
            description='Start the gripper-camera ArUco TF publisher.',
        ),
        DeclareLaunchArgument(
            'start_referee',
            default_value='false',
            description='Start the integration-branch board referee.',
        ),
    ]

    hardware = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                bringup_share,
                'launch',
                'open_manipulator_x.launch.py',
            )
        ),
        launch_arguments={
            'port_name': port_name,
            'use_sim': 'false',
            'init_position': 'false',
            'start_rviz': 'false',
        }.items(),
    )

    gazebo_twin = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                project_share,
                'launch',
                'hardware_gazebo_mirror.launch.py',
            )
        ),
        launch_arguments={
            'world': PathJoinSubstitution(
                [FindPackageShare('project2'), 'world', 'empty_world.sdf']
            )
        }.items(),
    )

    moveit = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                moveit_share,
                'launch',
                'open_manipulator_x_moveit.launch.py',
            )
        ),
        launch_arguments={
            'use_sim': 'false',
            'start_rviz': start_rviz,
            'publish_robot_description_semantic': 'true',
            'warehouse_sqlite_path': '/tmp/project2_hardware_warehouse.sqlite',
        }.items(),
    )

    manipulation_config = PathJoinSubstitution(
        [FindPackageShare('project2'), 'config', 'manipulation.yaml']
    )
    pick_place = TimerAction(
        period=8.0,
        actions=[
            Node(
                package='project2',
                executable='pick_place_controller',
                output='screen',
                parameters=[
                    manipulation_config,
                    {
                        'use_sim_time': False,
                        'simulate_piece_attachment': True,
                    },
                ],
                condition=IfCondition(start_pick_place),
            )
        ],
    )

    board_sync = TimerAction(
        period=3.0,
        actions=[
            Node(
                package='project2',
                executable='digital_twin_board',
                output='screen',
                parameters=[
                    {
                        'use_sim_time': False,
                        'board_state_topic': '/board_state',
                        'set_pose_service': (
                            '/world/tictactoe_world/set_pose'
                        ),
                        'board_piece_z': 0.025,
                    }
                ],
                condition=IfCondition(start_board_sync),
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
                parameters=[{'use_sim_time': False}],
                condition=IfCondition(start_referee),
            )
        ],
    )

    return LaunchDescription(
        declared_arguments
        + [
            hardware,
            gazebo_twin,
            moveit,
            pick_place,
            board_sync,
            vision,
            referee,
        ]
    )
