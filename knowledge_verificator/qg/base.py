"""Module with an interface of question generation module."""

from abc import ABC, abstractmethod


class QuestionGeneration(ABC):
    """Class for generating question based on supplied context."""

    @abstractmethod
    def generate(self, answer: str, context: str) -> dict[str, str]:
        """
        Generate a question based on a supplied context and answer.

        Args:
            answer (str): Correct answer to a question to be generated.
            context (str): Contextual information, useful for question generation.

        Returns:
            dict[str, str]: Dictionary with a generated question, and a provided answer and context.
        """

    @abstractmethod
    def get_model(self) -> str:
        """
        Get a nicely-formatted name of the used question generation model.

        Returns:
            str: Name of the model.
        """
