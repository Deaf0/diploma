import math
import random

from src.core.geometry import Point, Shape, BoundingBox


def point_in_polygon_xy(px: float, py: float, polygon: Shape) -> int:
    inside = False
    n = len(polygon)

    for i in range(n):
        a = polygon[i]
        b = polygon[(i + 1) % n]

        ax, ay = a.x, a.y
        bx, by = b.x, b.y

        cross = (px - ax) * (by - ay) - (py - ay) * (bx - ax)
        if abs(cross) < 1e-9:
            dot = (px - ax) * (px - bx) + (py - ay) * (py - by)
            if dot <= 1e-9:
                return -1

        if (ay > py) != (by > py):
            x_intersection = (bx - ax) * (py - ay) / (by - ay) + ax
            if px < x_intersection:
                inside = not inside

    return 1 if inside else 0


def raster_poly(
    polygon: Shape,
    total_points: int,
    samples_per_cell: int = 1,
    rng: random.Random | None = None
) -> Shape:

    n_per_dim = math.ceil(math.sqrt(total_points))

    bbox = BoundingBox(polygon)

    min_x, max_x = bbox.min.x, bbox.max.x
    min_y, max_y = bbox.min.y, bbox.max.y

    dx = (max_x - min_x) / n_per_dim
    dy = (max_y - min_y) / n_per_dim

    sub_dim = int(math.sqrt(samples_per_cell))

    if sub_dim * sub_dim != samples_per_cell:
        raise ValueError(
            "samples_per_cell must be perfect square"
        )

    sub_dx = dx / sub_dim
    sub_dy = dy / sub_dim

    result = []

    for i in range(n_per_dim):
        for j in range(n_per_dim):

            cell_x = min_x + i * dx
            cell_y = min_y + j * dy

            for si in range(sub_dim):
                for sj in range(sub_dim):

                    x0 = cell_x + si * sub_dx
                    y0 = cell_y + sj * sub_dy

                    x = x0 + rng.random() * sub_dx
                    y = y0 + rng.random() * sub_dy

                    if point_in_polygon_xy(x, y, polygon) != 0:
                        result.append(Point(x, y))

    if len(result) >= total_points:
        rng.shuffle(result)
        return result[:total_points]

    remaining = total_points - len(result)

    max_attempts = max(1000, remaining * 100)

    attempts = 0

    while len(result) < total_points and attempts < max_attempts:
        x = rng.uniform(min_x, max_x)
        y = rng.uniform(min_y, max_y)

        if point_in_polygon_xy(x, y, polygon) != 0:
            result.append(Point(x, y))

        attempts += 1

    if len(result) < total_points:
        raise RuntimeError(
            f"Could not generate {total_points} points "
            f"inside polygon after {max_attempts} attempts. "
            f"Generated only {len(result)}."
        )

    return result


