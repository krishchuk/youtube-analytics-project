import pathlib
from pathlib import Path


def get_path() -> str:
    path_file = Path(pathlib.Path.cwd().parent, ".env")
    return str(path_file)
