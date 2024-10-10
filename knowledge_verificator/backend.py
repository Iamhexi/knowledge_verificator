"""Module with the backend defining available endpoints."""

from typing import Any, Union

from fastapi import FastAPI, Response

from knowledge_verificator.materials import Material, MaterialDatabase
from knowledge_verificator.io_handler import config

endpoints = FastAPI()
material_db = MaterialDatabase(materials_dir=config.learning_materials)


def format_response(data: Any = '', message: str = '') -> dict:
    """
    Format a response to a request to a defined JSON format.

    The format looks in the following way:
    ```json
    {
        'data': <data>,
        'message': <message>
    }
    ```
    Args:
        data (Any, optional): Requested data. Defaults to ''.
        message (str, optional): Description of a result. Especially useful
            when something went wrong. Defaults to ''.

    Returns:
        dict: Dict with keys `data` and `message`. Data contains crucial
            information about a requested operation. Message is used to
            convey additional information such as a failure description.
    """
    return {
        'data': data,
        'message': message,
    }


@endpoints.get('/materials')
def get_materials(
    response: Response, criteria: Union[str, None] = None
) -> dict:
    """
    Get all learning materials matching criteria.

    Args:
        response (Response): Instance of response, provided automatically.
        criteria (Union[str, None], optional): Criteria, which materials have
        to match to be retrieved. Defaults to None.

    Returns:
        dict: Requested materials with corresponding IDs.
    """
    if criteria is not None:
        message = 'Applying criteria is not implemented yet.'
        response.status_code = 501
        return format_response(message=message)
    response.status_code = 200
    return format_response(data=material_db.materials)


@endpoints.get('/materials/{material_id}')
def get_material(material_id: str, response: Response):
    """
    Get a specific learning material.

    Args:
        material_id (str): ID of a material to retrieve.
        response (Response): Instance of response, provided automatically.

    Returns:
        dict: Under `data` key, there are `material_id` and `material` keys.
    """
    try:
        material = material_db[material_id]
    except KeyError:
        message = f'Material with id = {material_id} was not found.'
        response.status_code = 404
        return format_response(message=message)

    data = {'material_id': material_id, 'material': material}
    response.status_code = 200
    return format_response(data=data)


@endpoints.post('/materials')
def add_material(material: Material, response: Response) -> dict:
    """
    Endpoint to add a learning material to a database.

    Args:
        material (Material): Learning material to be added.
        response (Response): Response to a request. Automatically passed.

    Returns:
        dict: Under 'data' key, there is `material_id` key containing ID
        of the newly added material.
    """
    response.status_code = 200
    message = ''
    try:
        material_db.add_material(material=material)
    except ValueError as e:
        message = str(e)
        response.status_code = 400
    except FileExistsError as e:
        message = str(e)
        response.status_code = 403

    if response.status_code != 200:
        return format_response(message=message)

    data = {'material_id': material.id}
    return format_response(data=data)


@endpoints.delete('/materials/{material_id}')
def delete_material(material_id: str, response: Response) -> dict:
    """
    Endpoint to delete a learning material.

    Args:
        material_id (str): ID of the material to be removed.
        response (Response): Response to a request. Automatically passed.

    Returns:
        dict: Under `data` key, there is `material_id` key containing ID
        of the removed material.
    """
    try:
        material_db.delete_material(material=material_id)
    except KeyError as e:
        message = str(e)
        response.status_code = 400
        return format_response(message=message)

    response.status_code = 200
    return format_response(data=str(material_id))
