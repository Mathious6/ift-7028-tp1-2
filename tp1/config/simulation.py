from dataclasses import dataclass, field
from typing import Dict


@dataclass
class SimulationConfig:
    """Configuration for the simulation."""
    SPEED_TIME_FACTOR: int = 1000
    SIMULATION_TIME: int = 40000 * SPEED_TIME_FACTOR
    CONFIDENCE_LEVEL: float = 0.95
    NUM_REPLICATIONS: int = 10

    # TIPS: use field(default_factory=lambda: {}) to initialize a dictionary with default values
    ROBOT_SCENARIOS: Dict[int, float] = field(default_factory=lambda: {
        2: 9.0 * SimulationConfig.SPEED_TIME_FACTOR,
        3: 7.0 * SimulationConfig.SPEED_TIME_FACTOR,
        5: 5.5 * SimulationConfig.SPEED_TIME_FACTOR,
        8: 4.5 * SimulationConfig.SPEED_TIME_FACTOR,
        12: 4.2 * SimulationConfig.SPEED_TIME_FACTOR
    })

    MEAN_ARRIVAL_TIME: float = 12.3 * SPEED_TIME_FACTOR
