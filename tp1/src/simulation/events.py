from enum import Enum
from dataclasses import dataclass
from typing import Any


class EventType(Enum):
    """Types of events in the simulation."""
    PLANE_ARRIVAL = "plane_arrival"
    PLANE_SERVICE_START = "service_start"
    PLANE_SERVICE_END = "service_end"


@dataclass
class Event:
    """Represents a simulation event."""
    event_type: EventType
    time: float
    data: Any
