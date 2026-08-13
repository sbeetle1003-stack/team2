import os
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int8MultiArray
from ros_gz_interfaces.srv import SpawnEntity
from ament_index_python.packages import get_package_share_directory

# 상태 정의
EMPTY = 0
HUMAN = 1   # BLUE (O 말)
ROBOT = 2   # RED (X 말)
UNKNOWN = 3

class DigitalTwinBoardSync(Node):
    """
    /board_state 토픽(Int8MultiArray)을 구독하여 
    보드판에 말이 새로 놓였을 때 Gazebo Harmonic 시뮬레이터에 가상 말을 동적으로 스폰한다.
    """
    def __init__(self):
        super().__init__('digital_twin_board_sync')
        
        # 1. 비전 인식 노드로부터 전체 보드 상태 토픽 구독
        self.subscription = self.create_subscription(
            Int8MultiArray,
            '/board_state',
            self.board_state_callback,
            10
        )
        
        # 2. Gazebo Harmonic 서비스 클라이언트 연결
        self.spawn_service_name = '/world/tictactoe_world/create'
        self.spawn_client = self.create_client(
            SpawnEntity,
            self.spawn_service_name
        )

        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(
                f'Gazebo Harmonic {self.spawn_service_name} 서비스가 준비되기를 기다리는 중...'
            )

        # 이전 보드 상태 기억 (9칸 배열, 초기값 모두 EMPTY)
        self.previous_board = [EMPTY] * 9
        
        # 각 플레이어별 스폰 카운트 (모델 이름 중복 방지용)
        self.human_piece_count = 0
        self.robot_piece_count = 0
        
        # 3x3 각 셀의 3차원 물리 좌표 설정 (보드판 위 중심 기준 Z 높이 포함)
        self.cell_coordinates = {
            (0, 0): {'x': -0.06, 'y':  0.06, 'z': 0.02},
            (0, 1): {'x':  0.00, 'y':  0.06, 'z': 0.02},
            (0, 2): {'x':  0.06, 'y':  0.06, 'z': 0.02},
            (1, 0): {'x': -0.06, 'y':  0.00, 'z': 0.02},
            (1, 1): {'x':  0.00, 'y':  0.00, 'z': 0.02},
            (1, 2): {'x':  0.06, 'y':  0.00, 'z': 0.02},
            (2, 0): {'x': -0.06, 'y': -0.06, 'z': 0.02},
            (2, 1): {'x':  0.00, 'y': -0.06, 'z': 0.02},
            (2, 2): {'x':  0.06, 'y': -0.06, 'z': 0.02},
        }

        self.get_logger().info("Digital Twin Board Sync Node Started for Gazebo Harmonic. Subscribing to /board_state")

    def board_state_callback(self, msg):
        try:
            # 1. 수신된 데이터를 확실한 파이썬 정수 리스트로 변환
            current_board = [int(val) for val in msg.data]

            # BoardState는 반드시 9개여야 함
            if len(current_board) != 9:
                self.get_logger().warning(
                    f"잘못된 BoardState 길이: {len(current_board)}"
                )
                return

            # 허용되는 상태값인지 검사
            valid_states = {EMPTY, HUMAN, ROBOT, UNKNOWN}
            if any(value not in valid_states for value in current_board):
                self.get_logger().warning(
                    f"잘못된 BoardState 값: {current_board}"
                )
                return

            # UNKNOWN이 있으면 이전 상태를 갱신하지 않고 대기
            if UNKNOWN in current_board:
                return

            # 이전 보드와 같으면 처리하지 않음
            if current_board == self.previous_board:
                return

            self.get_logger().info(
                f"Board State Changed! Current: {current_board}"
            )

            # 9개 셀의 변경 상태 확인
            for i in range(9):
                prev_val = self.previous_board[i]
                curr_val = current_board[i]

                # EMPTY에서 HUMAN 또는 ROBOT으로 변한 경우 (새로운 말 놓임)
                if prev_val == EMPTY and curr_val in (HUMAN, ROBOT):
                    row = i // 3
                    col = i % 3
                    player_type = "human" if curr_val == HUMAN else "robot"

                    self.spawn_virtual_piece(player_type, row, col)

                # 이미 놓인 말이 사라지거나 다른 말로 바뀐 경우 (경고 로그)
                elif prev_val in (HUMAN, ROBOT) and curr_val != prev_val:
                    self.get_logger().warning(
                        f"허용되지 않은 상태 변화: cell={i}, {prev_val} -> {curr_val}"
                    )

            # 정상적으로 처리한 경우에만 이전 상태 갱신
            self.previous_board = current_board.copy()

        except Exception as e:
            self.get_logger().error(
                f"Error processing board state: {e}"
            )

    def load_model_sdf(self, filename):
        """ROS2 패키지 share 경로를 이용해 SDF 파일 내용을 UTF-8로 안전하게 읽어오는 함수"""
        try:
            package_share_dir = get_package_share_directory('project2')
            model_path = os.path.join(package_share_dir, 'models', filename)
            
            with open(model_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.get_logger().error(f"SDF file read error ({filename}): {e}")
            return None

    def spawn_virtual_piece(self, player_type, row, col):
        """
        Gazebo Harmonic /world/<world_name>/create 서비스를 호출하여 
        o_mark.sdf 또는 x_mark.sdf를 지정된 셀 좌표에 동적으로 스폰한다.
        """
        if not self.spawn_client.service_is_ready():
            self.get_logger().warning(
                "Gazebo Harmonic spawn 서비스가 준비되지 않았습니다."
            )
            return

        # 1. 플레이어 종류에 따른 SDF 파일 선택 및 모델 이름 결정
        if player_type == "human":
            filename = "o_mark.sdf"
            entity_name = f"human_piece_{self.human_piece_count}_{row}_{col}"
            self.human_piece_count += 1
        elif player_type == "robot":
            filename = "x_mark.sdf"
            entity_name = f"robot_piece_{self.robot_piece_count}_{row}_{col}"
            self.robot_piece_count += 1
        else:
            return

        # 2. SDF 파일 내용(XML 문자열) 로드
        model_xml = self.load_model_sdf(filename)
        if not model_xml:
            return

        # 3. 셀 좌표 확인
        coords = self.cell_coordinates.get((row, col))
        if coords is None:
            self.get_logger().error(f"잘못된 셀 좌표: row={row}, col={col}")
            return

        # 4. ros_gz_interfaces/srv/SpawnEntity 요청 작성
        request = SpawnEntity.Request()
        request.entity_factory.name = entity_name
        request.entity_factory.sdf = model_xml
        
        # 스폰 위치 및 자세 설정
        request.entity_factory.pose.position.x = float(coords["x"])
        request.entity_factory.pose.position.y = float(coords["y"])
        request.entity_factory.pose.position.z = float(coords["z"])
        
        request.entity_factory.pose.orientation.x = 0.0
        request.entity_factory.pose.orientation.y = 0.0
        request.entity_factory.pose.orientation.z = 0.0
        request.entity_factory.pose.orientation.w = 1.0

        self.get_logger().info(
            f"스폰 요청 [Harmonic] -> Entity: {entity_name}, Cell: ({row}, {col}), "
            f"x={coords['x']}, y={coords['y']}, z={coords['z']}"
        )

        # 5. 비동기 서비스 호출 및 콜백 등록
        future = self.spawn_client.call_async(request)
        future.add_done_callback(
            lambda completed_future: self.spawn_response_callback(
                completed_future, entity_name, row, col
            )
        )

    def spawn_response_callback(self, future, entity_name, row, col):
        """SpawnEntity 서비스 호출 결과를 처리한다."""
        try:
            response = future.result()
            if response is not None and response.success:
                self.get_logger().info(
                    f"Successfully spawned {entity_name} at cell ({row}, {col}) in Gazebo Harmonic!"
                )
            else:
                self.get_logger().warning(
                    f"Failed to spawn entity {entity_name} in Gazebo Harmonic."
                )
        except Exception as e:
            self.get_logger().error(f"Spawn service call failed: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = DigitalTwinBoardSync()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()