from src.core.geometry import Polygon, Shape, get_point_on_segment
from src.n_net_sampling.hausdorff_discrete import generate_samples


def init_centers(polygon: Polygon, k: int) -> Shape:
    samples = generate_samples(polygon, k)
    return [get_point_on_segment(polygon, s) for s in samples]