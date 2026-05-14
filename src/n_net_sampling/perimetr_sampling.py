import math

from src.core.geometry import Point, Shape


def sample_perimeter(polygon: Shape, N: int) -> Shape:

    if N <= 0:
        return []

    edges = []
    lengths = []
    total_length = 0.0

    n = len(polygon)

    for i in range(n):
        a = polygon[i]
        b = polygon[(i + 1) % n]

        dx = b.x - a.x
        dy = b.y - a.y
        length = math.hypot(dx, dy)

        edges.append((a, b, length))
        lengths.append(length)
        total_length += length

    if total_length == 0:
        return [polygon[0]] * N

    step = total_length / N

    result = []

    current_edge_idx = 0
    current_edge_pos = 0.0  
    dist_accum = 0.0        

    for k in range(N):
        target_dist = k * step

        while dist_accum + edges[current_edge_idx][2] < target_dist:
            dist_accum += edges[current_edge_idx][2]
            current_edge_idx += 1

        a, b, edge_len = edges[current_edge_idx]

        local_dist = target_dist - dist_accum

        t = local_dist / edge_len if edge_len > 0 else 0.0

        x = a.x + t * (b.x - a.x)
        y = a.y + t * (b.y - a.y)

        result.append(Point(x, y))

    return result