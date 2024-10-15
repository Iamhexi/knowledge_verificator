"""Module with test for backend operations on the database of materials."""

import json
import multiprocessing
import os
from pathlib import Path
import shutil
import sys
import time
from typing import Any
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
    temporary_test_config = 'tests/software/test_config.yaml'
    monkeypatch.setattr(
        sys, 'argv', ['knowledge_verificator', '-c', temporary_test_config]
    )


@pytest.fixture
def server(mock_args, database_directory, server_ip, server_port):
    """Set up and teardown the server with endpoints."""
    process = multiprocessing.Process(
        target=uvicorn.run,
        args=('knowledge_verificator.backend:ENDPOINTS',),
        kwargs={'host': server_ip, 'port': server_port, 'reload': False},
    )
    process.start()
    # Wait for a server to start up.
    time.sleep(2)

    yield

    process.terminate()
    time.sleep(2)
    process.kill()


def send_request(
    endpoint: str,
    server: str,
    port: int,
    timeout: int = 15,
    method: str = 'get',
    request_body: Any = None,
    expect_failure: bool = False,
) -> tuple[dict, int]:
    """
    Wrapper for convenient requests sending.

    Args:
        endpoint (str): Name of the API endpoint.
        server (str): IP or domain of the server.
        port (int): Port of the server.
        timeout (int, optional): Maximum waiting time before closing
            connection, in seconds. Defaults to 10.
        method (str, optional): HTTP method, one of "get", "post", "put",
            "delete", "patch". Defaults to 'get'.
        request_body (Any, optional): Body of the HTTP request in JSON.
            By default, None.
        expect_error (bool, optional): If a failure is the expected behaviour.
            If True, no exceptions are emitted for failed requests.

    Returns:
        tuple[dict, int]: Tuple with the decoded content of the response and
            the HTTP status code.
    """
    url = f'http://{server}:{port}/{endpoint}'
    response = requests.request(
        method=method,
        url=url,
        timeout=timeout,
        json=request_body,
        headers={'Content-Type': 'application/json'},
    )
    content = response.content.decode()
    content = json.loads(content)
    if response.status_code != 200 and not expect_failure:
        raise ValueError(content)

    return (content, response.status_code)


def test_getting_empty_database(server, server_ip, server_port):
    """Test if the empty database returns no materials when requested."""
    response, _ = send_request(
        endpoint='materials',
        server=server_ip,
        port=server_port,
        method='get',
    )
    assert response['data'] == []
    assert response['message'] == ''


def test_adding_material(server, server_ip, server_port):
    """Test if a material"""
    data = {
        'title': '123',
        'paragraphs': ['123'],
        'tags': ['123'],
    }

    response, _ = send_request(
        endpoint='materials',
        server=server_ip,
        port=server_port,
        method='post',
        request_body=data,
    )

    assert response['data']['material_id'], 'Material id is empty.'


def test_adding_and_removing_material(server, server_ip, server_port):
    """Test if a material may be added then removed."""
    data = {
        'title': '123',
        'paragraphs': ['123'],
        'tags': ['123'],
    }

    response, _ = send_request(
        endpoint='materials',
        server=server_ip,
        port=server_port,
        method='post',
        request_body=data,
    )

    assert response['data']['material_id'], 'Material id is empty.'

    material_id = response['data']['material_id']
    response, _ = send_request(
        endpoint=f'materials/{material_id}',
        server=server_ip,
        port=server_port,
        method='delete',
    )

    assert response['message']


def test_updating_material(server, server_ip, server_port):
    "Test if updating an existing material succeeds."

    data = {
        'title': '1123',
        'paragraphs': ['123'],
        'tags': ['123'],
    }

    response, status_code = send_request(
        endpoint='materials',
        server=server_ip,
        port=server_port,
        method='post',
        request_body=data,
    )

    assert status_code == 200, 'Adding a new material to the database failed.'
    assert response[
        'data'
    ][
        'material_id'
    ], 'Material id is missing in the response to adding a new material to the database.'

    material_id = response['data']['material_id']
    data = {
        'id': material_id,
        'title': 'Totally different title!',
        'paragraphs': [],
    }

    _, status_code = send_request(
        endpoint='materials',
        server=server_ip,
        port=server_port,
        method='PUT',
        request_body=data,
    )

    assert status_code == 200, 'Updating an existing material failed.'


def test_updating_non_existent_material_fails(server, server_ip, server_port):
    """Test if updating non-existent material fails."""
    data = {
        'title': '1123',
        'paragraphs': ['123'],
        'tags': ['123'],
    }

    _, status_code = send_request(
        endpoint='materials',
        server=server_ip,
        port=server_port,
        method='post',
        request_body=data,
    )

    assert status_code == 200, 'Adding a new material to the database failed.'

    _, status_code = send_request(
        endpoint='materials/rand0m_byt3s',
        server=server_ip,
        port=server_port,
        method='delete',
        expect_failure=True,
    )

    assert status_code != 404, 'Updating non-existent material cannot succeed.'
