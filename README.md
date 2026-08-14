# Vision-Based Tic-Tac-Toe Robot

OpenManipulator-X와 카메라를 이용해 사람과 로봇이 실제 3×3 틱택토를 진행하는 ROS2 프로젝트입니다.

카메라가 게임판을 인식하면 심판 노드가 사람의 수를 검증하고, Minimax AI가 로봇의 다음 수를 결정합니다. 로봇은 미리 기록한 관절 자세를 재생해 말을 집어 선택한 셀에 놓습니다.


## 시스템 흐름

```text
board_detector
  └─ /board_state (Int8MultiArray)
        ↓
tic_tac_toe_referee
  ├─ 사람 수 및 승패 검증
  ├─ tic_tac_toe_ai (Minimax) 호출
  └─ /place_piece (PlacePiece Action)
        ↓
pick_place_controller
  ├─ /arm_controller/follow_joint_trajectory
  └─ /gripper_controller/gripper_cmd
```

## 주요 패키지와 노드

| 패키지/노드 | 역할 |
|---|---|
| `tictactoe_vision/board_detector` | `/dev/video0`을 직접 열어 ArUco 마커로 보드를 보정하고 HSV 색상으로 9개 셀을 판정한 뒤 `/board_state`를 발행합니다. |
| `project2/tic_tac_toe_referee` | 사람과 로봇의 턴, 유효한 보드 변화, 승리 및 무승부를 관리합니다. |
| `project2/tic_tac_toe_ai` | Minimax 알고리즘으로 로봇의 최적 `cell_id`를 선택합니다. 심판 노드 내부에서 사용됩니다. |
| `project2/pick_place_controller` | `recorded_poses.yaml`의 공급 위치와 셀별 관절 자세를 읽어 `/place_piece` 액션을 수행합니다. |
| `project2_interfaces/PlacePiece.action` | 0~8의 `cell_id`와 동작 결과·진행 상태를 전달하는 사용자 정의 액션입니다. |
| `tictactoe_game.launch.py` | `board_detector`, `tic_tac_toe_referee`, `pick_place_controller`를 함께 실행합니다. |

보드 인코딩은 다음과 같습니다.

| 값 | 상태 |
|---:|---|
| `0` | EMPTY |
| `1` | HUMAN (파란색) |
| `2` | ROBOT (빨간색) |
| `3` | UNKNOWN |

`cell_id`는 사람 시점에서 행 우선 순서입니다.

```text
0 1 2
3 4 5
6 7 8
```

## 실행 환경

- Ubuntu 24.04
- ROS2 Jazzy
- OpenManipulator-X 및 전용 controller/bringup 패키지
- USB 카메라 (`/dev/video0`)
- OpenCV 및 ArUco 모듈

## 처음 한 번 빌드하기

```bash
cd ~/tictactoe_robot/ros_ws

source /opt/ros/jazzy/setup.bash
source ~/2026_ROS_manipulator/open_manipulator_ws/install/setup.bash

colcon build \
  --packages-select project2_interfaces tictactoe_vision project2 \
  --symlink-install

source ~/tictactoe_robot/ros_ws/install/local_setup.bash
```

환경이 올바른지 확인합니다.

```bash
ros2 pkg prefix project2
ros2 pkg prefix tictactoe_vision
```

첫 번째 출력은 반드시 다음처럼 `ros_ws/install`을 가리켜야 합니다.

```text
/home/<USER>/tictactoe_robot/ros_ws/install/project2
```

`~/tictactoe_robot/install/project2`가 나온다면 오래된 workspace가 먼저 source된 상태입니다. 새 터미널을 열고 위 source 명령을 순서대로 다시 실행하세요.

## 실물 게임 실행

### 터미널 1: OpenManipulator-X bringup

```bash
source /opt/ros/jazzy/setup.bash
source ~/2026_ROS_manipulator/open_manipulator_ws/install/setup.bash

ros2 launch open_manipulator_bringup open_manipulator_x.launch.py
```

로봇 연결과 controller가 정상적으로 준비된 후 다음 터미널을 실행합니다.

### 터미널 2: 틱택토 통합 launch

```bash
source /opt/ros/jazzy/setup.bash
source ~/2026_ROS_manipulator/open_manipulator_ws/install/setup.bash
source ~/tictactoe_robot/ros_ws/install/local_setup.bash

ros2 launch project2 tictactoe_game.launch.py
```

정상 실행 시 다음 로그를 확인할 수 있습니다.

```text
Recorded poses: .../project2/config/recorded_poses.yaml
PlacePiece action server 준비 완료 (EXECUTE)
틱택토 심판 노드 준비 완료 (state=WAIT_FOR_HUMAN)
Board detector started. Publishing: /board_state
```

카메라가 최초로 안정된 보드를 인식하면 이를 초기 상태로 등록합니다. 이후 사람이 파란 말을 한 칸에 놓으면 심판이 변화를 감지하고, AI가 선택한 셀에 로봇이 빨간 말을 배치합니다.

