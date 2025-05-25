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

    # QUEUE:
    queue_length: int = 0

    @property
    def waiting_time(self) -> float:
        """Calculate the time the plane spent waiting in queue."""
        return self.service_start_time - self.queue_entry_time

    @property
    def service_time(self) -> float:
        """Calculate the time the plane spent being served."""
        return self.service_end_time - self.service_start_time

    def is_unloaded_by(self, time: int) -> bool:
        """Check if the plane is unloaded by a given time."""
        return self.service_end_time is not None and self.service_end_time <= time

    @classmethod
    def count_unloaded_by_time(cls, planes: list["AirPlane"], start_time: int, end_time: int) -> int:
        """Count how many planes have been unloaded between start_time and end_time."""
        return sum(1 for plane in planes if plane.is_unloaded_by(time=end_time) and plane.service_end_time >= start_time)

    @classmethod
    def calculate_mean_unloaded_rate(cls, planes: list["AirPlane"], start_time: int, end_time: int, window_size: int) -> float:
        """Calculate the mean rate of planes unloaded between start_time and end_time."""
        planes_unloaded = cls.count_unloaded_by_time(planes, start_time, end_time)
        windows_elapsed = (end_time - start_time) / window_size
        return planes_unloaded / windows_elapsed if windows_elapsed > 0 else 0

    @classmethod
    def calculate_mean_queue_length(cls, planes: list["AirPlane"], start_time: int, end_time: int) -> float:
        """Calculate the mean number of planes in queue between start_time and end_time."""
        relevant_planes = [p for p in planes if start_time <= p.queue_entry_time <= end_time]
        if not relevant_planes:
            return 0
        return sum(p.queue_length for p in relevant_planes) / len(relevant_planes)

    @classmethod
    def get_completed_planes_by_time(cls, planes: list["AirPlane"], start_time: int, end_time: int) -> list["AirPlane"]:
        """Get list of planes that have completed service between start_time and end_time."""
        return [
            plane
            for plane in planes
            if (plane.service_end_time is not None
                and start_time <= plane.service_end_time <= end_time
                and plane.waiting_time is not None)
        ]

    @classmethod
    def calculate_mean_waiting_time(cls, planes: list["AirPlane"], start_time: int, end_time: int) -> float:
        """Calculate the mean waiting time for planes completed between start_time and end_time."""
        completed_planes = cls.get_completed_planes_by_time(planes, start_time, end_time)
        if not completed_planes:
            return 0
        return sum(plane.waiting_time for plane in completed_planes) / len(completed_planes)

    @classmethod
    def calculate_total_service_time(cls, planes: list["AirPlane"], start_time: int, end_time: int) -> float:
        """Calculate the total service time for all planes between start_time and end_time."""
        return sum(
            min(end_time, plane.service_end_time or end_time) - max(start_time, plane.service_start_time or start_time)
            for plane in planes
            if (plane.service_start_time is not None
                and plane.service_start_time <= end_time
                and (plane.service_end_time is None or plane.service_end_time >= start_time))
        )

    @classmethod
    def calculate_mean_robot_utilization(cls, planes: list["AirPlane"], start_time: int, end_time: int) -> float:
        """Calculate the mean robot utilization rate between start_time and end_time."""
        total_service_time = cls.calculate_total_service_time(planes, start_time, end_time)
        period_duration = end_time - start_time
        return total_service_time / period_duration if period_duration > 0 else 0
