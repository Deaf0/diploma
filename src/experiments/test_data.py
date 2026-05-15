import random
from itertools import combinations
from pathlib import Path

from src.core.geometry import Point, Shape


def extract_polygon_from_file(file_path: Path) -> Shape:
    polygon = []
    
    with open(file_path, "r") as file:
        file.readline()

        for line in file:
            x, y = map(float, line.strip().split())
            polygon.append(Point(x, y))
   
    return polygon


def get_polygon(folder_path: Path, polygon_type: str) -> Shape:
    pattern = f"*_polygon_{polygon_type}.txt"

    try:
        file_name = next(folder_path.glob(pattern))
    except StopIteration:
         raise FileNotFoundError(f"{polygon_type} polygon not found in {folder_path}")

    return extract_polygon_from_file(file_name)


def get_dataset_folders(base_path: Path) -> list[Path]:
    folders = [f for f in base_path.iterdir() if f.is_dir()]
    folders.sort()

    if not folders:
        raise ValueError("Dataset is empty")
    
    return folders


def build_unique_pairs(base_path: Path) -> list[dict]:
    folders = get_dataset_folders(base_path)

    pairs = []

    for folder_a, folder_b in combinations(folders, 2):

        polygon_a = get_polygon(folder_a, "convex")
        polygon_b = get_polygon(folder_b, "nonconvex")

        pairs.append({
            "A": polygon_a,
            "B": polygon_b,
            "A_name": folder_a.name,
            "B_name": folder_b.name
        })

    return pairs 

