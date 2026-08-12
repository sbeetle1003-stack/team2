import pytest
from geometry_msgs.msg import TransformStamped
from rclpy.duration import Duration
from rclpy.time import Time
from tf2_ros import Buffer

from project2.board_geometry import cell_offset, lookup_cell_pose_in_base


def test_cell_offsets_are_row_major():
    assert cell_offset(0, 0.08) == pytest.approx((-0.08, 0.08))
    assert cell_offset(4, 0.08) == pytest.approx((0.0, 0.0))
    assert cell_offset(8, 0.08) == pytest.approx((0.08, -0.08))


def test_cell_id_range_is_checked():
    for invalid_cell in (-1, 9):
        try:
            cell_offset(invalid_cell, 0.08)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid cell_id was accepted')


def _translated_transform(parent, child, stamp, x, y, z):
    transform = TransformStamped()
    transform.header.frame_id = parent
    transform.header.stamp = stamp
    transform.child_frame_id = child
    transform.transform.translation.x = x
    transform.transform.translation.y = y
    transform.transform.translation.z = z
    transform.transform.rotation.w = 1.0
    return transform


def test_lookup_cell_pose_in_base_uses_detection_stamp_not_now():
    buffer = Buffer()

    detect_time = Time(seconds=10, nanoseconds=0)
    now_time = Time(seconds=10, nanoseconds=500_000_000)

    # The marker was only seen at detect_time.
    buffer.set_transform(
        _translated_transform(
            'camera_optical', 'board_frame', detect_time.to_msg(), 0.05, 0.0, 0.2,
        ),
        'test',
    )
    # The camera->base chain is known at both instants (arm keeps moving).
    buffer.set_transform(
        _translated_transform(
            'link1', 'camera_optical', detect_time.to_msg(), 0.0, 0.0, 0.3,
        ),
        'test',
    )
    buffer.set_transform(
        _translated_transform(
            'link1', 'camera_optical', now_time.to_msg(), 10.0, 10.0, 10.0,
        ),
        'test',
    )

    result = lookup_cell_pose_in_base(
        buffer,
        4,  # center cell -> board-frame offset (0, 0)
        base_frame='link1',
        board_frame='board_frame',
        camera_frame='camera_optical',
        cell_spacing=0.08,
        now=now_time,
        max_age=Duration(seconds=2.0),
    )

    assert result is not None
    assert result.header.frame_id == 'link1'
    # Must use the link1->camera_optical pose from detect_time (z=0.3),
    # not the wildly different one published later at now_time.
    assert result.pose.position.x == pytest.approx(0.05)
    assert result.pose.position.y == pytest.approx(0.0)
    assert result.pose.position.z == pytest.approx(0.5)


def test_lookup_cell_pose_in_base_returns_none_when_stale():
    buffer = Buffer()
    detect_time = Time(seconds=10, nanoseconds=0)
    now_time = Time(seconds=20, nanoseconds=0)

    buffer.set_transform(
        _translated_transform(
            'camera_optical', 'board_frame', detect_time.to_msg(), 0.0, 0.0, 0.0,
        ),
        'test',
    )
    buffer.set_transform(
        _translated_transform(
            'link1', 'camera_optical', detect_time.to_msg(), 0.0, 0.0, 0.0,
        ),
        'test',
    )

    result = lookup_cell_pose_in_base(
        buffer,
        4,
        base_frame='link1',
        board_frame='board_frame',
        camera_frame='camera_optical',
        cell_spacing=0.08,
        now=now_time,
        max_age=Duration(seconds=2.0),
    )

    assert result is None


def test_lookup_cell_pose_in_base_returns_none_when_never_seen():
    buffer = Buffer()

    result = lookup_cell_pose_in_base(
        buffer,
        4,
        base_frame='link1',
        board_frame='board_frame',
        camera_frame='camera_optical',
        cell_spacing=0.08,
    )

    assert result is None
