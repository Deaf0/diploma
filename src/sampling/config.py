from dataclasses import dataclass
import random


@dataclass
class SamplingConfig:
    method: str
    total_points: int

    boundary_ratio: float = 0.3
    samples_per_cell: int = 1

    rng: random.Random | None = None

    