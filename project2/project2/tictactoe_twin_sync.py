import rclpy
from rclpy.node import Node
from std_msgs.msg import String
# Gazebo spawn entities service 관련 메시지 임포트 필요
from gazebo_msgs.srv import SpawnEntity

class TicTacToeTwinSync(Node):
    def __init__(self):
        super().__init__('tictactoe_twin_sync')
        self.subscription = self.create_subscription(
            String,
            '/tictactoe_action',
            self.action_callback,
            10
        )
        self.cli = self.create_client(SpawnEntity, '/spawn_entity')
        
    def action_callback(self, msg):
        # msg.data 예: "robot,1,1" (로봇이 (1,1) 셀에 놓음)
        player, row, col = msg.data.split(',')
        self.get_logger().info(f"Received Action -> Player: {player}, Cell: ({row}, {col})")
        
        # 위치 좌표 매핑 후 Gazebo 스폰 서비스 호출 로직 구현
        # self.spawn_model_in_gazebo(row, col, player)

def main(args=None):
    rclpy.init(args=args)
    node = TicTacToeTwinSync()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()