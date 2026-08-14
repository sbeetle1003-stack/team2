import rclpy
from rclpy.duration import Duration
from rclpy.node import Node

from tf2_ros import Buffer, TransformListener

from project2.board_geometry import lookup_cell_pose_in_base


class BoardCellTest(Node):

    def __init__(self):
        super().__init__('board_cell_test')

        self.buffer = Buffer()
        self.listener = TransformListener(
            self.buffer,
            self,
        )

        self.base_frame = 'link1'
        self.board_frame = 'board_frame'
        self.camera_frame = 'camera_optical'

        # 실제 게임판 한 칸 중심 간격: 5 cm
        self.cell_spacing = 0.05

        self.timer = self.create_timer(
            1.0,
            self.print_cells,
        )

    def print_cells(self):

        self.get_logger().info(
            '----- Board cell poses -----'
        )

        for cell_id in range(9):

            pose = lookup_cell_pose_in_base(
                self.buffer,
                cell_id,
                base_frame=self.base_frame,
                board_frame=self.board_frame,
                camera_frame=self.camera_frame,
                cell_spacing=self.cell_spacing,
                now=self.get_clock().now(),
                max_age=Duration(seconds=5.0),
                timeout=Duration(seconds=0.2),
            )

            if pose is None:
                self.get_logger().warning(
                    f'cell {cell_id}: TF unavailable'
                )
                continue

            p = pose.pose.position

            self.get_logger().info(
                f'cell {cell_id}: '
                f'x={p.x:.4f}, '
                f'y={p.y:.4f}, '
                f'z={p.z:.4f}'
            )


def main(args=None):
    rclpy.init(args=args)

    node = BoardCellTest()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()