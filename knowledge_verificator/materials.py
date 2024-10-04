"""Module with tools for managing learning material."""

from dataclasses import dataclass
import os
from pathlib import Path

from knowledge_verificator.utils.filesystem import in_directory


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

        self.materials_dir = materials_dir.resolve()
        if not self.materials_dir.exists():
            raise FileNotFoundError(
                f'There is no directory under `{self.materials_dir}`.'
            )

        self.materials: list[Material] = []
        for directory_path, _, filenames in self.materials_dir.walk():
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

    def add_material(self, material: Material) -> None:
        """
        Add a learning material to a database, also material's its
        representation  in a file.

        Args:
            material (Material): Initialised learning material without
                existing file representation.

        Raises:
            ValueError: Raised if title of a learning material is empty.
            FileExistsError: Raised if learning material in a supplied
                path already exists.
            ValueError: Raised if a supplied path path is outside the
                directory for learning materials.
        """
        if not material.title:
            raise ValueError('Title of a learning material cannot be empty.')
        if material.path.exists():
            raise FileExistsError(
                'A file in the provided path already exists. '
                'Choose a different filename.'
            )
        if not in_directory(file=material.path, directory=self.materials_dir):
            raise ValueError(
                f'A file {os.path.basename(material.path)}'
                f' has to be in {self.materials_dir}'
            )
        self._create_file_with_material(material=material)
        self.materials.append(material)

    def _format_file_content(self, material: Material) -> str:
        output = ''
        # Format a title.
        output += material.title
        output += '\n---\n'

        # Format tags.
        tags_line = ', '.join('tags')
        output += tags_line + '\n'

        # Format content.
        content_lines = '\n\n'.join(material.paragraphs)
        output += content_lines + '\n\n'

        return output

    def _create_file_with_material(self, material: Material) -> None:
        with open(material.path, 'wt', encoding='utf-8') as fd:
            file_content = self._format_file_content(material=material)
            fd.write(file_content)
