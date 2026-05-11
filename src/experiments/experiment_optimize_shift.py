import random
from dataclasses import replace
from scipy.spatial import KDTree

from src.sampling.config import SamplingConfig
from src.core.geometry import Point, Shape
from src.metrics.polygon_hausdorff import to_array
from src.optimization.hausdorff_grid_search import find_optimal_translation_grid
from src.optimization.shor_optimize import shor_optimize
from src.experiments.common import (
    approximate_polygon, shift_polygon,
    hausdorff
)


def find_optimal_shift(A_pts: Shape, B_pts: Shape, Q0: list[float], steps: int=20) -> Point:
    A_tree = KDTree(to_array(A_pts))
    B_tree = KDTree(to_array(B_pts))

    x0, _, _ = find_optimal_translation_grid(
        A_pts, B_pts, A_tree, B_tree, Q0, steps
    )

    x_opt, _ = shor_optimize(
        A_pts, B_pts, A_tree, B_tree, x0
    )

    return x_opt


def evaluate_shift(A_dense: Shape, B_dense: Shape, x: Point) -> float: 
    B_shifted = shift_polygon(B_dense, x.x, x.y)
    return hausdorff(A_dense, B_shifted)
    

def run_single_case_exp2(
        A: Shape, 
        B: Shape, 
        config: SamplingConfig,
        Q0: list[float], 
        A_dense: Shape, 
        B_dense: Shape, 
        x_reference: Point, 
        H_reference: float
) -> dict:
    
    A_rng = random.Random(config.rng.randint(0, 10**9))
    B_rng = random.Random(config.rng.randint(0, 10**9))

    A_config = replace(config, rng=A_rng)
    B_config = replace(config, rng=B_rng)

    A_approx = approximate_polygon(A, A_config)
    B_approx = approximate_polygon(B, B_config)

    x_est = find_optimal_shift(A_approx, B_approx, Q0)

    H_est = evaluate_shift(A_dense, B_dense, x_est)

    return {
        "experiment": "optimize_shift",
        "method": config.method,
        "total_points": config.total_points,
        "H_reference": H_reference,
        "H_est": H_est,
        "x_err": (x_est - x_reference).norm(),
        "signed_H_err": H_est - H_reference,
        "abs_H_err": abs(H_est - H_reference)
    }
