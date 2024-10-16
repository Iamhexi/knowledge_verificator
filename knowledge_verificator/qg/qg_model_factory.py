"""Module with factory of Question Generation (QG) models."""

from knowledge_verificator.qg.base import QuestionGeneration
from knowledge_verificator.qg.t5 import T5FineTuned


def create_model(model_name: str) -> QuestionGeneration:
    """
    Instantiate a Question Generation model by the provided name.

    Args:
        model_name (str): Name of the model.

    Raises:
        ValueError: Raised if the provided name does not match to any model.

    Returns:
        QuestionGeneration: Instance of Question Generation model.
    """

    match model_name:
        case 'T5 (fine-tuned)':
            return T5FineTuned()

        case _:
            raise ValueError(
                f'Unknown Question Generation model name: {model_name}.'
            )
