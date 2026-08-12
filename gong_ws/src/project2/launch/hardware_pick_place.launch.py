"""Run real OpenManipulator-X pick-and-place with a passive Gazebo twin."""

import glob
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.actions import OpaqueFunction
from launch.actions import TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def _start_hardware(context):
    """Resolve a single serial port before starting ros2_control."""
    requested_port = LaunchConfiguration('port_name').perform(context)
    mock_hardware = LaunchConfiguration('use_mock_hardware').perform(
        context
    ).lower() in ('1', 'true', 'yes', 'on')

    if requested_port == 'auto' and not mock_hardware:
        candidates = sorted(
            glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
        )
        if not candidates:
            raise RuntimeError(
                'OpenManipulator serial device not found. '
                'Attach U2D2 to WSL or pass port_name:=/dev/ttyUSB<N>.'
            )
        if len(candidates) > 1:
            raise RuntimeError(
                'Multiple serial devices found: '
                f'{", ".join(candidates)}. Pass port_name explicitly.'
            )
        requested_port = candidates[0]
    elif requested_port == 'auto':
        requested_port = '/dev/ttyUSB0'

    return [
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory(
                        'open_manipulator_bringup'
                    ),
                    'launch',
                    'open_manipulator_x.launch.py',
                )
            ),
            launch_arguments={
                'use_sim': 'false',
                'use_mock_hardware': LaunchConfiguration(
                    'use_mock_hardware'
                ),
                'port_name': requested_port,
                'init_position': LaunchConfiguration('init_position'),
                'start_rviz': 'false',
            }.items(),
        )
    ]


def generate_launch_description():
    dry_run = LaunchConfiguration('dry_run')
    start_gazebo = LaunchConfiguration('start_gazebo')
    start_rviz = LaunchConfiguration('start_rviz')

    arguments = [
        DeclareLaunchArgument(
            'port_name',
            default_value='auto',
            description='U2D2 device path, or auto for a single USB device.',
        ),
        DeclareLaunchArgument(
            'dry_run',
            default_value='false',
            description='True plans and prints stages without moving hardware.',
        ),
        DeclareLaunchArgument(
            'start_gazebo',
            default_value='true',
            description='Show a passive Gazebo robot following /joint_states.',
        ),
        DeclareLaunchArgument(
            'start_rviz',
            default_value='false',
            description='Start the standard MoveIt RViz window.',
        ),
        DeclareLaunchArgument(
            'init_position',
            default_value='false',
            description='Move hardware to its configured initial pose at startup.',
        ),
        DeclareLaunchArgument(
            'use_mock_hardware',
            default_value='false',
            description='Use ros2_control mock hardware for integration tests.',
        ),
    ]

    bringup = OpaqueFunction(function=_start_hardware)

    moveit = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory(
                    'open_manipulator_moveit_config'
                ),
                'launch',
                'open_manipulator_x_moveit.launch.py',
            )
        ),
        launch_arguments={
            'use_sim': 'false',
            'start_rviz': start_rviz,
            'publish_robot_description_semantic': 'true',
            'warehouse_sqlite_path': '/tmp/project2_hardware.sqlite',
        }.items(),
    )

    gazebo_twin = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    FindPackageShare('project2'),
                    'launch',
                    'hardware_gazebo_mirror.launch.py',
                ]
            )
        ),
        condition=IfCondition(start_gazebo),
    )

    config = PathJoinSubstitution(
        [FindPackageShare('project2'), 'config', 'hardware_manipulation.yaml']
    )
    controller = TimerAction(
        period=6.0,
        actions=[
            Node(
                package='project2',
                executable='pick_place_controller',
                output='screen',
                parameters=[
                    config,
                    {
                        'dry_run': ParameterValue(
                            dry_run,
                            value_type=bool,
                        )
                    },
                ],
            )
        ],
    )

    return LaunchDescription(
        arguments + [bringup, moveit, gazebo_twin, controller]
    )
