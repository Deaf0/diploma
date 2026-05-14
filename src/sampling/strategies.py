import random

from src.core.geometry import  Polygon, Shape
from src.sampling.boundary_sampling import sample_boundary
from src.sampling.point_generator import random_points_in_polygon
from src.sampling.fps import fps
from src.sampling.jittered_raster import raster_poly
from src.sampling.utils import ensure_exact_num_points
from src.n_net_sampling.utils import init_centers
from src.n_net_sampling.inner_sampling import solve


def build_n_net(
    polygon: Shape, 
    total_points: int, 
    boundary_ratio: float=0.3, 
    rng: random.Random | None = None
) -> Shape:
    
    k_boundary = int(total_points * boundary_ratio)
    k_inner = total_points - k_boundary

    centers = init_centers(Polygon(polygon), k_inner)

    boundary_pts = sample_boundary(polygon, k_boundary)
    inner_pts = solve(Polygon(polygon), centers, rng)
    result = boundary_pts + inner_pts

    return ensure_exact_num_points(result, total_points)


def build_fps_net(
    polygon: Shape, 
    total_points: int, 
    boundary_ratio: float=0.3, 
    rng: random.Random | None = None
) -> Shape:

    k_boundary = int(total_points * boundary_ratio)
    k_inner = total_points - k_boundary

    boundary_pts = sample_boundary(polygon, k_boundary)
    candidates = random_points_in_polygon(polygon, k_inner, rng)
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
