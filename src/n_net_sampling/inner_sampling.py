import random   

from src.core.geometry import Point, Polygon, Shape
from src.n_net_sampling.clipping import get_voronoi_cells_shapely
from src.n_net_sampling.min_enclosing_circle import get_minimum_enclosing_circle
from src.n_net_sampling.hausdorff_discrete import hausdorff_with_witness


def update_centers(cells: Shape, old_centers: Shape, rng: random.Random | None = None) -> Shape:
    new_centers = []

    for i, cell in enumerate(cells):
        if not cell.vertices:
            new_centers.append(old_centers[i])
            continue

        center, _ = get_minimum_enclosing_circle(cell.vertices, rng)
        new_centers.append(center)

    return new_centers


def make_one_iteration(polygon: Polygon, centers: Shape, rng: random.Random | None = None) -> Shape:
    cells = get_voronoi_cells_shapely(polygon, centers, rng)
    new_centers = update_centers(cells, centers, rng)
    return new_centers


def solve(
        polygon: Polygon,
        centers: Shape,
        rng: random.Random | None = None,
        max_iter: int = 50,
        eps: float = 1e-3
) -> Shape:
    prev_dist = float("inf")

    for i in range(max_iter):
        new_centers = make_one_iteration(polygon, centers, rng)

        hausdorff_dist, _ = hausdorff_with_witness(polygon, new_centers)

        if abs(prev_dist - hausdorff_dist) <= eps:
            # print("Converged")
            break 
        
        centers = new_centers
        prev_dist = hausdorff_dist

    return centers