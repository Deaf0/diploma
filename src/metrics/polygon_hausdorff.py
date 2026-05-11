from scipy.spatial import KDTree
from typing import List, Tuple

from src.core.geometry import Point, Shape


def to_array(polygon: Shape) -> List:
    return [(point.x, point.y) for point in polygon]


def hausdorff_with_witness(
    A: Shape, 
    B: Shape, 
    tree_A: KDTree, 
    tree_B: KDTree, 
    shift: Point = None
) -> Tuple[float, Tuple[Point, Point], str]:
    max_dist = 0.0
    witness = None
    source = None

    if shift is not None:
        sx, sy = shift.x, shift.y
    else:
        sx, sy = 0, 0

    for a in A:
        query_point = (a.x - sx, a.y - sy)
        dist, idx = tree_B.query(query_point)
        b = B[idx]

        b_shifted = Point(b.x + sx, b.y + sy)

        if dist > max_dist:
            max_dist = dist
            witness = (a, b_shifted)
            source = "A_to_B"

    for b in B:
        b_shifted = Point(b.x + sx, b.y + sy)
        query_point = (b_shifted.x, b_shifted.y)

        dist, idx = tree_A.query(query_point)
        a = A[idx]

        if dist > max_dist:
            max_dist = dist
            witness = (a, b_shifted)
            source = "B_to_A"
    
    return max_dist, witness, source


