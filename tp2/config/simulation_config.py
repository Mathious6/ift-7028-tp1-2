from dataclasses import dataclass, field
from typing import ClassVar, Dict


@dataclass
class SimulationConfig:

    SIMULATION_TIME: int = 40000
    RANDOM_SEED: ClassVar[int] = 42

    ROBOTs_MEAN_UNLOADING_TIMES: Dict[int, float] = field(
        default_factory=lambda: {
            2: 9.0,
            3: 7.0,
            5: 5.5,
            8: 4.5,
            12: 4.2,
        }
    )

    PLANES_MEAN_ARRIVAL_TIME: float = 12.3
