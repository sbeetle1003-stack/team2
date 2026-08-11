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