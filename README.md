# team2
- README.md 공지
 - READMD.md 매일 11:40, 16:30 종합 후 작성
 - 주요 작업만 작성 예정, 추가 작성이 필요한 경우 README에 작성 후 팀장에게 얘기하면 확인하여 추가 작성할 계획.
 - 다른 좋은 의견이 있다면 언제든지 말씀해주세요.


> [!IMPORTANT]
> 현재 통합 작업 파일은 `feature/integration` 브랜치에 있습니다.
> 최신 통합 버전은 해당 브랜치를 확인해 주세요.
<br>

## 🔗 Project Resources

- 📄 Project Proposal: https://docs.google.com/document/d/1ujhqk1tdocbYJao8EDuLnZ8Bm_JgyH2_NuoS8eUxt3c/edit?usp=sharing
- 💻 Git Repository: https://github.com/sbeetle1003-stack/team2.git
- 📊 Presentation: 
- 🎥 Demo Video: https://youtu.be/fUDVXlAjMoQ?si=mpPt4mSILIlT5iIF
<br>


## 팀원 이메일
- 권신용: sbeetle1003@gmail.com
- 곽정미: utauloid.kk@gmail.com
- 이명연: coolhk03@gmail.com
- 주영찬:jyber9616@gmail.com
- 박미진:luckymijin0608@gmail.com
<br>

# 2026-08-10(1일차)
~~Occlusion-Aware Active Perception for Tomato Harvesting Using Deep Learning and a ROS2 Manipulator~~  
~~딥러닝과 ROS2 매니퓰레이터를 이용한 토마토 수확 대상의 가림 인지 기반 능동 시각 시스템~~ 

> **주제 변경:** 환경 구축 및 팀원 간 개발 환경 통일의 어려움으로 인해
> 2일차부터 틱택토 프로젝트로 변경함.

- 기존 계획서: https://docs.google.com/document/d/1Da4qCqeY5nMt9YkbcyU7bKz6OxcQ_4JnLeU_khmT6Bo/edit?usp=sharing
---
## 오전
- 권신용
  - 프로젝트 주제 구상 및 회의: ROS2 매니퓰레이터를 이용한 자동차 부품 자동 조립 시스템
- 곽정미
  - 프로젝트 주제 구상 및 회의: 딥러닝과 ROS2 매니퓰레이터를 이용한 토마토 수확 대상의 가림 인지 기반 능동 시각 시스템
  - 프로젝트 계획서 작성
- 이명연
  - 프로젝트 주제 구상 및 회의: ROS2 매니퓰레이터를 이용한 자동차 부품 자동 조립 시스템
- 주영찬
  - 프로젝트 주제 구상 및 회의: ROS2 매니퓰레이터를 이용한 자동차 부품 자동 조립 시스템
- 박미진
  - 프로젝트 주제 구상 및 회의: ROS2 매니퓰레이터와 Gazebo 디지털 트윈을 이용한 비전 기반 자율 틱택토 시스템


---
## 오후
- 권신용
  - 프로젝트 주제 구상 및 회의
- 곽정미
  - 프로젝트 주제 구상 및 회의
- 이명연
  - 프로젝트 주제 구상 및 회의
- 주영찬
  - 프로젝트 주제 구상 및 회의
- 박미진
  - 프로젝트 주제 구상 및 회의

- 금일 목표과제
  - 팀 구성과 역할 분담
  - 구글 슬라이드 팀 정보 수정
  - 주제 선택
  - 사후시험
  - team git Repositories 생성
  - 계획서 제출

<br>


# 2026-08-11(2일차)
### 프로젝트 주제 변경  
Vision-Based Autonomous Tic-Tac-Toe with a ROS2 Manipulator and Gazebo Digital Twin  
(ROS2 매니퓰레이터와 Gazebo 디지털 트윈을 이용한 비전 기반 자율 틱택토 시스템)  
- 프로젝트 계획서: https://docs.google.com/document/d/1ujhqk1tdocbYJao8EDuLnZ8Bm_JgyH2_NuoS8eUxt3c/edit?usp=sharing

---
## 오전
- 권신용
  - Ubuntu -> wsl 코드 최적화 방향성 모색
- 곽정미
  - 변경된 주제에 맞춰 계획서 작성, 시스템 구조 설계
  - 신규 ROS2 Workspace·Git Repository 및 tictactoe_vision 패키지 구축, OpenCV 카메라 및 ArUco Marker 인식 테스트
- 이명연
  - 좌표 추정 및 변환 개발
- 주영찬
  - 3by3 tic tac toe manipulator 개발 환경 구축
- 박미진
  - 시뮬레이션 환경 구축(Gazebo sys 설계)


---
## 오후
- 권신용
  - manipulator와 minimax algorithm 결합 후 시뮬 
- 곽정미
  - 틱택토 게임 에셋(Board, Mark, ArUco Marker) 제작하고 ROI 및 HSV 기반 보드·말 인식 테스트 진행
  - Vision 결과를 ROS2 Topic으로 연동하고, board_detector → referee → AI → Action Server까지 통합하여 Pick & Place dry-run 동작 확인
  - 팀원 작업 파일을 취합·정리하여 통합 Workspace를 구성하고 feature/integration 브랜치에 업로드
- 이명연
  - 좌표 추정 및 변환
- 주영찬
  - manipulator 개발(pick & place logic)
- 박미진
  - digital_twin 코드 작성

- 금일 목표과제





# 2026-08-12(3일차)

---
## 오전
- 권신용
  - Gazebo 보드 좌표계 수정, 매니퓰레이터 pick-and-place 실동작 연동, feature/integration와 minimax 로직 동기화
- 곽정미
  - 틱택토 로봇팔 Pick & Place 액션 서버 실행 및 실제 로봇 구동을 위한 ROS2 토픽 확인
  - 게임 로직–Referee–Pick & Place Controller 간 연동 코드 수정 및 테스트
- 이명연
  - 좌표 추정 및 변환
- 주영찬
  - digital twin 오류 수정 및 개발
- 박미진
  - 게임용 말 생성, world 파일 수정


---
## 오후
- 권신용
  - Game reset, over logic 개발 및 digital twin test, gripper 토크 측정 초기
- 곽정미
  - ArUco 기반 실제 보드 프레임과 TF 기반 셀 위치 계산 기능 구현·점검
  - OpenManipulator 이용해 기존 Referee, AI, Pick & Place 코드와 새 좌표 변환 기능의 연동 상태 확인, 동작 구조 정리
- 이명연
  - 좌표 추정 및 변환
- 주영찬
  - digital twin 개발 및 연동
- 박미진
  - digital_twin 파일 수정, xo_mark.sdf

- 금일 목표과제




# 2026-08-13(4일차)

---
## 오전
- 권신용
  - 
- 곽정미
  - 
- 이명연
  - 
- 주영찬
  - 
- 박미진
  - 


---
## 오후
- 권신용
  - 
- 곽정미
  - 
- 이명연
  - 
- 주영찬
  - 
- 박미진
  - 

- 금일 목표과제




## 2026-08-14(5일차)

---
#오전
- 권신용
  - 
- 곽정미
  - 
- 이명연
  - 
- 주영찬
  - 
- 박미진
  - 


---
#오후
- 권신용
  - 
- 곽정미
  - 
- 이명연
  - 
- 주영찬
  - 
- 박미진
  - 

- 금일 목표과제


