"""Module for downloading resource required for the app to run."""

from knowledge_verificator.answer_chooser import AnswerChooser
from knowledge_verificator.io_handler import config
from knowledge_verificator.nli import NaturalLanguageInference
from knowledge_verificator.qg.qg_model_factory import create_model


def download_models() -> None:
    """
    Download the default models for Natural Language Inference,
    Question Generation, and resources for NLTK.

    The function is used externally in building a Docker image.
    """
    NaturalLanguageInference(config().natural_language_inference_model)
    AnswerChooser()
    create_model(config().question_generation_model)


if __name__ == '__main__':
    download_models()
