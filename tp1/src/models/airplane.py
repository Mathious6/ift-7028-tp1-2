from dataclasses import dataclass
from typing import Optional


@dataclass
class Airplane:
    """Represents an airplane in the simulation."""
    id: int
    arrival_time: float
    service_start_time: Optional[float] = None
    service_end_time: Optional[float] = None
