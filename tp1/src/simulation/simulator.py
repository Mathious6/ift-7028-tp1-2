from tp1.src.simulation.events import Event, EventQueue, EventType
from typing import Callable


class Simulator:
    """Generic discrete event simulator."""

    def __init__(self):
        """Initialize the simulator."""
        self.event_queue = EventQueue()
        self.current_time = 0.0
        self.event_handlers = {}  # {EventType: Callable[[Event], None]}

    def register_handler(self, event_type: EventType, handler: Callable[[Event], None]) -> None:
        """Register an event handler for a specific event type."""
        self.event_handlers[event_type] = handler

    def schedule(self, event: Event) -> None:
        """Schedule a new event."""
        self.event_queue.schedule(event)

    def get_current_time(self) -> float:
        """Get the current simulation time."""
        return self.current_time

    def run(self, max_time: float) -> None:
        """Run the simulation until max_time is reached."""
        while self.event_queue.has_events():
            # DEBUG TIP: Breakpoint here to see the events in the queue
            event = self.event_queue.next_event()

            # This avoid to process events that are after the max_time
            if event.time > max_time:
                break

            self.current_time = event.time
            if event.type in self.event_handlers:
                self.event_handlers[event.type](event)
