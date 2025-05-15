from dataclasses import dataclass
import random
import time
from typing import Optional

from config.simulation import SimulationConfig


@dataclass
class Airplane:
    """Represents an airplane in the simulation."""

    def __init__(self):
        self.id = random.randint(100000000, 999999999)

