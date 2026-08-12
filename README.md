# 현재 통합 개발 브랜치(feature/integration)
## Branch Structure

                    GitHub team2
                         │
                    ros_ws/src
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
      A PC         B PC           C PC
    team2/ros_ws    team2/ros_ws    team2/ros_ws


현재 프로젝트는 기능별 브랜치에서 개발한 뒤 통합 브랜치에서 연결 및 테스트하는 방식으로 진행

- `main`
  - 팀 프로젝트의 기준 브랜치

- `feature/board-vision`
  - 틱택토 게임판 영상 인식 개발 브랜치
  - 카메라 영상에서 3×3 보드 상태를 인식
  - `/board_state` 토픽으로 보드 상태 publish

- `feature/integration`
  - **현재 통합 개발 브랜치**
  - 개별 기능을 가져와 실제 ROS2 노드 간 연결 및 통합 테스트 진행
  - 현재 다음 파이프라인까지 연결 및 dry-run 테스트 완료:

    `board_detector → tic_tac_toe_referee → tic_tac_toe_ai → PlacePiece Action → pick_place_controller`

  - 주요 통합 내용:
    - `board_detector`가 `/board_state` (`std_msgs/msg/Int8MultiArray`) publish
    - `tic_tac_toe_referee`가 보드 상태 subscribe
    - 사람의 새로운 수를 감지하면 `tic_tac_toe_ai`를 이용해 다음 수 결정
    - AI가 결정한 위치를 `cell_id`로 변환
    - `PlacePiece.action`을 통해 `pick_place_controller`에 배치 요청
    - `pick_place_controller`의 `dry_run` 모드에서 Pick & Place 전체 sequence 동작 확인

> 새로운 기능의 통합 및 테스트는 `feature/integration`에서 진행하며,
> 충분히 검증된 이후 `main` 브랜치에 병합

<br>

---
### Current Integration Status

| Component | Status |
|---|---|
| Board detection | ✅ Working |
| `/board_state` communication | ✅ Working |
| Referee integration | ✅ Working |
| Tic-Tac-Toe AI | ✅ Working |
| `PlacePiece` Action communication | ✅ Working |
| Pick & Place dry-run | ✅ Working |
| Gazebo integration | 🚧 In progress |
| Real manipulator execution | 🚧 Not tested yet |
| Game reset / undo handling | 🚧 TODO |
| Game-over logic verification | 🚧 TODO |
