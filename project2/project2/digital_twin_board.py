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