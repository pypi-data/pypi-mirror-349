from pathlib import Path


def read(path: str) -> str:
    """
    Reads the file at `path` and return contents as a string

    Args:
        path: path to the file to read

    Returns:
        File contents as a string
    """
    return Path(path).read_text()
