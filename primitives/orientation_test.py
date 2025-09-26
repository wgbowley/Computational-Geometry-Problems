"""
Filename: orientation_test.py
Author: William Bowley
Version: 0.1
Date: 2025-09-26

Description:
    Determines the orientation of a point relative to a
    directed line AB.

    Uses the cross product test to check if the point is:
        - Left of the line
        - Right of the line
        - Collinear with the line
"""

from primitives.definitions import Point, Line, Orientation


def test_orientation(
    AB: Line,
    P: Point
) -> Orientation:
    """
    Determines the orientation of a point P relative to
    directed line AB

    Args:
        AB: Line dataclass
        P: Point dataclass
    """
    a = AB.start.x, AB.start.y
    b = AB.end.x, AB.end.y
    p = P.x, P.y

    # Cross product
    val = (b[0] - a[0])*(p[1] - a[1]) - (b[1] - a[1])*(p[0] - a[0])

    if val > 0:
        return Orientation.LEFT
    elif val < 0:
        return Orientation.RIGHT
    else:
        return Orientation.COLLINEAR
