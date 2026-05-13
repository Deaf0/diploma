import math

from src.core.geometry import Point, Shape


def sample_boundary(polygon: Shape, N: int) -> Shape:
    if N <= 0:
        return []

    n = len(polygon)

    if n == 0:
        return []

    if n == 1:
        return [polygon[0].copy() for _ in range(N)]

    edges = []
    total_length = 0.0

    for i in range(n):
        a = polygon[i]
        b = polygon[(i + 1) % n]

        length = math.hypot(b.x - a.x, b.y - a.y)

        edges.append((a, b, length))
        total_length += length

    if total_length == 0:
        return [polygon[0].copy() for _ in range(N)]

    result = []

    current_edge_idx = 0
    accumulated = 0.0

    for k in range(N):
        target = ((k + 0.5) * total_length) / N

        while (
            current_edge_idx < len(edges) - 1
            and accumulated + edges[current_edge_idx][2] < target
        ):
            accumulated += edges[current_edge_idx][2]
            current_edge_idx += 1

        a, b, edge_len = edges[current_edge_idx]

        local_dist = target - accumulated

        if edge_len > 0:
            t = local_dist / edge_len
        else:
            t = 0.0

        x = a.x + t * (b.x - a.x)
        y = a.y + t * (b.y - a.y)

        result.append(Point(x, y))

    return result