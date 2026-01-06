"""
Filename: order_clockwise.py
Author: William Bowley
Version: 0.1
Date: 2025-09-26

Description:
    Orders a list of point object
    in clockwise order
"""

from math import atan2
from cga.primitives.definitions import Point


def order_clockwise(points: list[Point]) -> list[Point]:
    """
    Orders a list of point object in clockwise order
    """
    cx = sum(p.x for p in points) / len(points)
    cy = sum(p.y for p in points) / len(points)

    # Sort points by angle from centroid (clockwise)
    return sorted(
        points,
        key=lambda p: atan2(p.y - cy, p.x - cx),
        reverse=True
    )
