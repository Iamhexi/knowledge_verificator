"""Module with filesystem utility functions."""

from pathlib import Path


def in_directory(file: Path, directory: Path) -> bool:
    """
    Determine if a file is located in the supplied directory
    or one of its subdirectories.

    Args:
        file (Path): Path to a file.
        directory (Path): Path to a directory.

    Returns:
        bool: Present in a directory or subdirectories (True) or not (False).
    """
    return str(directory.resolve()) in str(
        file.resolve()
    ) and not file.samefile(directory)
