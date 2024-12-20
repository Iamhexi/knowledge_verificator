"""Module with factory of Question Generation (QG) models."""

from enum import Enum
from knowledge_verificator.qg.base import QuestionGeneration

from knowledge_verificator.qg.t5_fine_tuned import T5FineTuned
from knowledge_verificator.qg.t5_flan_base import T5FlanBase


class QuestionGenerationModel(Enum):
    """Enumeration with the available Question Generation models."""

    T5 = T5FineTuned
    FLAN_T5 = T5FlanBase


def create_model(model: QuestionGenerationModel) -> QuestionGeneration:
    """
    Instantiate a Question Generation module with the desired model.

    Args:
        model (QuestionGenerationModel): Chosen QG model.

    Returns:
        QuestionGeneration: Instance of Question Generation model.
    """
    return model.value()


def get_available_qg_models() -> list[str]:
    """
    Get a list of available Question Generation models.

    Returns:
        list[str]: _description_
    """
    return [model.name for model in QuestionGenerationModel]
