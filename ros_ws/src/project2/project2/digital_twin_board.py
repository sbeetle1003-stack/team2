import os
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int8MultiArray
from gazebo_msgs.srv import SpawnEntity
from ament_index_python.packages import get_package_share_directory

# 상태 정의
EMPTY = 0
HUMAN = 1   # BLUE (O 말)
ROBOT = 2   # RED (X 말)

class DigitalTwinBoardSync(Node):
    """
    /board_state 토픽(Int8MultiArray)을 구독하여 
    보드판에 말이 새로 놓였을 때 Gazebo 시뮬레이터에 가상 말을 동적으로 스폰한다.
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
        
        # 2. Gazebo 엔티티 생성 서비스 클라이언트 생성
        self.spawn_client = self.create_client(SpawnEntity, '/spawn_entity')
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Gazebo /spawn_entity 서비스가 준비되기를 기다리는 중...')
            
        # 이전 보드 상태 기억 (9칸 배열, 초기값 모두 EMPTY)
        self.previous_board = [EMPTY] * 9
        
        # 3x3 각 셀의 3차원 물리 좌표 설정 (보드판 위 중심 기준)
        self.cell_coordinates = {
            (0, 0): {'x': -0.06, 'y':  0.06},
            (0, 1): {'x':  0.00, 'y':  0.06},
            (0, 2): {'x':  0.06, 'y':  0.06},
            (1, 0): {'x': -0.06, 'y':  0.00},
            (1, 1): {'x':  0.00, 'y':  0.00},
            (1, 2): {'x':  0.06, 'y':  0.00},
            (2, 0): {'x': -0.06, 'y': -0.06},
            (2, 1): {'x':  0.00, 'y': -0.06},
            (2, 2): {'x':  0.06, 'y': -0.06},
        }

        self.get_logger().info("Digital Twin Board Sync Node Started. Subscribing to /board_state")

    def board_state_callback(self, msg):
        try:
            current_board = list(msg.data)
            
            # 9칸 상태 배열에 변화가 없으면 무시
            if current_board == self.previous_board:
                return
                
            self.get_logger().info(f"Board State Changed! Current: {current_board}")
            
            # 9칸을 순회하며 새로 채워진 셀 탐색
            for i in range(9):
                prev_val = self.previous_board[i]
                curr_val = current_board[i]
                
                # 빈 칸(EMPTY)이었다가 플레이어(HUMAN)나 로봇(ROBOT)의 말이 놓인 경우
                if prev_val == EMPTY and curr_val != EMPTY:
                    row = i // 3
                    col = i % 3
                    
                    player_type = "human" if curr_val == HUMAN else "robot"
                    self.spawn_virtual_piece(player_type, row, col, i)
                    
            # 현재 상태를 이전 상태로 갱신
            self.previous_board = current_board.copy()
            
        except Exception as e:
            self.get_logger().error(f"Error processing board state: {e}")

    def spawn_virtual_piece(self, player_type, row, col, cell_index):
        """Gazebo /spawn_entity 서비스를 호출하여 해당 좌표에 말을 스폰한다."""
        model_filename = "o_mark.sdf" if player_type == "human" else "x_mark.sdf"
        entity_name = f"{player_type}_piece_{cell_index}"
        
        # 모델 SDF 파일 내용 로드
        model_xml = self.load_model_sdf(model_filename)
        if not model_xml:
            return

        # 해당 셀의 3차원 물리 좌표 가져오기
        coords = self.cell_coordinates.get((row, col), {'x': 0.0, 'y': 0.0})
        pos_x = coords['x']
        pos_y = coords['y']
        pos_z = 0.02  # 보드판 표면 높이 (살짝 띄움)

        # Gazebo SpawnEntity 서비스 요청 객체 설정
        request = SpawnEntity.Request()
        request.name = entity_name
        request.xml = model_xml
        request.robot_namespace = ""
        request.initial_pose.position.x = pos_x
        request.initial_pose.position.y = pos_y
        request.initial_pose.position.z = pos_z
        request.initial_pose.orientation.w = 1.0

        # 비동기 서비스 호출
        future = self.spawn_client.call_async(request)
        future.add_done_callback(lambda ft: self.spawn_response_callback(ft, row, col, player_type))

    def load_model_sdf(self, filename):
        """ROS2 패키지 share 경로를 이용해 SDF 파일 내용을 UTF-8 인코딩으로 안전하게 읽어오는 함수"""
        try:
            package_share_dir = get_package_share_directory('project2')
            model_path = os.path.join(package_share_dir, 'models', filename)
            
            with open(model_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.get_logger().error(f"SDF file read error ({filename}): {e}")
            return None

    def spawn_response_callback(self, future, row, col, player_type):
        try:
            response = future.result()
            if response.success:
                self.get_logger().info(f"Successfully spawned {player_type} piece at cell ({row}, {col}) in Gazebo!")
            else:
                self.get_logger().warning(f"Failed to spawn entity: {response.status_message}")
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