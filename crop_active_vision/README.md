# Crop Active Vision

## Project

**Occlusion-Aware Active Perception for Tomato Harvesting Using Deep
Learning and a ROS2 Manipulator**

딥러닝과 ROS2 매니퓰레이터를 이용한 토마토 수확 대상의 가림 인지 기반
능동 시각 시스템

Gazebo 토마토 재배 환경에서 OpenManipulator-X 말단 카메라로 작물을
관찰하고, 과실의 숙도 및 가림 상태를 판단한 뒤 필요한 경우
매니퓰레이터의 관찰 시점을 변경하여 수확 대상을 재인식하는 시스템을
구현하는 프로젝트입니다.

## Development Environment

-   Ubuntu 24.04
-   ROS 2 Jazzy
-   Gazebo Harmonic
-   OpenManipulator-X
-   MoveIt2
-   ros2_control
-   ros_gz
-   AOC Tomato Farm 기반 Gazebo 모델

## Current Status

현재 구현된 기능:

-   AOC Tomato Farm 기반 온실 환경 로딩
-   Gazebo용 토마토 모델 및 월드 구성
-   토마토 모델 크기 조정
-   OpenManipulator-X Gazebo 연동
-   ROS2 controller 연동
-   Gripper-mounted RGB camera 연동
-   `/gripper_camera/image_raw` 영상 송출
-   Teleop을 이용한 매니퓰레이터 및 카메라 시점 제어
-   매니퓰레이터의 초기 관찰 위치 설정

추후 구현 예정:

-   YOLO 기반 토마토 과실 검출
-   Segmentation 기반 과실 영역 추정
-   숙도 및 Occlusion 판단
-   Active Perception
-   MoveIt2 기반 자동 관찰 시점 변경
-   Depth / TF2 기반 과실 3D 위치 추정
-   수확 대상 및 접근 위치 결정

## Repository

현재 프로젝트는 `feature/active-vision` 브랜치에서 개발 중입니다.

### 처음 다운로드하는 경우

``` bash
cd ~

git clone https://github.com/sbeetle1003-stack/team2.git
cd team2
git switch feature/active-vision
```

프로젝트 디렉터리:

``` text
team2/
└── crop_active_vision/
    ├── config/
    ├── launch/
    ├── models/
    ├── scripts/
    ├── worlds/
    └── README.md
```

### 이미 Repository를 받은 경우

``` bash
cd ~/team2
git switch feature/active-vision
git pull
```

작업 중인 파일이 있다면 먼저 상태를 확인합니다.

``` bash
git status
```

## Requirements

본 Repository에는 OpenManipulator-X 패키지 자체가 포함되어 있지
않습니다.

ROS2 환경에서 다음 패키지가 확인되어야 합니다.

``` bash
ros2 pkg list | grep open_manipulator
```

또한 Gazebo와 ROS2 연동을 위해 `ros_gz` 관련 패키지가 필요합니다.

``` bash
ros2 pkg list | grep ros_gz
```

## Gazebo Assets

프로젝트에서 사용하는 생성 완료된 Gazebo 모델과 월드는 Repository에
포함되어 있습니다.

``` text
crop_active_vision/
├── models/
│   ├── tomato_*
│   ├── flowerpot_*
│   ├── lamp_*
│   ├── soilbed_*
│   ├── metal_*
│   └── structure_0
└── worlds/
    └── tomato_farm_2mx3m_gazebo_sim.sdf
```

따라서 일반적인 실행 과정에서는 AOC Tomato Farm의 Jupyter generator와
Blender를 다시 실행할 필요가 없습니다.

## Running

먼저 ROS2와 OpenManipulator workspace를 source합니다.

``` bash
source /opt/ros/jazzy/setup.bash
source <OPEN_MANIPULATOR_WORKSPACE>/install/setup.bash
```

> 현재 launch 파일의 경로 독립화 작업이 진행 중이므로, 팀원 PC의
> OpenManipulator workspace 구성에 따라 경로 설정이 필요할 수 있습니다.

## Check Controllers

시뮬레이션 실행 후 controller 상태를 확인합니다.

``` bash
ros2 control list_controllers
```

정상적인 경우 다음 controller들이 `active` 상태여야 합니다.

``` text
arm_controller          active
gripper_controller      active
joint_state_broadcaster active
```

## Check Gripper Camera

카메라 topic을 확인합니다.

``` bash
ros2 topic list | grep -E "camera|image"
```

정상적인 경우:

``` text
/gripper_camera/camera_info
/gripper_camera/image_raw
```

영상은 다음 명령으로 확인할 수 있습니다.

``` bash
rqt_image_view
```

`/gripper_camera/image_raw` topic을 선택합니다.

## Manual Manipulator Test

현재 매니퓰레이터의 수동 동작 테스트에는 OpenManipulator teleop을 사용할
수 있습니다.

``` bash
ros2 run open_manipulator_teleop open_manipulator_x_teleop
```

매니퓰레이터를 움직이면 말단에 장착된 gripper camera의 시야도 함께
이동합니다.

## Project Workflow

``` text
Gazebo Tomato Farm
        ↓
OpenManipulator-X + Eye-in-Hand Camera
        ↓
Tomato Detection / Segmentation
        ↓
Ripeness + Occlusion Estimation
        ↓
Active Perception Decision
        ↓
Manipulator Viewpoint Change
        ↓
Re-observation
        ↓
3D Target Localization
        ↓
Harvest Target / Approach Pose Selection
```

## Notes

-   현재 개발 브랜치는 `feature/active-vision`입니다.
-   프로젝트가 `main` 브랜치에 병합되기 전까지는 해당 브랜치를
    사용하세요.
-   생성 완료된 Gazebo world/model이 포함되어 있으므로 월드 생성 과정을
    반복할 필요가 없습니다.
-   OpenManipulator-X 관련 ROS2 패키지는 별도로 준비되어 있어야 합니다.
-   `build/`, `install/`, `log/`, 가상환경 디렉터리는 Git에 포함하지
    않습니다.
