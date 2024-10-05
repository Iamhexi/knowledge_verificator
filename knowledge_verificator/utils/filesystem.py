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


def create_text_file(path: Path | str, content: str = '') -> None:
    """
    Create a text file in the supplied location.

    If no content is provided, an empty file is created.

    Args:
        path (Path | str): Location of a new file.
        content (str, optional): Content of a file. Defaults to ''.

    Raises:
        FileExistsError: Raised if a file already exists.
    """
    if isinstance(path, str):
        path = Path(path)

    if path.exists():
        raise FileExistsError(f'A file already exists under `{str(path)}`')

    with open(path.resolve(), 'wt', encoding='utf-8') as fd:
        fd.write(content)
