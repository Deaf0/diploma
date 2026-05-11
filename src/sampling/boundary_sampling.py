import math
from src.core.geometry import Point, Shape


def sample_boundary(polygon: Shape, N: int) -> Shape:
    if N <= 0:
        return []

    n = len(polygon)

    if n == 0:
        return []

    if n == 1:
        return [polygon[0]] * N

    if N <= n:
        return polygon[:N]

    edges = []
    total_length = 0.0

    for i in range(n):
        a = polygon[i]
        b = polygon[(i + 1) % n]

        length = math.hypot(b.x - a.x, b.y - a.y)

        edges.append((a, b, length))
        total_length += length

    if total_length == 0:
        return [polygon[0]] * N

    result = [p.copy() for p in polygon]

    extra_points = N - n

    step = total_length / extra_points

    current_edge_idx = 0
    dist_accum = 0.0

    for k in range(extra_points):
        target_dist = (k + 0.5) * step

        while (
            current_edge_idx < len(edges) - 1
            and dist_accum + edges[current_edge_idx][2] < target_dist
        ):
            dist_accum += edges[current_edge_idx][2]
            current_edge_idx += 1

        a, b, edge_len = edges[current_edge_idx]

        local_dist = target_dist - dist_accum

        if edge_len > 0:
            t = local_dist / edge_len
        else:
            t = 0.0

        x = a.x + t * (b.x - a.x)
        y = a.y + t * (b.y - a.y)

        result.append(Point(x, y))

    return result