"""
Filename: slow_convex_hull.py
Author: William Bowley
Version: 0.1
Date: 2025-09-26

Description:
    Implementation of SlowConvexHull
    algorithm described in chapter 1.

    This algorithm has a time complexity of
    O(n^3), which makes it practically usable
    for large sets
"""

from primitives.definitions import Point, Line, Orientation
from primitives.orientation_test import test_orientation
from primitives.order_clockwise import order_clockwise


def slow_convex_hull(
    vertices: list[Point]
) -> list[Point]:
    """
    Checks every point until a right turn,
    than adds that point to a edge list.

    After iterating across the whole list,
    the edge list is sorted in clockwise order.
    """
    edges = []

    for p in vertices:
        for q in vertices:
            if p == q:
                continue

            valid = True
            AB = Line(p, q)

            for r in vertices:
                if r == p or r == q:
                    continue

                test = test_orientation(AB, r)
                if test == Orientation.LEFT:
                    valid = False
                    break

            if valid:
                if q not in edges:
                    edges.append(q)

    return order_clockwise(edges)


if __name__ == "__main__":
    points = [
        Point(0, 0),
        Point(1, 0),
        Point(0, 1),
        Point(1, 1),
        Point(0.5, 0.5),
        Point(0.2, 0.8)
    ]
    output = slow_convex_hull(points)
    print("Convex Hull:", output)
