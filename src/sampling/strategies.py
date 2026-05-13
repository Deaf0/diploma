import random

from src.core.geometry import  Point, Shape
from src.sampling.boundary_sampling import sample_boundary
from src.sampling.point_generator import random_points_in_polygon
from src.sampling.fps import fps
from src.sampling.jittered_raster import raster_poly
from src.sampling.utils import ensure_exact_num_points


def build_fps_net(
    polygon: Shape, total_points: int, 
    boundary_ratio: float=0.3, 
    candidate_multiplier: int = 10,
    rng: random.Random | None = None
) -> Shape:

    k_boundary = int(total_points * boundary_ratio)
    k_inner = total_points - k_boundary

    boundary_pts = sample_boundary(polygon, k_boundary)
    candidates = raster_poly(polygon, candidate_multiplier  * k_inner, 1, rng)
    inner_pts = fps(candidates, k_inner, rng)
    result = boundary_pts + inner_pts

    return ensure_exact_num_points(result, total_points)


def build_jittered_raster_net(
    polygon: Shape, total_points: int, 
    boundary_ratio: float=0.3, 
    samples_per_cell: int = 1,
    rng: random.Random | None = None
) -> Shape:

    k_boundary = int(total_points * boundary_ratio)
    k_inner = total_points - k_boundary

    boundary_pts = sample_boundary(polygon, k_boundary)
    inner_pts = raster_poly(polygon, k_inner, samples_per_cell, rng)
    result = boundary_pts + inner_pts

    return ensure_exact_num_points(result, total_points)
