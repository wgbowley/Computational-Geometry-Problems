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


class Orientation(Enum):
    """
    Orientation types
    """
    LEFT = auto()
    RIGHT = auto()
    COLLINEAR = auto()
