"""Launch the physical tic-tac-toe vision, motion, and referee nodes.

Start the physical OpenManipulator-X bringup separately before this launch.
The board detector opens /dev/video0 directly, so do not run camera_pub at the
same time.
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    dry_run = LaunchConfiguration('dry_run')
    pose_file = LaunchConfiguration('recorded_poses_file')
    start_board_detector = LaunchConfiguration('start_board_detector')
    start_pick_place = LaunchConfiguration('start_pick_place')
    start_referee = LaunchConfiguration('start_referee')

    declared_arguments = [
        DeclareLaunchArgument(
            'dry_run',
            default_value='false',
            description='Log recorded motions without moving the robot.',
        ),
        DeclareLaunchArgument(
            'recorded_poses_file',
            default_value=PathJoinSubstitution(
                [
                    FindPackageShare('project2'),
                    'config',
                    'recorded_poses.yaml',
                ]
            ),
            description='Recorded arm and gripper pose YAML file.',
        ),
        DeclareLaunchArgument(
            'start_board_detector',
            default_value='true',
            description='Start the OpenCV board detector.',
        ),
        DeclareLaunchArgument(
            'start_pick_place',
            default_value='true',
            description='Start the recorded-pose PlacePiece action server.',
        ),
        DeclareLaunchArgument(
            'start_referee',
            default_value='true',
            description='Start the tic-tac-toe referee and AI client.',
        ),
    ]

    pick_place_controller = Node(
        package='project2',
        executable='pick_place_controller',
        name='pick_place_controller',
        output='screen',
        emulate_tty=True,
        parameters=[
            {
                'use_sim_time': False,
                'dry_run': dry_run,
                'recorded_poses_file': pose_file,
            }
        ],
        condition=IfCondition(start_pick_place),
    )

    referee = Node(
        package='project2',
        executable='tic_tac_toe_referee',
        name='tic_tac_toe_referee',
        output='screen',
        emulate_tty=True,
        parameters=[{'use_sim_time': False}],
        condition=IfCondition(start_referee),
    )

    # Let the referee subscribe to /board_state before the detector publishes
    # its first stable state. The detector only republishes when state changes.
    board_detector = TimerAction(
        period=1.5,
        actions=[
            Node(
                package='tictactoe_vision',
                executable='board_detector',
                name='board_detector',
                output='screen',
                emulate_tty=True,
                parameters=[{'use_sim_time': False}],
                condition=IfCondition(start_board_detector),
            )
        ],
    )

    return LaunchDescription(
        declared_arguments
        + [
            pick_place_controller,
            referee,
            board_detector,
        ]
    )
