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

    def is_unloaded_by(self, time: int) -> bool:
        """Check if the plane is unloaded by a given time."""
        return self.service_end_time is not None and self.service_end_time <= time

    @classmethod
    def count_unloaded_by_time(cls, planes: list["AirPlane"], time: int) -> int:
        """Count how many planes have been unloaded by a given time."""
        return sum(1 for plane in planes if plane.is_unloaded_by(time=time))

    @classmethod
    def calculate_mean_unloaded_rate(
        cls, planes: list["AirPlane"], time: int, window_size: int
    ) -> float:
        """Calculate the mean rate of planes unloaded up to a given time."""
        planes_unloaded = cls.count_unloaded_by_time(planes, time)
        windows_elapsed = time / window_size
        return planes_unloaded / windows_elapsed if windows_elapsed > 0 else 0

    @classmethod
    def calculate_queue_time_at_time(cls, planes: list["AirPlane"], time: int) -> float:
        """Calculate the total queue time for all planes up to a given time."""
        return sum(
            min(time, plane.service_start_time or time) - plane.queue_entry_time
            for plane in planes
            if plane.queue_entry_time is not None and plane.queue_entry_time <= time
        )

    @classmethod
    def calculate_mean_queue_length(cls, planes: list["AirPlane"], time: int) -> float:
        """Calculate the mean queue length up to a given time."""
        total_queue_time = cls.calculate_queue_time_at_time(planes, time)
        return total_queue_time / time if time > 0 else 0

    @classmethod
    def get_completed_planes_by_time(
        cls, planes: list["AirPlane"], time: int
    ) -> list["AirPlane"]:
        """Get list of planes that have completed service by a given time."""
        return [
            plane
            for plane in planes
            if plane.service_end_time is not None
            and plane.service_end_time <= time
            and plane.waiting_time is not None
        ]

    @classmethod
    def calculate_mean_waiting_time(cls, planes: list["AirPlane"], time: int) -> float:
        """Calculate the mean waiting time for planes completed by a given time."""
        completed_planes = cls.get_completed_planes_by_time(planes, time)
        if not completed_planes:
            return 0
        return sum(plane.waiting_time for plane in completed_planes) / len(
            completed_planes
        )

    @classmethod
    def calculate_total_service_time(cls, planes: list["AirPlane"], time: int) -> float:
        """Calculate the total service time for all planes up to a given time."""
        return sum(
            min(time, plane.service_end_time or time) - plane.service_start_time
            for plane in planes
            if plane.service_start_time is not None and plane.service_start_time <= time
        )

    @classmethod
    def calculate_mean_robot_utilization(cls, planes: list["AirPlane"], time: int) -> float:
        """Calculate the mean robot utilization rate up to a given time."""
        total_service_time = cls.calculate_total_service_time(planes, time)
        return total_service_time / time if time > 0 else 0
