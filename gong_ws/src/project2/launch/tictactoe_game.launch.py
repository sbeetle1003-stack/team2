import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # 1. world 인자 선언 (기본값 설정 가능)
    default_world_path = '/home/boyfriend51/temp/gong/gong_ws/src/project2/world/empty_world.sdf'
    
    world_arg = DeclareLaunchArgument(
        'world',
        default_value=default_world_path,
        description='Path to the Gazebo SDF world file'
    )

    # 2. 선언된 world 인자 가져오기
    world_path = LaunchConfiguration('world')

    # 3. OpenManipulator Gazebo 런치 파일이나 ros_gz_sim 런치와 연동할 때 
    # world_path 변수를 Gazebo 실행 액션(또는 하위 런치)의 인자로 넘겨줍니다.
    # (예시: ros_gz_sim을 포함하는 구문이 있다면 world:=world_path 형태로 전달)
    
    # 예시 코드 구조 (작성하신 프로젝트 런치 형태에 맞게 대입하세요)
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            ])
        ]),
        launch_arguments={'gz_args': ['-r ', world_path]}.items()
    )

    return LaunchDescription([
        world_arg,
        gazebo_launch,
        # ... 심판 노드나 다른 노드들 추가 ...
    ])