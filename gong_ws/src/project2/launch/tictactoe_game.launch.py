#!/usr/bin/env python3
"""틱택토 Gazebo 환경: 보드 + 말 공급 + 카메라 + OpenManipulator-X.

로봇은 (0.3, -0.05, 0)에 스폰한다. 보드 표면은 로봇 base 기준 z=0.23m
(수평거리 20~300mm 구간)로, URDF 링크 길이 기반 기구학 계산으로
9칸 전부 도달 가능함을 사전 검증한 배치다.
"""

import os
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.actions import RegisterEventHandler
from launch.actions import SetEnvironmentVariable
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    open_manipulator_description_path = os.path.join(
        get_package_share_directory('open_manipulator_description')
    )
    open_manipulator_bringup_path = os.path.join(
        get_package_share_directory('open_manipulator_bringup')
    )

    # project2/ 디렉터리 (이 launch 파일의 상위의 상위). 아직 정식
    # ROS2 패키지가 아니라 get_package_share_directory를 쓸 수 없어
    # 파일 경로 기준으로 직접 계산한다.
    project2_path = Path(__file__).resolve().parent.parent

    gazebo_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=[
            os.path.join(open_manipulator_bringup_path, 'worlds'),
            ':' + str(Path(open_manipulator_description_path).parent.resolve()),
            ':' + str(project2_path / 'world'),
            ':' + str(project2_path / 'models'),
        ],
    )

    arguments = LaunchDescription([
        DeclareLaunchArgument(
            'world', default_value='tictactoe_world',
            description='Gz sim World (project2/world 안의 파일명, 확장자 제외)'
        ),
        DeclareLaunchArgument('use_sim_time', default_value='true'),
    ])

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch'),
            '/gz_sim.launch.py',
        ]),
        launch_arguments=[
            ('gz_args', [LaunchConfiguration('world'), '.sdf', ' -v 1', ' -r'])
        ],
    )

    xacro_file = os.path.join(
        open_manipulator_description_path,
        'urdf', 'open_manipulator_x', 'open_manipulator_x.urdf.xacro',
    )
    doc = xacro.process_file(xacro_file, mappings={'use_sim': 'true'})
    robot_desc = doc.toprettyxml(indent='  ')

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc,
                     'use_sim_time': LaunchConfiguration('use_sim_time')}],
    )

    # 보드 중심(0.3, 0) 바로 옆(y=-0.05)에 스폰 -> 9칸 전부 도달 범위 안
    gz_spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=[
            '-string', robot_desc,
            '-x', '0.3', '-y', '-0.05', '-z', '0.0',
            '-R', '0.0', '-P', '0.0', '-Y', '0.0',
            '-name', 'open_manipulator_x',
            '-allow_renaming', 'true',
        ],
    )

    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
        output='screen',
    )
    arm_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['arm_controller'],
        output='screen',
    )
    gripper_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['gripper_controller'],
        output='screen',
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/gripper_camera/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo',
            '/gripper_camera/image_raw@sensor_msgs/msg/Image@gz.msgs.Image',
            '/camera/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo',
            '/camera/image_raw@sensor_msgs/msg/Image@gz.msgs.Image',
        ],
        output='screen',
    )

    return LaunchDescription([
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=gz_spawn_entity,
                on_exit=[joint_state_broadcaster_spawner],
            )
        ),
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=joint_state_broadcaster_spawner,
                on_exit=[arm_controller_spawner, gripper_controller_spawner],
            )
        ),
        bridge,
        gazebo_resource_path,
        arguments,
        gazebo,
        node_robot_state_publisher,
        gz_spawn_entity,
    ])
