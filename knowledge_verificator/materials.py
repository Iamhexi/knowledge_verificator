"""Module with tools for managing learning material."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Material:
    """
    Data class representing a learning material loaded from a database.
    """

    path: Path
    title: str
    paragraphs: list[str]
    tags: list[str]


class MaterialDatabase:
    """Class managing a database with learning materials."""

    def __init__(self, materials_dir: Path | str) -> None:
        """
        Load all learning materials from `material_dir` directory
        into an internal storage.

        Args:
            materials_dir (Path | str): Path to directory with learning materials.

        Raises:
            FileNotFoundError: Raised if supplied path to a directory does not exist.
        """
        if isinstance(materials_dir, str):
            materials_dir = Path(materials_dir)

        materials_dir = materials_dir.resolve()
        if not materials_dir.exists():
            raise FileNotFoundError(
                f'There is no directory under `{materials_dir}`.'
            )

        self.materials: list[Material] = []
        for directory_path, _, filenames in materials_dir.walk():
            for filename in filenames:
                path = Path(directory_path).joinpath(filename)
                material = self.load_material(path)
                self.materials.append(material)

    def load_material(self, path: Path) -> Material:
        """
        Load a learning material from a file.

        Args:
            path (Path): Path to a learning material.

        Returns:
            Material: Learning material loaded from the file.
        """
        with open(path.resolve(), 'rt', encoding='utf-8') as fd:
            title = fd.readline().rstrip()
            fd.readline()
            tags_line = fd.readline()
            tags = [tag.strip() for tag in tags_line.split(',')]
            tags_line = fd.readline()

            content = ''.join(fd.readlines()).rstrip()
            paragraphs = content.split('\n\n')

            return Material(
                path=path.resolve(),
                title=title,
                paragraphs=paragraphs,
                tags=tags,
            )
