import random
from shapely.geometry import Polygon as ShapePolygon, Point as ShapePoint, MultiPoint
from shapely.ops import voronoi_diagram, clip_by_rect
from shapely.errors import GEOSException
from typing import List

from src.core.geometry import Point, Shape, Polygon


def unique_points(points: List[Point], eps:float = 1e-8) -> List[Point]:
    unique = []
    for p in points:
        if not any((abs(p.x - q.x) < eps and abs(p.y - q.y) < eps) for q in unique):
            unique.append(p)
    return unique


def jitter_points(points: List[Point], rng: random.Random | None = None, eps:float = 1e-9) -> List[Point]:
    return [
        Point(
            p.x + rng.uniform(-eps, eps),
            p.y + rng.uniform(-eps, eps)
        )
        for p in points
    ]


def get_voronoi_cells_shapely(polygon: Shape, centers: List[Point], rng: random.Random | None = None) -> List[Polygon]:
    polygon_vertices = [(p.x, p.y) for p in polygon.vertices]
    polygon_shape = ShapePolygon(polygon_vertices)

    centers = unique_points(centers)
    centers = jitter_points(centers, rng)

    points_shape = [ShapePoint(c.x, c.y) for c in centers]
    points_multipoint = MultiPoint(points_shape)

    min_x, max_x, min_y, max_y = polygon_shape.bounds

    envelope = polygon_shape.buffer(max(max_x-min_x, max_y-min_y))
    try:
        voronoi_polys = voronoi_diagram(points_multipoint, envelope=envelope)
    except:
        centers = jitter_points(centers, rng, eps=1e-6)
        points_shape = [ShapePoint(c.x, c.y) for c in centers]
        points_multipoint = MultiPoint(points_shape)
        voronoi_polys = voronoi_diagram(points_multipoint, envelope=envelope)
    
    cells = []

    for center_idx, center in enumerate(centers):
        target_pt = ShapePoint(center.x, center.y)
        
        for poly in voronoi_polys.geoms:
            poly = poly.buffer(0)
            if poly.contains(target_pt) or poly.touches(target_pt):
                try:
                    intersection = poly.intersection(polygon_shape)
                except:
                    intersection = poly.buffer(0).intersection(polygon_shape.buffer(0))

                if intersection.is_empty:
                    cells.append(Polygon([]))
                elif intersection.geom_type == 'Polygon':
                    new_vertices = [Point(x, y) for x, y in intersection.exterior.coords[:-1]]
                    cells.append(Polygon(new_vertices))
                elif intersection.geom_type == 'MultiPolygon':
                    all_pts = []
                    for sub_poly in intersection.geoms:
                        for x, y in sub_poly.exterior.coords[:-1]:
                            all_pts.append(Point(x, y))
                    cells.append(Polygon(all_pts))
                break
                
    return cells