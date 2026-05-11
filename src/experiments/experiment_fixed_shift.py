import random
from dataclasses import replace

from src.sampling.config import SamplingConfig
from src.core.geometry import Point, Shape
from src.experiments.common import (
    approximate_polygon, shift_polygon,
    hausdorff
)


def calculate_hausdorff_metric(A_pts: Shape, B_pts: Shape, x_reference: Point) -> float:
    B_pts_shifted = shift_polygon(B_pts, x_reference.x, x_reference.y)
    return hausdorff(A_pts, B_pts_shifted)


def run_single_case_exp1(
        A: Shape, 
        B: Shape, 
        config: SamplingConfig,
        x_reference: Point, 
        H_reference: float
) -> dict:

    A_rng = random.Random(config.rng.randint(0, 10**9))
    B_rng = random.Random(config.rng.randint(0, 10**9))

    A_config = replace(config, rng=A_rng)
    B_config = replace(config, rng=B_rng)

    A_approx = approximate_polygon(A, A_config)
    B_approx = approximate_polygon(B, B_config)
    
    H_est = calculate_hausdorff_metric(
        A_approx, 
        B_approx, 
        x_reference
    )

    return {
        "experiment": "fixed_shift",
        "method": config.method,
        "total_points": config.total_points,
        "H_reference": H_reference,
        "H_est": H_est,
        "signed_H_err": H_est - H_reference,
        "abs_H_err": abs(H_est - H_reference)
    }



