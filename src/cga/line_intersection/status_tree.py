"""
Filename: status_tree.py
Author: William Bowley
Version: 0.1
Date: 2025-11-02

Description:
    Implementation of FindIntersections
    algorithm described in chapter 2.

    This class is part of the algorithm that
    stores and orders the line segments which
    are intersecting with the vertical sweep line
"""

import sys

from math import isclose
from dataclasses import dataclass

from cga.primitives.definitions import Line, Point


# Imports system epsilon for floats
EPSILON = sys.float_info.epsilon


@dataclass
class Node:
    """ Represents a node within the AVL tree """
    line: Line
    height: int
    right_child: "Node"
    left_child: "Node"


def _sweep_intersect(line: Line, sweep_y: float) -> float:
    """ Finds the x-coordinate of intersection with the sweep line """
    ax, ay = line.start.x, line.start.y
    bx, by = line.end.x, line.end.y

    # Primary: Vertical segment
    if isclose(bx, ax):
        return ax

    delta_y = by - ay
    delta_x = bx - ax

    # Secondary: Horizontal Segment
    if isclose(delta_y, 0.0):
        return min(ax, bx)

        # if isclose(ay, sweep_y):
        #     # Returns leftmost x-coordinate for consistent ordering
        #     return min(ax, bx)
        # msg = "Horizontal segment does not intersect sweep line"
        # raise ValueError(msg)

    # Tertiary: Standard segment
    x = ax + (sweep_y - ay) * (delta_x / delta_y)
    return x


def _get_dx_dy(line: Line) -> float:
    """ Depends the slope of the line"""
    dx = line.end.x - line.start.x
    dy = line.end.y - line.start.y

    if dy != 0:
        return dx / dy
    else:
        # Handles vertical lines as having infinite slope
        return float('inf')


