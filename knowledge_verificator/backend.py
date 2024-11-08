"""Module with the backend defining available endpoints."""

from typing import Any, Union

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from knowledge_verificator.answer_chooser import AnswerChooser
from knowledge_verificator.materials import Material, MaterialDatabase
from knowledge_verificator.io_handler import config
from knowledge_verificator.nli import (
    NaturalLanguageInference,
    NaturalLanguageInferenceModel,
    get_available_nli_models,
)
from knowledge_verificator.qg.qg_model_factory import (
    QuestionGenerationModel,
    create_model,
    get_available_qg_models,
)


# The allowed origins.
origins = [
    f'{config().protocol}://localhost:{config().frontend_port}',
    f'{config().protocol}://127.0.0.1:{config().frontend_port}',
    f'{config().protocol}://{config().frontend_address}:{config().frontend_port}',
]

ENDPOINTS = FastAPI(debug=not config().production_mode)
ENDPOINTS.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,
    allow_methods=['*'],  # Allows all methods: GET, POST, etc.
    allow_headers=['*'],  # Allows all headers
)
MATERIAL_DB = MaterialDatabase(materials_dir=config().learning_materials)
QG_MODEL = create_model(config().question_generation_model)
ANSWER_CHOOSER = AnswerChooser()

NLI_MODEL = NaturalLanguageInference(config().natural_language_inference_model)


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


@ENDPOINTS.get('/materials')
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
    return format_response(data=MATERIAL_DB.materials)


@ENDPOINTS.get('/materials/{material_id}')
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
        material = MATERIAL_DB[material_id]
    except KeyError:
        message = f'Material with id = {material_id} was not found.'
        response.status_code = 404
        return format_response(message=message)

    data = {'material_id': material_id, 'material': material}
    response.status_code = 200
    return format_response(data=data)


