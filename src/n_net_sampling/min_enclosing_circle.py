import random
from typing import Tuple, List

from src.core.geometry import Point


EPS = 1e-9


def is_in_circle(p: Point, c: Point, r: float) -> bool:
    return (p - c).norm() <= r + EPS


def circle_from_1(p: Point) -> Tuple[Point, float]:
    return p, 0.0


def circle_from_2(a: Point, b: Point) -> Tuple[Point, float]:
    center = (a + b) * 0.5
    radius = (a - center).norm()
    return center, radius


def circle_from_3(a: Point, b: Point, c: Point) -> Tuple[Point, float]:
    determinant = 2 * (
        a.x * (b.y - c.y) +
        b.x * (c.y - a.y) +
        c.x * (a.y - b.y)
    )

    if abs(determinant) < EPS:
        return None, None

    ux = (
        (a.x**2 + a.y**2) * (b.y - c.y) +
        (b.x**2 + b.y**2) * (c.y - a.y) +
        (c.x**2 + c.y**2) * (a.y - b.y)
    ) / determinant

    uy = (
        (a.x**2 + a.y**2) * (c.x - b.x) +
        (b.x**2 + b.y**2) * (a.x - c.x) +
        (c.x**2 + c.y**2) * (b.x - a.x)
    ) / determinant

    center = Point(ux, uy)
    radius = (center - a).norm()

    return center, radius


def trivial_circle(R: List[Point]) -> Tuple[Point, float]:
    if not R:
        return Point(0, 0), 0.0
    if len(R) == 1:
        return circle_from_1(R[0])
    if len(R) == 2:
        return circle_from_2(R[0], R[1])

    c, r = circle_from_3(R[0], R[1], R[2])
    if c is not None:
        return c, r

    best = None
    best_r = float("inf")

    for i in range(3):
        for j in range(i + 1, 3):
            c2, r2 = circle_from_2(R[i], R[j])
            if all(is_in_circle(p, c2, r2) for p in R):
                if r2 < best_r:
                    best = (c2, r2)
                    best_r = r2

    return best


def welzl(points: List[Point], R: List[Point]) -> Tuple[Point, float]:
    if not points or len(R) == 3:
        return trivial_circle(R)

    p = points.pop()

    c, r = welzl(points, R)

    if is_in_circle(p, c, r):
        points.append(p)
        return c, r

    R.append(p)
    c, r = welzl(points, R)
    R.pop()
    points.append(p)

    return c, r


def get_minimum_enclosing_circle(points: List[Point], rng: random.Random | None = None) -> Tuple[Point, float]:
    pts = points.copy()
    rng.shuffle(pts)
    return welzl(pts, [])