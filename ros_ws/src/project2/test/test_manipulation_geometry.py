import pytest

from project2.manipulation_geometry import cell_center, supply_position


def test_cell_centers_are_row_major():
    assert cell_center(0, 0.30, 0.0, 0.08) == pytest.approx((0.22, -0.08))
    assert cell_center(4, 0.30, 0.0, 0.08) == pytest.approx((0.30, 0.0))
    assert cell_center(8, 0.30, 0.0, 0.08) == pytest.approx((0.38, 0.08))


def test_cell_id_range_is_checked():
    for invalid_cell in (-1, 9):
        try:
            cell_center(invalid_cell, 0.25, 0.0, 0.08)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid cell_id was accepted')


def test_supply_position_advances_on_x_axis():
    assert supply_position(0, 0.08, -0.20, 0.05) == (0.08, -0.20)
    assert supply_position(4, 0.08, -0.20, 0.05) == (0.28, -0.20)
