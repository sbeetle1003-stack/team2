import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # open_manipulator_ws의 install/share 폴더 경로를 지정합니다.
    gz_resource_paths = [
        '/home/boyfriend51/temp/team2/project2',
        '/home/boyfriend51/temp/gong/open_manipulator_ws/install/share'
    ]
    
    set_gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=':'.join(gz_resource_paths)
    )

    # 1. world 인자 선언 (team2 경로 기준 기본값 설정)
    default_world_path = '/home/boyfriend51/temp/team2/project2/world/empty_world.sdf'
    
    world_arg = DeclareLaunchArgument(
        'world',
        default_value=default_world_path,
        description='Path to the Gazebo SDF world file'
    )

    # 2. 선언된 world 인자 가져오기
    world_path = LaunchConfiguration('world')

    # 3. Gazebo 실행 런치
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
        set_gz_resource_path,  # 환경 변수 설정을 가장 먼저 실행
        world_arg,
        gazebo_launch,
        # ... 심판 노드나 다른 노드들 추가 ...
    ])