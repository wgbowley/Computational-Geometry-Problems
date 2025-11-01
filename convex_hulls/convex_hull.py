"""
Filename: convex_hull.py
Author: William Bowley
Version: 0.1
Date: 2025-11-02

Description:
    Implementation of ConvexHull
    algorithm described in chapter 1.

    This algorithm has a time complexity of
    O(nln(n))
"""

from primitives.definitions import Point, Line, Orientation
from primitives.orientation_test import test_orientation
from primitives.order_clockwise import order_clockwise


def _is_not_right_turn(
    hull: list[Point]
) -> bool:
    """
    Checks if the last three points do not make
    a right turn with respect to line AB.
    """
    length = len(hull)
    if length < 3:
        return False

    AB = Line(hull[length-3], hull[length-2])
    test = test_orientation(AB, hull[length-1])

    if test == Orientation.RIGHT:
        return False

    return True


def _upper_hull(
    vertices: list[Point]
) -> list[Point]:
    """
    Creates a upper hull for the full convex hull
    """
    length = len(vertices)
    upper: list[Point] = [vertices[0], vertices[1]]

    # Goes 2 up to length of vertices
    for i in range(2, length):
        upper.append(vertices[i])
        while _is_not_right_turn(upper):
            # if _hull_check is true
            # Removes middle of the last three points
            del upper[len(upper) - 2]

    return upper


def _lower_hull(
    vertices: list[Point]
) -> list[Point]:
    """
    Creates a lower hull for the full convex hull
    """
    lower: list[Point] = [vertices[-1], vertices[-2]]

    # Goes (n-2) down to 1
    for i in range(len(vertices) - 3, -1, -1):
        lower.append(vertices[i])

        while _is_not_right_turn(lower):
            # if _hull_check is true
            # Removes middle of the last three points
            del lower[len(lower) - 2]

    return lower


def convex_hull(
    vertices: list[Point]
) -> list[Point]:
    """
    Sorts the vertices by x-coordinate
    and than creates two hulls (upper and lower).
    And lastly combines them together
    """
    vertices: list = sorted(
        vertices, key=lambda p: (p.x, p.y)
    )

    upper: list = _upper_hull(vertices)
    lower: list = _lower_hull(vertices)

    return order_clockwise(
        upper[:-1] + lower[:-1]
    )


if __name__ == "__main__":
    points = [
        Point(0, 0),
        Point(1, 0),
        Point(0, 1),
        Point(1, 1),
        Point(0.5, 0.5),
        Point(0.2, 0.8)
    ]
    output = convex_hull(points)
    print("Convex Hull:", output)
