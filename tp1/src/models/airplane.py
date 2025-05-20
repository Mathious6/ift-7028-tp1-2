from dataclasses import dataclass
from typing import Optional
from enum import Enum, auto


class PlaneStatus(Enum):
    """Status of a plane in the system."""
    WAITING = auto()
    BEING_SERVED = auto()
    UNLOADED = auto()


@dataclass
class AirPlane:
    """Represents an aircraft in the simulation."""
    id: int
    status: PlaneStatus = PlaneStatus.WAITING

    # TIMINGS:
    queue_entry_time: Optional[float] = None
    service_start_time: Optional[float] = None
    service_end_time: Optional[float] = None

    @property
    def waiting_time(self) -> float:
        """Calculate the time the plane spent waiting in queue."""
        return self.service_start_time - self.queue_entry_time

    @property
    def service_time(self) -> float:
        """Calculate the time the plane spent being served."""
        return self.service_end_time - self.service_start_time
