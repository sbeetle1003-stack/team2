"""Mirror integration-branch ``/board_state`` updates into Gazebo Sim.

The integration branch publishes a full nine-cell ``Int8MultiArray`` board:
0 is empty, 1 is HUMAN, and 2 is ROBOT.  Gazebo Sim does not provide the
Gazebo Classic ``/spawn_entity`` service used by the first prototype, so the
existing ArUco cube entities are moved through ``SetEntityPose`` instead.
"""

from project2.manipulation_geometry import cell_center, supply_position

import rclpy
from geometry_msgs.msg import Pose
from rclpy.node import Node
from ros_gz_interfaces.msg import Entity
from ros_gz_interfaces.srv import SetEntityPose
from std_msgs.msg import Int8MultiArray


EMPTY = 0
HUMAN = 1
ROBOT = 2
BOARD_SIZE = 9


class DigitalTwinBoard(Node):
    """Move the fixed human/robot cube pool to match ``/board_state``."""

    def __init__(self):
        """Declare synchronizer parameters, topics, and pose retry state."""
        super().__init__('digital_twin_board')

        self.declare_parameter('board_state_topic', '/board_state')
        self.declare_parameter(
            'set_pose_service',
            '/world/tictactoe_world/set_pose',
        )
        self.declare_parameter('board_origin_x', 0.30)
        self.declare_parameter('board_origin_y', 0.0)
        self.declare_parameter('cell_spacing', 0.08)
        self.declare_parameter('board_piece_z', 0.025)
        self.declare_parameter('robot_supply_x', 0.10)
        self.declare_parameter('robot_supply_y', -0.20)
        self.declare_parameter('human_supply_x', 0.10)
        self.declare_parameter('human_supply_y', 0.20)
        self.declare_parameter('supply_spacing', 0.05)
        self.declare_parameter('robot_piece_prefix', 'robot_cube_')
        self.declare_parameter('human_piece_prefix', 'human_cube_')
        self.declare_parameter('robot_first_marker_id', 6)
        self.declare_parameter('human_first_marker_id', 11)

        self.pose_client = self.create_client(
            SetEntityPose,
            self.get_parameter('set_pose_service').value,
        )
        self.create_subscription(
            Int8MultiArray,
            self.get_parameter('board_state_topic').value,
            self._board_state_callback,
            10,
        )

        # Desired poses survive DDS discovery delays and are retried until
        # Gazebo acknowledges them.
        self.desired_poses = {}
        self.in_flight = {}
        self.placements = {}
        self.current_board = None
        self.create_timer(0.5, self._flush_poses)

        self.get_logger().info(
            'Digital twin board sync started; waiting for /board_state.'
        )

    def _board_state_callback(self, message):
        board = list(message.data)
        if len(board) != BOARD_SIZE:
            self.get_logger().warning(
                f'Ignoring board state with {len(board)} cells; expected 9.'
            )
            return
        if any(value not in (EMPTY, HUMAN, ROBOT) for value in board):
            self.get_logger().warning(
                'Ignoring board state containing UNKNOWN values.'
            )
            return
        if board == self.current_board:
            return

        self._apply_board(board)
        self.current_board = board

    def _apply_board(self, board):
        old_placements = self.placements
        new_placements = {}
        used_pieces = set()

        for cell_id, player in enumerate(board):
            if player == EMPTY:
                continue

            old = old_placements.get(cell_id)
            if old is not None and old[0] == player:
                new_placements[cell_id] = old
                used_pieces.add((player, old[1]))
                continue

            piece_index = self._next_piece_index(player, used_pieces)
            if piece_index is None:
                self.get_logger().error(
                    f'No {self._player_name(player)} cube is available '
                    f'for cell {cell_id}.'
                )
                continue

            new_placements[cell_id] = (player, piece_index)
            used_pieces.add((player, piece_index))
            self._queue_board_pose(player, piece_index, cell_id)

        active_pieces = set(new_placements.values())
        for player, piece_index in old_placements.values():
            if (player, piece_index) not in active_pieces:
                self._queue_supply_pose(player, piece_index)

        self.placements = new_placements

    def _next_piece_index(self, player, used_pieces):
        for piece_index in range(5):
            if (player, piece_index) not in used_pieces:
                return piece_index
        return None

    @staticmethod
    def _player_name(player):
        return 'human' if player == HUMAN else 'robot'

    def _entity_name(self, player, piece_index):
        if player == HUMAN:
            prefix = self.get_parameter('human_piece_prefix').value
            marker_id = self.get_parameter('human_first_marker_id').value
        else:
            prefix = self.get_parameter('robot_piece_prefix').value
            marker_id = self.get_parameter('robot_first_marker_id').value
        return f'{prefix}{marker_id + piece_index}'

    def _queue_board_pose(self, player, piece_index, cell_id):
        origin_x = self.get_parameter('board_origin_x').value
        origin_y = self.get_parameter('board_origin_y').value
        spacing = self.get_parameter('cell_spacing').value
        x, y = cell_center(cell_id, origin_x, origin_y, spacing)
        z = self.get_parameter('board_piece_z').value
        self._queue_pose(self._entity_name(player, piece_index), x, y, z)

    def _queue_supply_pose(self, player, piece_index):
        if player == HUMAN:
            supply_x = self.get_parameter('human_supply_x').value
            supply_y = self.get_parameter('human_supply_y').value
        else:
            supply_x = self.get_parameter('robot_supply_x').value
            supply_y = self.get_parameter('robot_supply_y').value
        spacing = self.get_parameter('supply_spacing').value
        x, y = supply_position(piece_index, supply_x, supply_y, spacing)
        z = self.get_parameter('board_piece_z').value
        self._queue_pose(self._entity_name(player, piece_index), x, y, z)

    def _queue_pose(self, entity_name, x, y, z):
        self.desired_poses[entity_name] = (float(x), float(y), float(z))
        self._flush_poses()

    def _flush_poses(self):
        if not self.pose_client.service_is_ready():
            return

        for entity_name, pose in list(self.desired_poses.items()):
            if entity_name in self.in_flight:
                continue

            request = SetEntityPose.Request()
            request.entity.name = entity_name
            request.entity.type = Entity.MODEL
            request.pose = Pose()
            request.pose.position.x = pose[0]
            request.pose.position.y = pose[1]
            request.pose.position.z = pose[2]
            request.pose.orientation.w = 1.0

            future = self.pose_client.call_async(request)
            self.in_flight[entity_name] = pose
            future.add_done_callback(
                lambda result, name=entity_name, target=pose:
                self._pose_done(name, target, result)
            )

    def _pose_done(self, entity_name, pose, future):
        self.in_flight.pop(entity_name, None)
        try:
            response = future.result()
        except Exception as error:
            self.get_logger().warning(
                f'Failed to move {entity_name}: {error}'
            )
            return

        if not response.success:
            status = getattr(response, 'status_message', 'no status')
            self.get_logger().warning(
                f'Gazebo rejected pose for {entity_name}: '
                f'{status}'
            )
            return

        if self.desired_poses.get(entity_name) == pose:
            self.desired_poses.pop(entity_name, None)


def main(args=None):
    """Run the board-state synchronizer."""
    rclpy.init(args=args)
    node = DigitalTwinBoard()
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
