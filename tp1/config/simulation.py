from dataclasses import dataclass
from typing import Dict, ClassVar
from src.random.distributions import ExponentialDistribution


class SimulationConfig:
    """Configuration for the simulation."""

    SIMULATION_TIME: ClassVar[int] = 40000
    MEAN_ARRIVAL_TIME: ClassVar[float] = 12.3
    RANDOM_SEED: ClassVar[int] = 42
    ROBOT_SCENARIOS: ClassVar[Dict[int, float]] = {
        2: 9.0,
        3: 7.0,
        5: 5.5,
        8: 4.5,
        12: 4.2,
    }

    def __init__(self, num_robots: int, mean_arrival_time: float = MEAN_ARRIVAL_TIME):
        self.num_robots = num_robots
        self.robot_processing_time = self.ROBOT_SCENARIOS[num_robots]
        self.mean_arrival_time = mean_arrival_time
