from dataclasses import dataclass, field
from typing import Dict


@dataclass
class SimulationConfig:
    """Configuration for the simulation."""
    SIMULATION_TIME: int = 40000
    CONFIDENCE_LEVEL: float = 0.95
    NUM_REPLICATIONS: int = 10

    # TIPS: use field(default_factory=lambda: {}) to initialize a dictionary with default values
    ROBOT_SCENARIOS: Dict[int, float] = field(default_factory=lambda: {
        2: 9.0,
        3: 7.0,
        5: 5.5,
        8: 4.5,
        12: 4.2
    })

    MEAN_ARRIVAL_TIME: float = 12.3
