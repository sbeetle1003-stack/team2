import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class DigitalTwinRobotSync(Node):
    def __init__(self):
        super().__init__('digital_twin_robot_sync')
        
        # 실제 로봇의 joint_states 구독
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )
        
        # Gazebo 가상 로봇 제어를 위한 퍼블리셔 (필요 시 연결)
        # self.publisher = self.create_publisher(JointState, '/controlled_joint_states', 10)
        
        self.get_logger().info("Digital Twin Robot Sync Node Started.")

    def joint_state_callback(self, msg):
        # 실제 로봇의 관절 이름과 위치(position) 로깅 및 동기화 처리
        self.get_logger().debug(f"Syncing Joints -> Names: {msg.name}, Positions: {msg.position}")
        
        # 가상 로봇 동기화 제어 로직 작성 공간
        # (ros2_control이 정상 설정되어 있다면 별도 코드가 없어도 /joint_states 공유를 통해 자동 동기화됩니다)

def main(args=None):
    rclpy.init(args=args)
    node = DigitalTwinRobotSync()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()