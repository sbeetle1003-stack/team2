"""Launch a namespaced Gazebo twin that mirrors the real OpenManipulator-X.

계획서 디지털 트윈 요구사항: 실제 로봇의 /joint_states를 Gazebo와 동기화.
이 launch는 그 Gazebo 쪽 절반만 담당한다 -- pick_place_controller/vision/
referee는 포함하지 않는다 (트윈은 독자적으로 판단하지 않고 실제 로봇을
그대로 따라 움직이기만 한다).

실행 순서 (터미널 2개, 순서 무관):
  1) ros2 launch open_manipulator_bringup open_manipulator_x.launch.py \
       port_name:=/dev/ttyUSB0 use_sim:=false
  2) ros2 launch project2 digital_twin.launch.py
"""
import os
import xml.etree.ElementTree as ET
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    IncludeLaunchDescription,
    RegisterEventHandler,
    SetEnvironmentVariable,
    TimerAction,
)
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

# arm_controller/gripper_controller가 이 네임스페이스 아래에서 뜨므로,
# digital_twin_bridge 노드의 twin_namespace 파라미터와 반드시 일치해야 한다.
TWIN_NAMESPACE = 'twin'


def generate_launch_description():
    project_share = get_package_share_directory('project2')
    description_share = get_package_share_directory('open_manipulator_description')

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
        launch_arguments={
            'gz_args': [
                '-r ',
                os.path.join(project_share, 'world', 'empty_world.sdf'),
            ]
        }.items(),
    )

    xacro_file = os.path.join(
        description_share, 'urdf', 'open_manipulator_x', 'open_manipulator_x.urdf.xacro'
    )
    robot_description = xacro.process_file(
        xacro_file, mappings={'use_sim': 'true'}
    ).toxml()

    # gz_ros2_control이 만드는 controller_manager를 'twin' 네임스페이스
    # 아래로 넣어서, 실제 하드웨어(네임스페이스 없음)의 /joint_states,
    # /arm_controller 등과 토픽/서비스 이름이 절대 겹치지 않게 한다.
    robot_root = ET.fromstring(robot_description)
    for gazebo_elem in robot_root.findall('gazebo'):
        for plugin_elem in gazebo_elem.findall('plugin'):
            if plugin_elem.get('name') == 'gz_ros2_control::GazeboSimROS2ControlPlugin':
                ros_elem = ET.SubElement(plugin_elem, 'ros')
                ET.SubElement(ros_elem, 'namespace').text = TWIN_NAMESPACE
    robot_description = ET.tostring(robot_root, encoding='unicode')

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace=TWIN_NAMESPACE,
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
            '-string', robot_description,
            '-x', '0.0', '-y', '0.0', '-z', '0.0',
            '-name', 'open_manipulator_x_twin',
            '-allow_renaming', 'true',
        ],
    )

    joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            '--controller-manager', f'/{TWIN_NAMESPACE}/controller_manager',
        ],
        output='screen',
    )
    arm_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'arm_controller',
            '--controller-manager', f'/{TWIN_NAMESPACE}/controller_manager',
        ],
        output='screen',
    )
    gripper_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'gripper_controller',
            '--controller-manager', f'/{TWIN_NAMESPACE}/controller_manager',
        ],
        output='screen',
    )

    controller_startup = [
        RegisterEventHandler(
            OnProcessExit(target_action=spawn_robot, on_exit=[joint_state_broadcaster])
        ),
        RegisterEventHandler(
            OnProcessExit(
                target_action=joint_state_broadcaster,
                on_exit=[arm_controller, gripper_controller],
            )
        ),
    ]

    bridge = TimerAction(
        period=6.0,
        actions=[
            Node(
                package='project2',
                executable='digital_twin_bridge',
                output='screen',
                parameters=[{'twin_namespace': TWIN_NAMESPACE}],
            )
        ],
    )

    return LaunchDescription(
        [
            resource_path,
            gazebo,
            robot_state_publisher,
            spawn_robot,
            bridge,
        ]
        + controller_startup
    )
