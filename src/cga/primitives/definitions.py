"""
Filename: definitions.py
Author: William Bowley
Version: 0.1
Date: 2025-09-26

Description:
    This file defines enums that are used
    throughout the repo.
"""

from enum import Enum, auto
from dataclasses import dataclass


@dataclass
class Point:
    """
    Representation of a point
    with the cartesian coordinate system
    """
    x: float
    y: float


@dataclass
class Line:
    """
    Representation of a directed line system
    """
    start: Point
    end: Point

    def __hash__(self) -> int:
        """ Hash based on start and end point """
        point_tuples = {
            (p.x, p.y) for p in (self.start, self.end)
        }
        return hash(frozenset(point_tuples))


class Orientation(Enum):
    """
    Orientation types
    """
    LEFT = auto()
    RIGHT = auto()
    COLLINEAR = auto()
