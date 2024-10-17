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

SERVER = '127.0.0.1'
PORT = 8000


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


@pytest.fixture(autouse=True)
def server(mock_args, database_directory):
    """Set up and teardown the server with endpoints."""
    process = multiprocessing.Process(
        target=uvicorn.run,
        args=('knowledge_verificator.backend:ENDPOINTS',),
        kwargs={'host': SERVER, 'port': PORT, 'reload': False},
    )
    process.start()
    wait_for_server_startup(timeout=15)

    yield

    process.terminate()
    process.join(10)


def wait_for_server_startup(timeout: int = 10) -> None:
    """
    Wait until the server is ready.

    Args:
        timeout (int, optional): Number of seconds before the server startup will
            be considered failed and forcefully stopped. Defaults to 10.

    Raises:
        RuntimeError: Raised if the server did not start before the timeout.
    """
    url = f'http://{SERVER}:{PORT}/materials'
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=time.time() - start_time)
            if response.status_code == 200:
                return None
        except requests.ConnectionError:
            pass
        time.sleep(1)
    raise RuntimeError('Server did not start in time.')


@pytest.fixture
def material() -> dict[str, str | list]:
    """Fixture to provide required fields to create a learning material."""
    return {
        'title': '123',
        'paragraphs': ['123'],
        'tags': ['123'],
    }


def send_request(
    endpoint: str,
    timeout: int = 15,
    method: str = 'get',
    request_body: Any = None,
    expect_failure: bool = False,
) -> tuple[dict, int]:
    """
    Wrapper for convenient requests sending.

    Args:
        endpoint (str): Name of the API endpoint.
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
    url = f'http://{SERVER}:{PORT}/{endpoint}'
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


def test_getting_empty_database():
    """Test if the empty database returns no materials when requested."""
    response, _ = send_request(
        endpoint='materials',
        method='get',
    )
    assert response['data'] == []
    assert response['message'] == ''


def test_adding_material(material):
    """Test if a material"""

    response, _ = send_request(
        endpoint='materials',
        method='post',
        request_body=material,
    )

    assert response['data']['material_id'], 'Material id is empty.'


def test_adding_and_removing_material(material):
    """Test if a material may be added then removed."""

    response, _ = send_request(
        endpoint='materials',
        method='post',
        request_body=material,
    )

    assert response['data']['material_id'], 'Material id is empty.'

    material_id = response['data']['material_id']
    response, _ = send_request(
        endpoint=f'materials/{material_id}',
        method='delete',
    )

    assert response['message']


def test_updating_material(material):
    "Test if updating an existing material succeeds."

    response, status_code = send_request(
        endpoint='materials',
        method='post',
        request_body=material,
    )

    assert status_code == 200, 'Adding a new material to the database failed.'
    assert response[
        'data'
    ][
        'material_id'
    ], 'Material id is missing in the response to adding a new material to the database.'

    material_id = response['data']['material_id']
    new_material = {
        'id': material_id,
        'title': 'Totally different title!',
        'paragraphs': [],
    }

    response, status_code = send_request(
        endpoint='materials',
        method='PUT',
        request_body=new_material,
    )

    assert status_code == 200, 'Updating an existing material failed.'
    assert (
        'Updated the material with id' in response['message']
    ), 'Failed to update the material.'
    assert (
        new_material['title'] == response['data']['title']
    ), 'Title of the material has not been updated.'


def test_updating_non_existent_material_fails(material):
    """Test if updating non-existent material fails."""

    _, status_code = send_request(
        endpoint='materials',
        method='post',
        request_body=material,
    )

    assert status_code == 200, 'Adding a new material to the database failed.'

    _, status_code = send_request(
        endpoint='materials/rand0m_byt3s',
        method='delete',
        expect_failure=True,
    )

    assert status_code != 404, 'Updating non-existent material cannot succeed.'
