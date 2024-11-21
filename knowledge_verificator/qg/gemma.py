"""The implementation of QG module with the Gemma 2B chatbot."""

from typing import Sequence
import warnings
import torch
from knowledge_verificator.qg.base import QuestionGeneration

from llama_cpp import Llama


class Gemma(QuestionGeneration):
    """Class for generating question based on supplied context."""

    def __init__(self) -> None:
        warnings.filterwarnings('ignore', category=FutureWarning)
        model_path = 'bartowski/gemma-2-2b-it-GGUF'
        gguf_file = 'gemma-2-2b-it-Q6_K_L.gguf'

        self.model = Llama.from_pretrained(
            repo_id=model_path,
            filename=gguf_file,
        )

        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu'
        )

    def _send_prompt(self, prompt: str) -> str:
        prompt = (
            '<bos><start_of_turn>user'
            f'{prompt}<end_of_turn>'
            '<start_of_turn>model'
            '<end_of_turn>'
            '<start_of_turn>model'
        )
        response = self.model(prompt, max_tokens=64, echo=True)['choices'][0][
            'text'
        ]
        to_remove = (
            '<bos><start_of_turn>user',
            '<end_of_turn>',
            '<start_of_turn>model',
            '<end_of_turn>',
            '<start_of_turn>model',
        )
        response = self._remove_phrases(text=response, to_be_removed=to_remove)
        return response.replace(prompt, '')

    def _remove_phrases(self, text: str, to_be_removed: Sequence[str]) -> str:
        for phrase in to_be_removed:
            text = text.replace(phrase, '')
        return text

    def generate(self, answer: str, context: str) -> dict[str, str]:
        """
        Generate a question based on a supplied context and answer.

        Args:
            answer (str): This answer is not used at all.
            context (str): Contextual information used to generate the question.

        Returns:
            dict[str, str]: Dictionary with a generated question, and a provided answer and context.
        """

        prompt = f'Ask a question about TEXT. \nTEXT:\n{context}\n\n---'
        question = self._send_prompt(prompt)

        prompt = (
            f'TEXT:\n{context}\n\n---\nPlease answer to the following '
            'question based on TEXT. '
            f'{question}'
        )
        answer = self._send_prompt(prompt)

        return {'question': question, 'answer': answer, 'context': context}

    def get_model(self) -> str:
        """
        Get a nicely-formatted name of the used question generation model.

        Returns:
            str: Name of the model.
        """
        return 'Gemma'
