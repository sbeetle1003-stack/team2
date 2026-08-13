import os
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from ament_index_python.packages import get_package_share_directory
from ros_gz_interfaces.srv import SpawnEntity

class SpawnTestNode(Node):
    def __init__(self):
        super().__init__('spawn_test_node')
        
        # 1. 액션/위치 정보를 받을 구독자 생성 (/tictactoe_action 토픽)
        self.subscription = self.create_subscription(
            String,
            '/tictactoe_action',
            self.action_callback,
            10
        )
        
        # 2. Gazebo Harmonic 엔티티 생성 서비스 클라이언트 연결
        self.spawn_service_name = '/world/tictactoe_world/create'
        # self.spawn_service_name = '/world/empty_world/create'
        self.spawn_client = self.create_client(SpawnEntity, self.spawn_service_name)
        self.get_logger().info(f"Spawn client created for service: {self.spawn_service_name}")
            
        # 3x3 보드판 규격에 맞춘 칸별 좌표 딕셔너리
        self.cell_coordinates = {
            (0, 0): {'x': 0.38, 'y':  0.08, 'z': 0.04},
            (0, 1): {'x': 0.38, 'y':  0.00, 'z': 0.04},
            (0, 2): {'x': 0.38, 'y': -0.08, 'z': 0.04},
            
            (1, 0): {'x': 0.30, 'y':  0.08, 'z': 0.04},
            (1, 1): {'x': 0.30, 'y':  0.00, 'z': 0.04}, # 중앙
            (1, 2): {'x': 0.30, 'y': -0.08, 'z': 0.04},
            
            (2, 0): {'x': 0.22, 'y':  0.08, 'z': 0.04},
            (2, 1): {'x': 0.22, 'y':  0.00, 'z': 0.04},
            (2, 2): {'x': 0.22, 'y': -0.08, 'z': 0.04},
        }
        
        self.get_logger().info("Spawn Test Node Ready. Send message to /tictactoe_action (e.g., human,1,1)")

    def action_callback(self, msg):
        try:
            parts = msg.data.split(',')
            player = parts[0].strip()
            row = int(parts[1].strip())
            col = int(parts[2].strip())
        except Exception as e:
            self.get_logger().error(f"Invalid message format! Use 'player,row,col' (e.g. human,1,1). Error: {e}")
            return

        # 고유한 타임스탬프를 조합하여 중복 엔티티 이름 충돌(Interrupted system call) 원천 차단
        timestamp = int(time.time() * 1000) # 밀리초 단위로 충돌 확률 극소화
        if player == "human":
            filename = "o_mark.sdf"
            entity_name = f"human_piece_{row}_{col}_{timestamp}"
        elif player == "robot":
            filename = "x_mark.sdf"
            entity_name = f"robot_piece_{row}_{col}_{timestamp}"
        else:
            self.get_logger().error(f"Unknown player type: {player}")
            return

        # SDF 파일 읽기
        sdf_content = self.load_model_sdf(filename)
        if not sdf_content:
            return

        # 해당 셀 좌표 가져오기
        coords = self.cell_coordinates.get((row, col))
        if not coords:
            self.get_logger().error(f"Coordinates for cell ({row}, {col}) not found!")
            return

        # Gazebo Harmonic (ros_gz_interfaces) 방식의 요청 구성
        request = SpawnEntity.Request()
        request.entity_factory.name = entity_name
        request.entity_factory.sdf = sdf_content
        request.entity_factory.pose.position.x = float(coords['x'])
        request.entity_factory.pose.position.y = float(coords['y'])
        request.entity_factory.pose.position.z = float(coords['z'])
        request.entity_factory.pose.orientation.w = 1.0

        self.get_logger().info(f"Spawning {player} piece as '{entity_name}' at ({row}, {col})")
        
        if not self.spawn_client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error(f"Spawn service {self.spawn_service_name} not available!")
            return

        # 서비스 서버 대기 후 비동기 호출
        if not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().error(f"Spawn service {self.spawn_service_name} not available!")
            return

        future = self.spawn_client.call_async(request)
        future.add_done_callback(
            lambda completed_future: self.spawn_response_callback(
                completed_future, entity_name, row, col
            )
        )

    def load_model_sdf(self, filename):
        try:
            pkg_dir = get_package_share_directory('project2')
            model_path = os.path.join(pkg_dir, 'models', filename)
            with open(model_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.get_logger().error(f"SDF file read error ({filename}): {e}")
            return ""

    def spawn_response_callback(self, future, entity_name, row, col):
        try:
            response = future.result()
            if response is not None and getattr(response, 'success', False):
                self.get_logger().info(f"Successfully spawned {entity_name} at ({row}, {col})!")
            else:
                self.get_logger().warning(f"Spawn failed for {entity_name}")
        except Exception as e:
            self.get_logger().error(f"Service callback error: {e}")
        
def main(args=None):
    rclpy.init(args=args)
    node = SpawnTestNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()