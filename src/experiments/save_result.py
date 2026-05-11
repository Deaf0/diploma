import csv
from pathlib import Path


class ResultCSVWriter:
    def __init__(self, path: str, fieldnames: list[str]):
        self.path = Path(path)

        self.path.parent.mkdir(parents=True, exist_ok=True)

        self.file = open(self.path, "w", newline="", encoding="utf-8")

        self.writer = csv.DictWriter(
            self.file,
            fieldnames=fieldnames
        )

        self.writer.writeheader()

    def write(self, row: dict):
        self.writer.writerow(row)

    def close(self):
        self.file.close()