"""Module with test for backend operations on the database of materials."""

import json
import multiprocessing
import os
from pathlib import Path
import shutil
import sys
import time
import pytest
import requests  # type: ignore[import-untyped]
import uvicorn
import uvicorn.server


@pytest.fixture
def database_directory():
    """
    Create a directory for test database during the setup,
    and return path to it; remove the directory during the teardown.
    """
    directory = Path('test_database')
    os.mkdir(directory)

    yield directory
    shutil.rmtree(directory)


@pytest.fixture()
def server_ip() -> str:
    """Fixture to provide IP of the server."""
    return '127.0.0.1'


@pytest.fixture()
def server_port() -> int:
    """Fixture to provide port of the server."""
    return 8000


@pytest.fixture
def mock_args(monkeypatch):
    """
    Simulate command-line arguments to prevent argparse from consuming
    pytest's arguments.
    """
    monkeypatch.setattr(
        sys, 'argv', ['knowledge_verificator', '-c', 'config.yaml']
    )


@pytest.fixture
def server(mock_args, database_directory, server_ip, server_port):
    """Set up and teardown the server with endpoints."""
    process = multiprocessing.Process(
        target=uvicorn.run,
        args=('knowledge_verificator.backend:ENDPOINTS',),
        kwargs={'host': server_ip, 'port': server_port, 'reload': True},
    )
    process.start()
    # Wait for a server to start up.
    time.sleep(2)

    yield

    process.terminate()
    time.sleep(2)
    process.kill()


def test_getting_empty_database(server, server_ip, server_port):
    """Test if the empty database returns no materials when requested."""
    url = f'http://{server_ip}:{server_port}/materials'
    response = requests.get(url=url, timeout=10)

    content = response.content.decode()
    content = json.loads(content)

    assert content['data'] == []
    assert content['message'] == []
