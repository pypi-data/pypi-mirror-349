import os
from pathlib import Path


def get_file_kind(path: str | Path):
    return os.path.splitext(str(path))[1][1:]
