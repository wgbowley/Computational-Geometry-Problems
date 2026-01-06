"""
Filename: event_queue.py
Author: William Bowley
Version: 0.1
Date: 2025-11-02

Description:
    Implementation of FindIntersections
    algorithm described in chapter 2.

    This class is part of the algorithm that
    manages event point order
"""

from enum import Enum, auto
from dataclasses import dataclass
from cga.primitives.definitions import Point, Line


class EventType(Enum):
    """ Type of event the point represents """
    UPPER = auto()
    LOWER = auto()
    INTERIOR = auto()


@dataclass
class Node:
    """ Represents node within the heap """
    point: Point
    line: Line
    event_type: EventType
    id: int


class EventQueue:
    """
    Manages the highest-priority queue via using
    event points x and y coordinates to order them
    """
    def __init__(self) -> None:
        """ Creates the heap structure """
        self.heap: list[Node] = []
        self._next_id: int = 0

    @property
    def number_items(self) -> int:
        """ Returns the total number of items in the queue"""
        return len(self.heap)

    def _has_higher_priority(self, child: Node, parent: Node) -> bool:
        """ Returns TRUE if child is higher priority than parent """
        # Primary: Highest Y
        if child.point.y != parent.point.y:
            return child.point.y > parent.point.y

        # Secondary: Lowest X
        if child.point.x != parent.point.x:
            return child.point.x < parent.point.x

        # Tertiary: Tie-breaker (Priority to upper over lower)
        if child.event_type != parent.event_type:
            return child.event_type.value < parent.event_type.value

        # Final: Tie-breaker (lowest ID)
        return child.id < parent.id

    def peek_point(self) -> Point:
        """
        Returns the point of the highest priority node without removing it.
        """
        if not self.heap:
            return None
        return self.heap[0].point

    def enqueue(self, point: Point, e_type: EventType, line: Line) -> None:
        """ Adds a point and its segment, maintaining the sorted order """
        index = self._add_item(point, e_type, line)
        self._sift_up(index)

    def dequeue(self) -> Node:
        """ Removes and returns the highest priority event """
        if not self.heap:
            raise IndexError("Cannot dequeue from an empty EventQueue")

        max_item = self.heap[0]

        if len(self.heap) == 1:
            self.heap.pop()
        else:
            # Replaces root with last item
            self.heap[0] = self.heap.pop()
            # Restores highest priority
            self._sift_down(0)

        return max_item

    def _add_item(self, point: Point, e_type: EventType, line: Line) -> int:
        """ Adds item to the binary heap and increments the ID """

        # Adds the new node to the heap
        new_node = Node(point, line, e_type, self._next_id)
        self.heap.append(new_node)
        self._next_id += 1

        return len(self.heap) - 1

    def _sift_up(self, c_index: int) -> None:
        """ Sifts the child up the heap """
        heap = self.heap
        while c_index > 0:
            p_index = (c_index - 1) // 2

            # Checks if the child has higher or equal priority than the parent
            if self._has_higher_priority(heap[c_index], heap[p_index]):
                heap[c_index], heap[p_index] = heap[p_index], heap[c_index]

                c_index = p_index
            else:
                # The heap property is satisfied
                # (parent has higher or equal priority)
                break

    def _sift_down(self, r_index: int) -> None:
        """ Sifts the root down the heap to restore heap """
        heap = self.heap
        max_i = len(self.heap) - 1

        while True:
            left_child = 2 * r_index + 1
            right_child = 2 * r_index + 2
            highest = r_index

            # Checks left child against current node
            if left_child <= max_i:
                if self._has_higher_priority(heap[left_child], heap[highest]):
                    highest = left_child

            # Check right child against the current node
            if right_child <= max_i:
                if self._has_higher_priority(heap[right_child], heap[highest]):
                    highest = right_child

            if highest != r_index:
                # Swap down with the highest priority child
                heap[r_index], heap[highest] = heap[highest], heap[r_index]
                r_index = highest
            else:
                break

    def __len__(self) -> int:
        """Returns the number of events in the queue."""
        return len(self.heap)
