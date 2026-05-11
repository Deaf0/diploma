from shapely.geometry import Point as ShapelyPoint
from shapely.geometry import Polygon as ShapelyPolygon
import random

from src.core.geometry import Shape, Point


def random_points_in_polygon(polygon: Shape, k: int, rng: random.Random | None = None) -> Shape:

    poly = ShapelyPolygon([(p.x, p.y) for p in polygon])

    minx, miny, maxx, maxy = poly.bounds

    points = []

    max_attempts = k * 100
    attempts = 0

    while len(points) < k and attempts < max_attempts:
        x = rng.uniform(minx, maxx)
        y = rng.uniform(miny, maxy)

        if poly.covers(ShapelyPoint(x, y)):
            points.append(Point(x, y))

        attempts += 1
    
    if len(points) < k:
        raise RuntimeError(
            f"Could not generate {k} points "
            f"inside polygon after {max_attempts} attempts. "
            f"Generated only {len(points)}."
        )

    return points