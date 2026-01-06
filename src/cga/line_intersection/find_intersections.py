"""
Filename: find_intersections.py
Author: William Bowley
Version: 0.1
Date: 2025-11-02

Description:
    Implementation of FindIntersections
    algorithm described in chapter 2.

    This algorithm has a time complexity of
    O((n+k)log(n)), where k is the size of output
    and n is the size of input. This is a output
    sensitive algorithm
"""

from cga.primitives.definitions import Line, Point
from cga.primitives.get_intersection import get_intersection

from cga.line_intersection.event_queue import EventQueue, EventType, Node
from cga.line_intersection.status_tree import StatusStructure


def _normalize_line(line: Line) -> Line:
    """ Normalizes the lines to ensure start is the higher point """
    if line.start.y < line.end.y:
        return Line(line.end, line.start)

    if line.start.y == line.end.y and line.start.x > line.end.x:
        return Line(line.end, line.start)

    return line


def _add_upper_segment_points(
    queue: EventQueue,
    segments: list[Line]
) -> EventQueue:
    """ Adds the upper & lower endpoint of the segments to the queue """

    # Enqueues the upper endpoint of all segments
    for segment in segments:
        upper_endpoint = segment.start
        queue.enqueue(upper_endpoint, EventType.UPPER, segment)

    # Enqueues the lower endpoint of all segments
    for segment in segments:
        lower_endpoint = segment.end
        queue.enqueue(lower_endpoint, EventType.LOWER, segment)

    return queue


def _find_new_event(
    queue: EventQueue, left_segment: Line, right_segment: Line, event: Point
) -> None:
    """ Finds a new event point and enqueue its """
    # Tries to find intersection, returns none if not found
    point = get_intersection(left_segment, right_segment)

    if point:
        # Check: Only add if its below the current event point (sweep line)
        if point.y < event.y or (point.y == event.y and point.x > event.x):
            queue.enqueue(point, EventType.INTERIOR, left_segment)
            queue.enqueue(point, EventType.INTERIOR, right_segment)


def _handle_event_point(
    event: Point, current_event: list[Node],
    status: StatusStructure, queue: EventQueue
) -> list[Point]:
    """ Handles an event point """
    intersections: list[Point] = []

    upper = []      # Upper endpoints
    lower = []      # Lower endpoints
    interior = []   # Interior endpoints

    for node in current_event:
        # Creates subsets U(p), L(p), C(p)
        match node.event_type:
            case EventType.UPPER:
                upper.append(node.line)
            case EventType.LOWER:
                lower.append(node.line)
            case EventType.INTERIOR:
                interior.append(node.line)
            case _:
                msg = f"Heap has been corrupted, {node.event_type} is unknown"
                raise RuntimeError(msg)

    # Takes the union of upper, lower, interior
    segment_union = set(upper) | set(lower) | set(interior)

    if len(segment_union) > 1:
        intersections.append(event)

    # Deletes upper and interior segments from status structure
    for segment in interior:
        status.delete(segment)
    for segment in lower:
        status.delete(segment)

    # Inserts the union of upper and interior into status structure
    for segment in (set(upper) | set(interior)):
        status.insert(segment)

        # Checks if the newly inserted segment has any event points
        left, right = status.find_neighbors(segment)
        if left:
            _find_new_event(queue, left, segment, event)
        if right:
            _find_new_event(queue, segment, right, event)

    # If the union of upper and interior is an empty set
    if not (upper or interior):
        left, right = status.find_neighbors_at_point(event)

        if left and right:
            _find_new_event(queue, left, right, event)
    else:
        # Finds the leftmost segment of the set upper union interior
        leftmost = status.get_leftmost_segment_of_group(
            upper + interior
        )

        # Finds the left neighbor of leftmost in the status structure
        double_left, _ = status.find_neighbors(leftmost)

        if leftmost and double_left:
            _find_new_event(queue, double_left, leftmost, event)

        # Finds the rightmost segment of the set upper union interior
        rightmost = status.get_rightmost_of_group(
            upper + interior
        )

        # Finds the right neighbor of rightmost in the status structure
        _, double_right = status.find_neighbors(rightmost)

        if rightmost and double_right:
            _find_new_event(queue, double_right, rightmost, event)

    return intersections


def find_intersections(
    segments: list[Line]
) -> list[tuple[Point, Line]]:
    """
    Finds intersection points of a set of line segments in
    a plane. Returns the point and segment that contained it
    """
    # Intersection list
    intersections: list[tuple[Point, Line]] = []

    # Initializes the event queue and adds the segments
    queue = EventQueue()
    segments = [_normalize_line(s) for s in segments]
    _add_upper_segment_points(queue, segments)

    # # Initialize the status structure as empty
    status = StatusStructure()
    while queue.number_items > 0:
        event = queue.dequeue()

        # Collects all other events at this point
        current_events = [event]
        while queue.peek_point() == event.point:
            current_events.append(queue.dequeue())

        # Updates sweep line with event point y
        status.update_sweep_line(event.point.y)

        # Handles the event point from the heap
        new_intersection = _handle_event_point(
            event.point, current_events, status, queue
        )

        intersections.extend(new_intersection)

    return intersections


simple_test = [
    Line(Point(5, 10), Point(0, 0)),
    Line(Point(5, 10), Point(10, 0))
]

found = find_intersections(simple_test)
print(f"Found {len(found)} intersection(s):")
for pt in found:
    print(f"({pt.x}, {pt.y})")
