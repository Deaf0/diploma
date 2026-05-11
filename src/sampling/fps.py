import random

from src.core.geometry import Shape


def fps(points: Shape, n: int, rng: random.Random) -> Shape:
    if not points:
        return []

    n = min(n, len(points))

    first_idx = rng.randrange(len(points))
    selected = [points[first_idx]]
    
    distances = [float("inf")] * len(points)

    chosen = [False] * len(points)
    chosen[first_idx] = True

    for _ in range(1, n):
        last = selected[-1]

        for i, p in enumerate(points):
            if not chosen[i]:
                d = p.dist(last) 
                if d < distances[i]:
                    distances[i] = d
        
        best_dist = -1.0
        idx = -1
        for i, d in enumerate(distances):
            if not chosen[i] and d > best_dist:
                best_dist = d
                idx = i
        
        if idx == -1: 
            break
            
        selected.append(points[idx])
        chosen[idx] = True
        
    return selected