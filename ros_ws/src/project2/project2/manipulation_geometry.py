"""Geometry helpers shared by the pick-and-place controller and tests."""


def cell_center(cell_id, origin_x, origin_y, spacing):
    """Return the board-frame center of a row-major cell index.

    Robot and human sit on opposite sides of the board along x (robot at
    the origin, human beyond the board at large +x -- see the world file's
    default GUI camera, which stands past the board facing -x back at the
    robot). Row maps to x so row 1 is nearest the robot (small x) and row 3
    is nearest the human (large x). Column maps to y so column 1 is on the
    human's left (-y) and column 3 is on the human's right (+y): a camera
    at yaw=pi (facing -x) has its local +y pointing to world -y, so world
    +y is that camera's right side, matching how the human reads the board
    left-to-right while facing the robot.
    """
    if not 0 <= cell_id <= 8:
        raise ValueError('cell_id must be between 0 and 8')
    row, column = divmod(cell_id, 3)
    x = origin_x + (row - 1) * spacing
    y = origin_y + (column - 1) * spacing
    return x, y


def supply_position(piece_index, supply_x, supply_y, supply_spacing):
    """Return the fixed feeder position for a zero-based robot piece index."""
    if piece_index < 0:
        raise ValueError('piece_index must not be negative')
    return supply_x + piece_index * supply_spacing, supply_y
