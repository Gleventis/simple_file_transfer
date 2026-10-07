"""contains helper methods for cleaning up"""

from pathlib import Path


def clean(path: str) -> None:
    """helper method for deleting files

    Args:
        path: the path of the file to be deleted
    """
    Path(path).unlink(missing_ok=True)
