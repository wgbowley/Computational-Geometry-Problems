"""
Filename: get_intersection.py
Author: William Bowley
Version: 0.1
Date: 2026-01-06

Description:
    Determines if two line segments intersect,
    if so returns a point of intersection
"""


from typing import Optional
from cga.primitives.definitions import Point, Line


def get_intersection(l1: Line, l2: Line) -> Optional[Point]:
    """
    Returns the point of intersection if it exists within
    the line segments, otherwise returns none
    """

    # Line: p1 + t * (p2 - p1) & p3 + u * (p4 - p3)
    p1, p2 = l1.start, l2.end
    p3, p4 = l2.start, l2.end

    # Denominator for parameters t & u
    den = (p2.x - p1.x) * (p4.y - p3.y) - (p2.y - p1.y) * (p4.x - p3.x)

    # if denominator is 0, lines are parallel
    if den == 0:
        return None

    # Calculate parameters t and u
    t_num = (p3.x - p1.x) * (p4.y - p3.y) - (p3.y - p1.y) * (p4.x - p3.x)
    u_num = (p3.x - p1.x) * (p2.y - p1.y) - (p3.y - p1.y) * (p2.x - p1.x)

    t = t_num / den
    u = u_num / den

    # Check if intersection point lies within both segments (0 <= t, u <= 1)
    if 0 <= t <= 1 and 0 <= u <= 1:
        intersect_x = p1.x + t * (p2.x - p1.x)
        intersect_y = p1.y + t * (p2.y - p1.y)
        return Point(intersect_x, intersect_y)

    return None
