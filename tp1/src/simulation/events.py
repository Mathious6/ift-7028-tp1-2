# DOC: https://www.geeksforgeeks.org/heap-queue-or-heapq-in-python/
from dataclasses import dataclass
from typing import Callable, Any
import heapq
from enum import Enum, auto


class EventType(Enum):
    """Types of events that can occur in the simulation."""
    PLANE_ARRIVAL = auto()
    START_LOADING = auto()
    END_LOADING = auto()


@dataclass
class Event:
    """Represents an event in the simulation."""
    time: float  # When the event occurs
    type: EventType  # Type of event
    data: Any = None  # Additional data associated with the event
    callback: Callable = None  # Function to call when event occurs

    def __lt__(self, other):
        """Compare events by time for priority queue ordering."""
        return self.time < other.time


class EventQueue:
    """Manages events in chronological order using a priority queue."""

    def __init__(self):
        self._queue = []
        self._time = 0.0

    @property
    def current_time(self) -> float:
        """Get the current simulation time."""
        return self._time

    def schedule(self, event: Event) -> None:
        """Schedule a new event."""
        heapq.heappush(self._queue, event)

    def next_event(self) -> Event:
        """Get and remove the next event from the queue."""
        if not self._queue:
            raise IndexError("No more events in the queue")
        event = heapq.heappop(self._queue)
        self._time = event.time
        return event

    def has_events(self) -> bool:
        """Check if there are any events remaining."""
        return len(self._queue) > 0

    def clear(self) -> None:
        """Clear all events from the queue."""
        self._queue.clear()
        self._time = 0.0


if __name__ == "__main__":
    queue = EventQueue()

    queue.schedule(
        Event(time=10.0, type=EventType.PLANE_ARRIVAL, data="Plane 1"))
    queue.schedule(
        Event(time=5.0, type=EventType.START_LOADING, data="Plane 2"))
    queue.schedule(
        Event(time=15.0, type=EventType.END_LOADING, data="Plane 1"))

    print("Processing events in chronological order:")
    while queue.has_events():
        event = queue.next_event()
        print(f"Time {event.time:.1f}: {event.type.name} - {event.data}")
