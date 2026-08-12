"""Board-frame-relative cell geometry and TF2 lookups into the robot base frame."""

from geometry_msgs.msg import PoseStamped
from rclpy.time import Time
from tf2_geometry_msgs import do_transform_pose
from tf2_ros import ConnectivityException, ExtrapolationException, LookupException

TF_LOOKUP_ERRORS = (LookupException, ConnectivityException, ExtrapolationException)


def cell_offset(cell_id, cell_spacing):
    """Return the board-frame-relative (x, y) center of a row-major cell index."""
    if not 0 <= cell_id <= 8:
        raise ValueError('cell_id must be between 0 and 8')
    row, column = divmod(cell_id, 3)
    x = (column - 1) * cell_spacing
    y = (1 - row) * cell_spacing
    return x, y


def lookup_cell_pose_in_base(
    buffer,
    cell_id,
    *,
    base_frame,
    board_frame,
    camera_frame,
    cell_spacing,
    now=None,
    max_age=None,
    timeout=None,
):
    """Transform a board-frame cell center into base_frame using the TF tree.

    The camera is mounted on the moving arm, so the whole base_frame ->
    board_frame chain is looked up at the timestamp of the most recent
    camera_frame -> board_frame detection instead of "now". Otherwise the
    lookup could mix the robot's current joint pose with a stale marker
    observation taken while the arm was somewhere else.

    Returns None if board_frame has not been observed (recently enough, when
    `now`/`max_age` are given), or if the TF chain is not available.
    """
    try:
        latest = buffer.lookup_transform(camera_frame, board_frame, Time())
    except TF_LOOKUP_ERRORS:
        return None

    detect_stamp = Time.from_msg(latest.header.stamp)

    if max_age is not None and now is not None:
        age_ns = now.nanoseconds - detect_stamp.nanoseconds
        if age_ns > max_age.nanoseconds:
            return None

    lookup_kwargs = {} if timeout is None else {'timeout': timeout}
    try:
        board_in_base = buffer.lookup_transform(
            base_frame, board_frame, detect_stamp, **lookup_kwargs,
        )
    except TF_LOOKUP_ERRORS:
        return None

    x, y = cell_offset(cell_id, cell_spacing)
    cell_pose = PoseStamped()
    cell_pose.header.frame_id = board_frame
    cell_pose.header.stamp = latest.header.stamp
    cell_pose.pose.orientation.w = 1.0
    cell_pose.pose.position.x = float(x)
    cell_pose.pose.position.y = float(y)
    cell_pose.pose.position.z = 0.0

    result = PoseStamped()
    result.header.frame_id = base_frame
    result.header.stamp = latest.header.stamp
    result.pose = do_transform_pose(cell_pose.pose, board_in_base)
    return result
