from src.core.geometry import Shape


def ensure_exact_num_points(points: Shape, total_points: int) -> Shape:
    if len(points) > total_points:
        return points[:total_points]

    if len(points) < total_points:
        raise RuntimeError(
            f"Expected {total_points} points, got {len(points)}"
        )

    return points