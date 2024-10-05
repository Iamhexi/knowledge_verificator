"""Module with tests for filesystem utils."""

from pathlib import Path
import pytest

from knowledge_verificator.utils.filesystem import in_directory


@pytest.mark.code_quality
@pytest.mark.parametrize(
    'directory, file, exists_there',
    (
        ('knowledge_verificator', 'knowledge_verificator/main.py', True),
        ('knowledge_verificator', 'tests/test_filesystem_utils.py', False),
        (
            'knowledge_verificator',
            'knowledge_verificator/utils/filesystem.py',
            True,
        ),
        ('knowledge_verificator', 'knowledge_verificator', False),
    ),
)
def test_in_directory(file: str, directory: str, exists_there: bool):
    """
    Test if a function determining if a file is located inside a directory
    or one of its subdirectories works properly.
    """
    assert (
        in_directory(file=Path(file), directory=Path(directory)) == exists_there
    )
