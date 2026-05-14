from typing import Tuple
from scipy.spatial import KDTree

from src.core.geometry import Point, Shape
from src.metrics.polygon_hausdorff import to_array, hausdorff_with_witness
from src.optimization.q0_init import initQ0
from src.optimization.hausdorff_grid_search import find_optimal_translation_grid
from src.optimization.shor_optimize import shor_optimize
from src.sampling.strategies import build_n_net, build_fps_net, build_jittered_raster_net
from src.sampling.config import SamplingConfig


def approximate_polygon(polygon: Shape, config: SamplingConfig) -> Shape:

    if config.method == "raster":
        return build_jittered_raster_net(
            polygon, 
            total_points=config.total_points, 
            boundary_ratio=config.boundary_ratio,
            samples_per_cell=config.samples_per_cell, 
            rng=config.rng
        )
    elif config.method == "fps":
        return build_fps_net(
            polygon, 
            total_points=config.total_points, 
            boundary_ratio=config.boundary_ratio, 
            rng=config.rng
        )
    elif config.method == "n_net":
        return build_n_net(
            polygon, 
            total_points=config.total_points, 
            boundary_ratio=config.boundary_ratio, 
            rng=config.rng
        )
    
    raise ValueError(f"Unknown method: {config.method}")


def compute_ground_truth(
    A: Shape, 
    B: Shape, 
    config: SamplingConfig,
    n_per_dim_q0: int=20
) -> Tuple[Point, float, Shape, Shape, list[float]]:
    
    A_dense = build_jittered_raster_net(
        A, 
        total_points=config.total_points, 
        boundary_ratio=config.boundary_ratio,
        samples_per_cell=config.samples_per_cell,
        rng=config.rng
    )   
    B_dense = build_jittered_raster_net(
        B, 
        total_points=config.total_points, 
        boundary_ratio=config.boundary_ratio,
        samples_per_cell=config.samples_per_cell,
        rng=config.rng
    )
 
    A_tree = KDTree(to_array(A_dense))
    B_tree = KDTree(to_array(B_dense))

    Q0 = initQ0(A, B)

    best_x, _, _ = find_optimal_translation_grid(
        A_dense, B_dense, A_tree, B_tree, Q0, n_per_dim_q0
    )

    x_star, H_true = shor_optimize(
        A_dense, B_dense, A_tree, B_tree, best_x
    )

    return x_star, H_true, A_dense, B_dense, Q0


def shift_polygon(polygon: Shape, dx: float, dy: float) -> Shape:
    return [Point(p.x + dx, p.y + dy) for p in polygon]


def hausdorff(A_pts: Shape, B_pts: Shape) -> float:
    A_tree = KDTree(to_array(A_pts))
    B_tree = KDTree(to_array(B_pts))
    val, _, _ = hausdorff_with_witness(A_pts, B_pts, A_tree, B_tree)
    return val
