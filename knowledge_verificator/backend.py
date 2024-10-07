"""Module with backend defining endpoints."""

from typing import Any, Union

from fastapi import FastAPI


endpoints = FastAPI()


def format_response(data: Any = '', successful: bool = True) -> dict:
    """Format a response to a request to a single format."""
    if successful:
        message = 'Success'
    else:
        message = 'Failure'
    return {'data': data, 'message': message}


@endpoints.get('/materials')
def get_materials():
    """Get all learning materials."""
    # return materials.materials()
    return format_response(successful=True)


@endpoints.get('/materials/{material_id}')
def get_material(material_id: int, q: Union[str, None] = None):
    """
    Get a specific learning material.

    Args:
        material_id (int): ID of a material to retrieve.
        q (Union[str, None], optional): Query to find a material if
        `material_id` is not known. Defaults to None.

    Returns:
        dict: Response with status of a request
        status and a learning material if request was processed correctly.
    """
    data = {'material_id': material_id, 'query': q}
    return format_response(data=data, successful=True)


@endpoints.delete('/materials/{material_id}')
def delete_material(material_id: int):
    """Delete a learning material with the supplied `material_id`."""
    return format_response(data=str(material_id), successful=False)
