import pathlib
from pathlib import Path


def get_path() -> str:
    path_file = Path(pathlib.Path.cwd().parent, "manifest-ocean-407215-51b1854c7f81.json")
    return str(path_file)
