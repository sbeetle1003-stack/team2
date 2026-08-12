#!/usr/bin/env python3
"""실제 로봇으로 PlacePiece 한 번 실행하는 왕복(잡기->복귀) 테스트.

실물 틱택토 판/말이 아직 없어서 실제로 뭔가를 집지는 못하지만, real
hardware를 향해 pick_place_controller(OPEN_GRIPPER -> ... -> RETURN_HOME)
전체 동작 시퀀스가 정상 실행되는지, 그리고 그 동안 digital_twin_bridge를 통해
Gazebo 트윈이 같이 움직이는지 확인하기 위한 스모크 테스트.

실행 순서 (터미널 3개):
  1) ros2 launch open_manipulator_bringup open_manipulator_x.launch.py \
       port_name:=/dev/ttyUSB0 use_sim:=false
  2) ros2 run project2 pick_place_controller \
       --ros-args --params-file config/manipulation_real.yaml
  3) ros2 launch project2 digital_twin.launch.py   (선택: Gazebo에서 같이 보고 싶으면)
  4) ros2 run project2 digital_twin_grab_test --ros-args -p cell_id:=4
"""
import sys

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from project2_interfaces.action import PlacePiece


class DigitalTwinGrabTest(Node):
    def __init__(self):
        super().__init__('digital_twin_grab_test')
        self.declare_parameter('cell_id', 4)
        self.client = ActionClient(self, PlacePiece, 'place_piece')
        self.done = False
        self.success = False

    def run(self):
        cell_id = self.get_parameter('cell_id').value
        self.get_logger().info(
            f'place_piece 액션 서버를 기다리는 중... (cell_id={cell_id})'
        )
        if not self.client.wait_for_server(timeout_sec=10.0):
            self.get_logger().error(
                'place_piece 액션 서버를 찾을 수 없습니다. '
                'pick_place_controller가 실행 중인지 확인하세요.'
            )
            return False

        goal = PlacePiece.Goal()
        goal.cell_id = cell_id
        future = self.client.send_goal_async(
            goal, feedback_callback=self._on_feedback
        )
        rclpy.spin_until_future_complete(self, future)
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('goal이 거부되었습니다.')
            return False

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        result = result_future.result().result
        self.get_logger().info(f'결과: success={result.success}, {result.message}')
        return result.success

    def _on_feedback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'[{feedback.progress:5.1f}%] {feedback.stage}')


def main(args=None):
    rclpy.init(args=args)
    node = DigitalTwinGrabTest()
    try:
        success = node.run()
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
