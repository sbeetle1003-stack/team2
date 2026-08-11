"""Geometry helpers shared by the pick-and-place controller and tests."""


def cell_center(cell_id, origin_x, origin_y, spacing):
    """Return the board-frame center of a row-major cell index."""
    if not 0 <= cell_id <= 8:
        raise ValueError('cell_id must be between 0 and 8')
    row, column = divmod(cell_id, 3)
    x = origin_x + (column - 1) * spacing
    y = origin_y + (1 - row) * spacing
    return x, y


def supply_position(piece_index, supply_x, supply_y, supply_spacing):
    """Return the fixed feeder position for a zero-based robot piece index."""
    if piece_index < 0:
        raise ValueError('piece_index must not be negative')
    return supply_x + piece_index * supply_spacing, supply_y