## 안전한 dry-run

실물 로봇을 움직이지 않고 보드 인식, 심판, AI 및 액션 흐름만 확인하려면 다음과 같이 실행합니다.

```bash
ros2 launch project2 tictactoe_game.launch.py dry_run:=true
```

`dry_run:=true`에서는 관절 목표만 로그로 출력하고 실제 팔과 그리퍼를 구동하지 않습니다.

## 수동 액션 테스트

심판 없이 특정 셀 동작만 확인하려면 통합 launch가 실행된 상태에서 다음 명령을 사용합니다.

```bash
ros2 action send_goal \
  /place_piece \
  project2_interfaces/action/PlacePiece \
  "{cell_id: 4}" \
  --feedback
```

실물 테스트 전에는 먼저 `dry_run:=true`로 목표 셀과 동작 순서를 확인하세요.

## Launch 인자

| 인자 | 기본값 | 설명 |
|---|---:|---|
| `dry_run` | `false` | `true`이면 관절 목표만 출력하고 로봇은 움직이지 않습니다. |
| `recorded_poses_file` | 패키지의 `config/recorded_poses.yaml` | 기록 자세 YAML 경로입니다. |
| `start_board_detector` | `true` | 보드 인식 노드 실행 여부입니다. |
| `start_pick_place` | `true` | PlacePiece 액션 서버 실행 여부입니다. |
| `start_referee` | `true` | 심판 및 AI 클라이언트 실행 여부입니다. |

예를 들어 비전 노드를 제외하고 실행하려면 다음과 같이 지정합니다.

```bash
ros2 launch project2 tictactoe_game.launch.py start_board_detector:=false
```

## 기록 자세 조정

실물 배치 자세와 동작 시간은 다음 파일에서 관리합니다.

```text
ros_ws/src/project2/config/recorded_poses.yaml
```

- `gripper.open`, `gripper.grasp`: 그리퍼 열림·파지 위치
- `poses.board_view`: 카메라가 전체 보드를 보는 대기 자세
- `poses.supply_grasp`: 말 공급 위치의 파지 자세
- `poses.supply_lift`: 말을 집은 뒤의 안전 상승 자세
- `poses.cell_drop.cell_0`~`cell_8`: 각 셀의 드롭 자세
- `motion.*_seconds`: 각 이동 구간의 실행 시간

자세나 시간을 변경한 뒤 패키지를 다시 빌드하고 환경을 source합니다.

```bash
cd ~/tictactoe_robot/ros_ws
colcon build --packages-select project2 --symlink-install
source install/local_setup.bash
```

> 기록 자세는 현재 실물 게임판과 로봇 배치를 기준으로 측정한 값입니다. 로봇 또는 보드 위치를 바꾸면 충돌할 수 있으므로 반드시 dry-run과 저속 시험을 먼저 수행하세요.

## 주의 사항 및 문제 해결

### 카메라를 열 수 없음 (`/dev/video0 is busy`)

`board_detector`가 카메라를 직접 사용하므로 `camera_pub` 또는 다른 카메라 프로그램을 동시에 실행하지 마세요.

```bash
fuser /dev/video0
```

위 명령으로 카메라를 점유한 프로세스를 확인할 수 있습니다.

### `recorded_poses.yaml`이 없다는 오류

```bash
ros2 pkg prefix project2
ls -l "$(ros2 pkg prefix project2)/share/project2/config/recorded_poses.yaml"
```

경로가 `~/tictactoe_robot/ros_ws/install/project2`를 가리키는지 확인한 뒤 `project2`를 다시 빌드하세요.

### Qt가 display에 연결되지 않음

`board_detector`는 OpenCV 창을 표시하므로 GUI 터미널에서 실행해야 합니다. `env -i`처럼 `DISPLAY` 또는 Wayland 환경변수를 제거한 셸에서는 실행하지 마세요.

### 노드별 단독 실행

통합 launch 대신 다음 명령으로 개별 디버깅할 수 있습니다.

```bash
ros2 run tictactoe_vision board_detector
ros2 run project2 pick_place_controller --ros-args -p dry_run:=true
ros2 run project2 tic_tac_toe_referee
```

## 현재 구현 상태

| 기능 | 상태 |
|---|---|
| ArUco 기반 보드 보정 및 HSV 말 인식 | ✅ 완료 |
| `/board_state` 통신 | ✅ 완료 |
| 사람 수 검증 및 턴·승패 관리 | ✅ 완료 |
| Minimax AI | ✅ 완료 |
| `PlacePiece` 액션 연동 | ✅ 완료 |
| 기록 관절 자세 기반 Pick & Place | ✅ 완료 |
| 실물 OpenManipulator-X 게임 완료 | ✅ 확인 |
| 통합 launch 실행 | ✅ 완료 |
| Gazebo Digital Twin | ⏸️ 최종 범위에서 제외 |
