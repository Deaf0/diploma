from src.core.geometry import Polygon, Shape, get_point_on_segment
from src.n_net_sampling.hausdorff_discrete import generate_samples
from src.n_net_sampling.inner_sampling import solve
from src.n_net_sampling.perimetr_sampling import sample_perimeter


def init_centers(polygon: Polygon, k: int) -> Shape:
    samples = generate_samples(polygon, k)
    return [get_point_on_segment(polygon, s) for s in samples]


def build_net(polygon: Shape, N: int, proportional_coef: float=0.6) -> Shape:
    N_boundary = int(N * proportional_coef)
    N_interior = N - N_boundary

    centers = init_centers(Polygon(polygon), N_interior)

    boundary_pts = sample_perimeter(polygon, N_boundary)
    inner_pts = solve(Polygon(polygon), centers)

    return boundary_pts + inner_pts