class StatusStructure:
    """
    Orders the in-contact line segments with the
    sweep line based on their x coordinate along the line
    """
    def __init__(self) -> None:
        """ Creates the AVL Tree """
        self.tree: Node = None
        self.current_sweep_y: float = float('inf')

    def update_sweep_line(self, sweep_y: float) -> None:
        """ Updates the sweep line y-coordinate """
        self.current_sweep_y = sweep_y

    def insert(self, line: Line) -> bool:
        """ Wrapper for recursive insertion logic """
        new_root, is_intersecting = self._insert_node(self.tree, line)
        self.tree = new_root
        return is_intersecting

    def delete(self, line: Line) -> None:
        """ Wrapper for recursive deletion logic """
        self.tree = self._delete_node(self.tree, line)

    def find_neighbors(self, line: Line) -> tuple[Line | None, Line | None]:
        """
        Locates the line and finds its immediate left and right neighbors
        """
        left = None    # Tracks the largest segment < line
        right = None   # Tracks the smallest segment > line
        current = self.tree

        while current:
            # Tree traversal
            order: int = self._compare_segments(line, current.line)

            # Line segment founded
            if order == 0:
                # Left neighbor is the largest in the left subtree
                if current.left_child:
                    left_node = current.left_child
                    while left_node.right_child:
                        left_node = left_node.right_child
                    left = left_node.line

                # Right neighbor is the smallest in the right subtree
                if current.right_child:
                    right_node = current.right_child
                    while right_node.left_child:
                        right_node = right_node.left_child
                    right = right_node.line

                return left, right

            # Line is left of the current mode
            elif order == -1:
                right = current.line  # Current is a potential right neighbor
                current = current.left_child

            # Line is right of the current mode
            else:
                left = current.line  # Current is a potential left neighbor
                current = current.right_child

        return left, right

    def find_neighbors_at_point(
        self, event_point: Point
    ) -> tuple[Line | None, Line | None]:
        """ Finds segments to the left and right of a specific point """
        left, right = None, None
        current = self.tree

        while current:
            seg_x = _sweep_intersect(current.line, event_point.y)

            if isclose(seg_x, event_point.x):
                # If the point is on segment, use tree neighbors
                return self.find_neighbors(current.line)

            # Uses event point to determine neighbors
            if event_point.x < seg_x:
                right = current.line
                current = current.left_child
            else:
                left = current.line
                current = current.right_child

        return left, right

    def get_leftmost_segment_of_group(self, group: list[Line]) -> Line | None:
        """ Returns the segment in the group with the smallest x-coordinate """
        if not group:
            # Handles when group is none
            return None

        sweep_y = self.current_sweep_y - EPSILON

        leftmost_segment = None
        leftmost_x = None

        for segment in group:
            x_at_sweep = _sweep_intersect(segment, sweep_y)

            if leftmost_segment is None:
                # Handles if leftmost is none
                leftmost_segment = segment
                leftmost_x = x_at_sweep
                continue

            if x_at_sweep < leftmost_x:
                # Handles new left most segment
                leftmost_segment = segment
                leftmost_x = x_at_sweep

        return leftmost_segment

    def get_rightmost_of_group(self, group: list[Line]) -> Line | None:
        """ Returns the segment in the group with the largest x-coordinate """
        if not group:
            # Handles when group is none
            return None

        sweep_y = self.current_sweep_y - EPSILON

        rightmost_segment = None
        rightmost_x = None

        for segment in group:
            x_at_sweep = _sweep_intersect(segment, sweep_y)

            if rightmost_segment is None:
                # Handles if leftmost is none
                rightmost_segment = segment
                rightmost_x = x_at_sweep
                continue

            if x_at_sweep > rightmost_x:
                # Handles new left most segment
                rightmost_segment = segment
                rightmost_x = x_at_sweep

        return rightmost_segment

    def _insert_node(self, node: Node | None, line: Line) -> tuple[Node, bool]:
        """ Inserts a node into the AVL tree via recursion """
        # Primary case: Empty node
        if node is None:
            return Node(line, 1, None, None), False

        # Tree Traversal
        order: int = self._compare_segments(line, node.line)

        is_intersecting: bool = False
        # Moves left down the tree due to line having lower value
        if order == -1:
            new_child, is_intersecting = self._insert_node(
                node.left_child, line
            )
            node.left_child = new_child
        # Moves right down the tree due to line having higher value
        elif order == 1:
            new_child, is_intersecting = self._insert_node(
                node.right_child, line
            )
            node.right_child = new_child
        # Moves right down the tree due to intersection
        else:
            new_child, is_intersecting = self._insert_node(
                node.right_child, line
            )
            node.right_child = new_child
            is_intersecting = True

        node.height = 1 + max(
            self._node_height(node.left_child),
            self._node_height(node.right_child)
        )

        # Balances the AVL tree
        balanced_node = self._balance_node(node)
        return balanced_node, is_intersecting

    def _delete_node(self, node: Node | None, line: Line) -> Node | None:
        """ Deletes a node within the AVL tree via recursion """
        # Primary case: empty node
        if node is None:
            return None

        # Tree Traversal
        order: int = self._compare_segments(line, node.line)

        # Moves left down the tree due to line having lower value
        if order == -1:
            node.left_child = self._delete_node(node.left_child, line)
        # Moves right down the tree due to line having higher value
        elif order == 1:
            node.right_child = self._delete_node(node.right_child, line)
        # Secondary Case: Deletion
        else:
            # Node with at most one child (0 or 1)
            if node.left_child is None:
                temp = node.right_child
                return temp
            elif node.right_child is None:
                temp = node.left_child
                return temp

            # Finds in-order successor (smallest in the right subtree)
            successor = self._min_node(node.right_child)

            # Swap data and then deletes the successor from right subtree
            node.line = successor.line
            node.right_child = self._delete_node(
                node.right_child, successor.line
            )

        node.height = 1 + max(
            self._node_height(node.left_child),
            self._node_height(node.right_child)
        )
        return self._balance_node(node)

    def _compare_segments(self, s1: Line, s2: Line) -> int:
        """
        Determines the horizontal order of two segments
        with respect to the sweep line
        """
        if s1 == s2:
            # If they are the same segment
            return 0

        # Calculates the x-value along the sweep line for both segments
        s1_x: float = _sweep_intersect(s1, self.current_sweep_y)
        s2_x: float = _sweep_intersect(s2, self.current_sweep_y)

        if isclose(s1_x, s2_x):
            # Line 1 and line 2 are intersecting
            return 0

        # Relative direction segments are heading
        if _get_dx_dy(s1) < _get_dx_dy(s2):
            return -1

        return 1

    def _rotate_right(self, node: Node) -> Node:
        """ Performs a right rotation on the unbalanced node """
        new_root = node.left_child
        # Sub tree between new_root and original node
        sub_tree = new_root.right_child

        # New root takes original node position, and
        # original becomes new root right child
        new_root.right_child = node

        # Subtree becomes node new left child
        node.left_child = sub_tree

        # Updates heights (Node is now a child node)
        node.height = 1 + max(
            self._node_height(node.left_child),
            self._node_height(node.right_child)
        )

        # Update heights (new root is now the new root)
        new_root.height = 1 + max(
            self._node_height(new_root.left_child),
            self._node_height(new_root.right_child)
        )
        return new_root

    def _rotate_left(self, node: Node) -> Node:
        """ Performs a left rotation on the unbalanced node """
        new_root = node.right_child
        # Sub tree between new_root and original node
        sub_tree = new_root.left_child

        # New root takes original node position, and
        # original becomes new root left child
        new_root.left_child = node

        # sub_tree becomes node new right child
        node.right_child = sub_tree

        # Updates heights (Node is now a child node)
        node.height = 1 + max(
            self._node_height(node.left_child),
            self._node_height(node.right_child)
        )

        # Update heights (new root is now the new root)
        new_root.height = 1 + max(
            self._node_height(new_root.left_child),
            self._node_height(new_root.right_child)
        )
        return new_root

    def _balance_node(self, node: Node) -> Node:
        """ Checks balance and performs necessary rotations """
        balance: int = self._balance_factor(node)

        # Left imbalance
        if balance < -1:
            left_child_balance: int = self._balance_factor(node.left_child)

            # Left-Left Rotation
            if left_child_balance <= 0:
                return self._rotate_right(node)
            # Left-Right Rotation
            else:
                node.left_child = self._rotate_left(node.left_child)
                return self._rotate_right(node)
        # Right imbalance
        elif balance > 1:
            right_child_balance = self._balance_factor(node.right_child)

            # Right-Right Rotation
            if right_child_balance >= 0:
                return self._rotate_left(node)
            # Right-Left Rotation
            else:
                node.right_child = self._rotate_right(node.right_child)
                return self._rotate_left(node)
        return node

    def _balance_factor(self, node: Node) -> int:
        """ Calculates the balance factor (right height - left height) """
        right = self._node_height(node.right_child)
        left = self._node_height(node.left_child)
        return right - left

    def _min_node(self, node: Node) -> Node:
        """ Finds the leftmost node in a subtree """
        current = node
        while current.left_child is not None:
            current = current.left_child
        return current

    def _node_height(self, node: Node | None) -> int:
        """ Returns the height of a node, or 0 if none """
        if not node:
            return 0
        return node.height
