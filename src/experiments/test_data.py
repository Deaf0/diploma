import random
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


def get_pair_polygons(base_path: Path, rng: random.Random) -> dict:

    folders = get_dataset_folders(base_path)

    convex_folder = rng.choice(folders)
    nonconvex_folder = rng.choice(folders)

    convex_polygon = get_polygon(convex_folder, "convex")
    nonconvex_polygon = get_polygon(nonconvex_folder, "nonconvex")

    return {
        "A": convex_polygon, 
        "B": nonconvex_polygon,
        "A_name": convex_folder.name,
        "B_name": nonconvex_folder.name
    } 

