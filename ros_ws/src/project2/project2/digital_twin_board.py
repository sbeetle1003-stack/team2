import os
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from gazebo_msgs.srv import SpawnEntity

class TicTacToeTwinSync(Node):
    def __init__(self):
        super().__init__('tictactoe_twin_sync')
        
        # 1. 실제 로봇/게임 판정 모듈로부터 액션 토픽 구독
        # 메시지 예시: "robot,1,1" 또는 "human,0,2"
        self.subscription = self.create_subscription(
            String,
            '/tictactoe_action',
            self.action_callback,
            10
        )
        
        # 2. Gazebo 엔티티 생성(Spawn)을 위한 서비스 클라이언트 생성
        self.cli = self.create_client(SpawnEntity, '/spawn_entity')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Gazebo /spawn_entity service not available, waiting again...')
            
        self.get_logger().info("TicTacToe Twin Sync Node Started. Waiting for action messages...")

    def action_callback(self, msg):
        try:
            # 수신한 메시지 파싱 (예: "robot,1,1" -> player="robot", row=1, col=1)
            player, row_str, col_str = msg.data.split(',')
            row = int(row_str)
            col = int(col_str)
            
            self.get_logger().info(f"Received Action -> Player: {player}, Cell: ({row}, {col})")
            
            # 3. 틱택토 보드판 위 셀(Row, Col) 좌표를 Gazebo 3차원 공간(XYZ) 좌표로 매핑
            # (보드판의 크기 및 중심 위치에 맞게 offset 값을 수정해 주세요)
            base_x = 0.20  # 보드판 중심의 X 기준 좌표
            base_y = -0.0  # 보드판 중심의 Y 기준 좌표
            cell_size = 0.08 # 각 셀 사이의 간격 (단위: 미터)
            
            # 행, 열 인덱스를 3차원 물리 좌표로 변환 (예시 계산식)
            target_x = base_x + (col - 1) * cell_size
            target_y = base_y + (row - 1) * cell_size
            target_z = 0.02  # 보드판 표면 높이
            
            # 4. 플레이어 종류에 따라 생성할 SDF 모델 결정 (X 말 또는 O 말)
            # 패키지 경로 내 models 폴더에 위치한 SDF 파일 경로를 지정합니다.
            if player.lower() == 'robot':
                model_filename = 'x_mark.sdf'
                entity_name = f'x_mark_{row}_{col}'
            else:
                model_filename = 'o_mark.sdf'
                entity_name = f'o_mark_{row}_{col}'
                
            # SDF 파일 내용 로드
            model_xml = self.load_model_sdf(model_filename)
            if not model_xml:
                self.get_logger().error(f"Failed to load model file: {model_filename}")
                return
                
            # 5. Gazebo SpawnEntity 서비스 요청 객체 설정
            request = SpawnEntity.Request()
            request.name = entity_name
            request.xml = model_xml
            request.robot_namespace = ""
            request.initial_pose.position.x = target_x
            request.initial_pose.position.y = target_y
            request.initial_pose.position.z = target_z
            request.initial_pose.orientation.x = 0.0
            request.initial_pose.orientation.y = 0.0
            request.initial_pose.orientation.z = 0.0
            request.initial_pose.orientation.w = 1.0
            
            # 비동기 서비스 호출
            self.future = self.cli.call_async(request)
            self.future.add_done_callback(self.spawn_response_callback)
            
        except Exception as e:
            self.get_logger().error(f"Error processing action message: {e}")

    def load_model_sdf(self, filename):
        """패키지 경로 또는 지정된 디렉토리에서 SDF 파일 내용을 읽어오는 함수"""
        try:
            # 예시: 워크스페이스 내 프로젝트 모델 경로 설정 (본인 환경에 맞게 수정 가능)
            # 셰어 폴더나 지정된 경로의 절대/상대 경로 활용
            model_path = os.path.expanduser(f'/home/boyfriend51/temp/team2/project2/models/{filename}')
            with open(model_path, 'r') as f:
                return f.read()
        except Exception as e:
            self.get_logger().error(f"SDF file read error ({filename}): {e}")
            return None

    def spawn_response_callback(self, future):
        try:
            response = future.result()
            if response.success:
                self.get_logger().info("Successfully spawned game piece in Gazebo!")
            else:
                self.get_logger().warn(f"Failed to spawn entity: {response.status_message}")
        except Exception as e:
            self.get_logger().error(f"Spawn service call failed: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = TicTacToeTwinSync()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()



'''
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
from gazebo_msgs.srv import SpawnEntity, DeleteEntity

class DigitalTwinBoardSync(Node):
    def __init__(self):
        super().__init__('digital_twin_board_sync')
        
        # 실제 게임판 상태 토픽 구독
        self.subscription = self.create_subscription(
            Int32MultiArray,
            '/board_state',
            self.board_state_callback,
            10
        )
        
        # Gazebo 스폰 및 삭제 서비스 클라이언트 생성
        self.spawn_client = self.create_client(SpawnEntity, '/spawn_entity')
        self.delete_client = self.create_client(DeleteEntity, '/delete_entity')
        
        # 서비스 서버가 켜질 때까지 대기
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Spawn service not available, waiting again...')
        while not self.delete_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Delete service not available, waiting again...')
            
        self.get_logger().info("Digital Twin Board Sync Node Initialized.")
        
        # 이전 보드 상태를 기억하여 변경될 때만 업데이트 (9칸 기준)
        self.previous_board = [0] * 9

    def board_state_callback(self, msg):
        current_board = list(msg.data)
        
        if current_board == self.previous_board:
            return  # 상태 변화가 없으면 패스
            
        self.get_logger().info(f"Board State Changed: {current_board}")
        
        for i, state in enumerate(current_board):
            prev_state = self.previous_board[i]
            
            if state != prev_state:
                # 셀 번호(0~8)에 따른 3차원 좌표 매핑
                row = i // 3
                col = i % 3
                x = 0.2 + (col * 0.05)
                y = -0.05 + (row * 0.05)
                z = 0.01
                
                # 상태 변화에 따른 처리
                if state == 1: # HUMAN 말 (X 마크 스폰)
                    self.delete_marker(f"piece_{i}") # 기존에 혹시 남아있을 수 있는 말 제거 후 스폰
                    self.spawn_marker(f"piece_{i}", "x_mark.sdf", x, y, z)
                elif state == 2: # ROBOT 말 (O 마크 스폰)
                    self.delete_marker(f"piece_{i}")
                    self.spawn_marker(f"piece_{i}", "o_mark.sdf", x, y, z)
                elif state == 0: # 빈 칸이 된 경우 (말 제거)
                    self.delete_marker(f"piece_{i}")
                    
        self.previous_board = current_board

    def spawn_marker(self, name, model_filename, x, y, z):
        req = SpawnEntity.Request()
        req.name = name
        req.xml = self.load_model_sdf(model_filename)
        req.robot_namespace = ""
        req.initial_pose.position.x = float(x)
        req.initial_pose.position.y = float(y)
        req.initial_pose.position.z = float(z)
        
        future = self.spawn_client.call_async(req)
        self.get_logger().info(f"Spawn Request Sent: {name} at ({x}, {y}, {z})")
        print(future)

    def delete_marker(self, name):
        req = DeleteEntity.Request()
        req.name = name
        
        future = self.delete_client.call_async(req)
        self.get_logger().info(f"Delete Request Sent: {name}")
        print(future)


    def load_model_sdf(self, filename):
        # 간단한 SDF 파일 로더 예시 (실제 패키지 경로 혹은 환경변수 경로에 맞게 조정 필요)
        # 패키지 내 share 폴더나 GAZEBO_MODEL_PATH에 모델이 위치해야 합니다.
        try:
            with open(filename, 'r') as file:
                return file.read()
        except Exception as e:
            self.get_logger().error(f"Failed to load model file {filename}: {e}")
            # 예시로 기본 박스 형태 혹은 파일 읽기 처리 수행
            # 실제 환경에 맞춰 경로를 수정하여 사용하세요.
            return f"""
            <sdf version="1.6">
              <model name="marker">
                <link name="link">
                  <collision name="collision">
                    <geometry><box><size>0.03 0.03 0.01</size></box></geometry>
                  </collision>
                  <visual name="visual">
                    <geometry><box><size>0.03 0.03 0.01</size></box></geometry>
                  </visual>
                </link>
              </model>
            </sdf>
            """
        except Exception as e:
            self.get_logger().error(f"Failed to load model file: {e}")
            return ""

def main(args=None):
    rclpy.init(args=args)
    node = DigitalTwinBoardSync()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
'''


# 수정 전

'''
import rclpy
from rclpy.node import Node
# 예시용 커스텀 메시지 패키지 임포트 (프로젝트 구조에 맞게 수정 필요)
# from project2_msgs.msg import BoardState 
from std_msgs.msg import Int32MultiArray # 임시로 표준 배열 메시지 사용 시
from gazebo_msgs.srv import SpawnEntity, DeleteEntity

class DigitalTwinBoardSync(Node):
    def __init__(self):
        super().__init__('digital_twin_board_sync')
        
        # 실제 게임판 상태 토픽 구독
        self.subscription = self.create_subscription(
            Int32MultiArray,
            '/board_state',
            self.board_state_callback,
            10
        )
        
        self.get_logger().info("Digital Twin Board Sync Node Initialized.")
        
        # 이전 보드 상태를 기억하여 변경될 때만 업데이트
        self.previous_board = [0] * 9

    def board_state_callback(self, msg):
        current_board = list(msg.data)
        
        if current_board == self.previous_board:
            return # 상태 변화가 없으면 패스
            
        self.get_logger().info(f"Board State Changed: {current_board}")
        
        for i, state in enumerate(current_board):
            prev_state = self.previous_board[i]
            
            if state != prev_state:
                # 셀 번호(0~8)에 따른 3차원 좌표 매핑 (예시 계산)
                row = i // 3
                col = i % 3
                x = 0.2 + (col * 0.05) # 게임판 크기에 맞춘 상대 좌표
                y = -0.05 + (row * 0.05)
                z = 0.01
                
                if state == 1: # HUMAN 말 (예: 파란색 말 모델 스폰)
                    self.spawn_marker(f"human_piece_{i}", "x_mark.sdf", x, y, z)
                elif state == 2: # ROBOT 말 (예: 빨간색 말 모델 스폰)
                    self.spawn_marker(f"robot_piece_{i}", "o_mark.sdf", x, y, z)
                elif state == 0: # 빈 칸이 된 경우 (말 제거)
                    self.delete_marker(f"human_piece_{i}")
                    self.delete_marker(f"robot_piece_{i}")
                    
        self.previous_board = current_board

    def spawn_marker(self, name, model_filename, x, y, z):
        # Gazebo 서비스 클라이언트를 통한 모델 스폰 로직 구현 영역
        self.get_logger().info(f"Spawn Model {name} at ({x}, {y}, {z})")

    def delete_marker(self, name):
        # Gazebo 서비스 클라이언트를 통한 모델 삭제 로직 구현 영역
        self.get_logger().info(f"Delete Model {name}")

def main(args=None):
    rclpy.init(args=args)
    node = DigitalTwinBoardSync()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
'''