@ENDPOINTS.post('/materials')
def add_material(material: Material, response: Response) -> dict:
    """
    Endpoint to add a learning material to the database.

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
        MATERIAL_DB.add_material(material=material)
    except (ValueError, FileExistsError) as e:
        message = str(e)
        response.status_code = 400

    if response.status_code != 200:
        return format_response(message=message)

    data = {'material_id': material.id}
    return format_response(
        data=data, message=f'Added the material with id = {material.id}.'
    )


@ENDPOINTS.delete('/materials/{material_id}')
def delete_material(material_id: str, response: Response) -> dict:
    """
    Endpoint to delete a learning material from the database.

    Args:
        material_id (str): ID of the material to be removed.
        response (Response): Response to a request. Automatically passed.

    Returns:
        dict: Under `data` key, there is `material_id` key containing ID
        of the removed material.
    """
    try:
        MATERIAL_DB.delete_material(material=material_id)
    except KeyError as e:
        message = str(e)
        response.status_code = 400
        return format_response(message=message)

    response.status_code = 200
    return format_response(
        message=f'Deleted the material with id = {material_id}.'
    )


@ENDPOINTS.put('/materials')
def update_material(material: Material, response: Response) -> dict:
    """
    Endpoint to update multiple attributes of a learning material
    in the database.

    Args:
        material_id (str): ID of the material to be removed.
        response (Response): Response to a request. Automatically passed.

    Returns:
        dict: Under `data` key, there is `material_id` key containing ID
        of the removed material.
    """
    try:
        MATERIAL_DB.update_material(material)
    except KeyError as e:
        message = str(e)
        response.status_code = 404
        return format_response(message=message)

    response.status_code = 200
    return format_response(
        message=f'Updated the material with id = {material.id}.',
        data=MATERIAL_DB[material.id],
    )


@ENDPOINTS.get('/models/qg')
def get_qg_model() -> dict:
    """
    Endpoint to provide name of the currently chosen Question Generation model,
    and other available models.

    Returns:
        dict: Under `data` key, there is `loaded_model` key containing the name
        of the current Question Generation model, and under `available_models`
        a list of all the available QG models.
    """
    data = {
        'loaded_model': QG_MODEL.get_model(),
        'available_models': get_available_qg_models(),
    }
    return format_response(data=data)


@ENDPOINTS.get('/models/nli')
def get_nli_model() -> dict:
    """
    Endpoint to provide name of the currently chosen Natural Language Inference model and,
    other available models.

    Returns:
        dict: Under `data` key, there is `loaded_model` key containing the name
        of the current Natural Language Inference model, and under `available_models`
        the list of all the available NLI models.
    """
    data = {
        'loaded_model': NLI_MODEL.get_model(),
        'available_models': get_available_nli_models(),
    }
    return format_response(data=data)


@ENDPOINTS.post('/models/qg/{model_name}')
def set_qg_model(model_name: str, response: Response) -> dict:
    """
    Endpoint to set the Question Generation model.

    Args:
        model_name (str): Name of the desired QG model.
        response (Response): Instance of response, provided automatically.

    Returns:
        dict: If failed, only `message` key is available with the explanation
            of the reasons of the failure. If successful, under `data` key
            there is `model_name` key with the name of the new model.
    """
    try:
        model = QuestionGenerationModel[model_name]
        global QG_MODEL  # pylint: disable=global-statement

        QG_MODEL = create_model(model)
        return format_response(data={'model_name': QG_MODEL.get_model()})
    except KeyError:
        response.status_code = 404
        return format_response(
            message='Cannot change the Question Generation model because name'
            f' `{model_name}` has not been recognised.'
        )


@ENDPOINTS.post('/models/nli/{model_name}')
def set_nli_model(model_name: str, response: Response) -> dict:
    """
    Endpoint to set the Natural Language Inference model.

    Args:
        model_name (str): Name of the desired NLI model.
        response (Response): Instance of response, provided automatically.

    Returns:
        dict: If failed, only `message` key is available with the explanation
        of the reasons of the failure. If successful, under `data` key
        there is `model_name` key with the name of the new model.
    """
    try:
        model = NaturalLanguageInferenceModel[model_name]
        NLI_MODEL.set_model(model)
        return format_response(data={'model_name': NLI_MODEL.get_model()})
    except KeyError:
        response.status_code = 404
        return format_response(
            message='Cannot change the Natural Language Inference model '
            f'because name `{model_name}` has not been recognised.'
        )


class QuestionRequest(BaseModel):
    """Body parameter of /generate_question endpoint."""

    context: str


@ENDPOINTS.post('/generate_question')
def generate_question(
    question_context: QuestionRequest, response: Response
) -> dict:
    """
    Endpoint to generate a question to the supplied context using
    the currently chosen Question Generation model.

    Args:
        question_context (QuestionRequest): Context, based on which the question will be generated.
        response (Response): Instance of response, provided automatically.

    Returns:
        dict: If a request was successful, under `data` key there is `question` key
            with a question and under `answer` there is an answer.
            Otherwise, under `message` there is an error message.
    """
    context = question_context.context
    answer = ANSWER_CHOOSER.choose_answer(paragraph=context)
    if not answer:
        response.status_code = 400
        message = 'The provided text is not appropriate to generate question. Use a longer one.'
        return format_response(message=message)

    generated_item = QG_MODEL.generate(context=context, answer=answer)
    data = {'question': generated_item['question'], 'answer': answer}
    return format_response(data=data)


class AnswerEvaluationRequest(BaseModel):
    """Body parameter of /evaluate_answer endpoint."""

    context: str
    user_answer: str


@ENDPOINTS.post('/evaluate_answer')
def evaluate_answer(evaluation_request: AnswerEvaluationRequest) -> dict:
    """
    Endpoint to get an evaluation of an answer provided by a user
    with the currently chosen Natural Language Inference model.

    Args:
        evaluation_request (AnswerEvaluationRequest): Context, based on which
            the evaluated will be provided.

    Returns:
        dict: Under `data` key there is `evaluation` key
            with an evaluation.
    """
    evaluation = NLI_MODEL.infer_relation(
        premise=evaluation_request.context,
        hypothesis=evaluation_request.user_answer,
    )

    response_data = {'evaluation': evaluation.value}
    return format_response(data=response_data)
