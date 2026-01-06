"""
Filename: convex_hull.py
Author: William Bowley
Version: 0.1
Date: 2025-11-02

Description:
    Implementation of ConvexHull
    algorithm described in chapter 1.

    This algorithm has a time complexity of
    O(nlog(n))
"""

from cga.primitives.definitions import Point, Line, Orientation
from cga.primitives.orientation_test import test_orientation
from cga.primitives.order_clockwise import order_clockwise


def _is_left(hull: list[Point]) -> bool:
    """
    Returns True if the last three points make a
    left turn or are collinear.
    """
    length = len(hull)
    if length < 3:
        return False

    A, B, C = hull[-3], hull[-2], hull[-1]
    AB = Line(A, B)

    return test_orientation(AB, C) != Orientation.RIGHT


def _upper_hull(vertices: list[Point]) -> list[Point]:
    """
    Creates a upper hull for the full convex hull
    """
    upper = [vertices[0], vertices[1]]

    # Goes from index 2 upward to length of vertices
    for i in range(2, len(vertices)):
        upper.append(vertices[i])
        # While the last three points make a left turn,
        # remove the middle point
        while _is_left(upper):
            del upper[len(upper) - 2]

    return upper


def _lower_hull(vertices: list[Point]) -> list[Point]:
    """
    Creates a lower hull for the full convex hull
    """
    lower = [vertices[-1], vertices[-2]]

    # Goes from (n-2) downward to index 1
    for i in range(len(vertices) - 3, -1, -1):
        lower.append(vertices[i])

        # While the last three points make a left turn,
        # remove the middle point
        while _is_left(lower):
            del lower[len(lower) - 2]

    return lower


def convex_hull(vertices: list[Point]) -> list[Point]:
    """
    Sorts the vertices by x-coordinate
    and then creates two hulls (upper and lower).
    And lastly combines them together
    """
    if len(vertices) <= 1:
        return vertices

    vertices = sorted(vertices, key=lambda p: (p.x, p.y))

    upper: list = _upper_hull(vertices)
    lower: list = _lower_hull(vertices)

    # Combine upper and lower hulls, removing duplicate endpoints
    return order_clockwise(upper[:-1] + lower[:-1])


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
