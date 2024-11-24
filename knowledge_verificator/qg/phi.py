"""The module with implementation of fine-tuned version of T5 (called FLAN T5)."""

import warnings
from transformers import AutoTokenizer, AutoModelForCausalLM  # type: ignore[import-untyped]
import torch
from knowledge_verificator.qg.base import QuestionGeneration


class Phi(QuestionGeneration):
    """Class for generating question based on supplied context."""

    def __init__(self) -> None:
        warnings.filterwarnings('ignore', category=FutureWarning)
        model_path = 'microsoft/phi-1_5'
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path, device_map='auto'
        )

        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu'
        )

    def _send_prompt(self, prompt: str) -> str:
        max_new_tokens = 64
        input_ids = self.tokenizer(
            prompt, return_tensors='pt', return_attention_mask=False
        ).input_ids.to(self.device)
        output_ids = self.model.generate(
            input_ids,
            max_new_tokens=max_new_tokens,
        )
        return self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

    def generate(self, answer: str, context: str) -> dict[str, str]:
        """
        Generate a question based on a supplied context and answer.

        Args:
            answer (str): This answer is not used at all.
            context (str): Contextual information used to generate the question.

        Returns:
            dict[str, str]: Dictionary with a generated question, and a provided answer and context.
        """
        input_text = (
            f'TEXT:\n{context}\n\n---\nAsk a question about TEXT. '
            'Your question cannot be taken directly from the text.'
        )
        question = self._send_prompt(prompt=input_text)

        input_text = (
            f'TEXT:\n{context}\n\n---\nPlease answer to the following '
            'question based on TEXT. Do not answer directly from TEXT. '
            f'{question}'
        )
        answer = self._send_prompt(prompt=input_text)

        return {'question': question, 'answer': answer, 'context': context}

    def get_model(self) -> str:
        """
        Get a nicely-formatted name of the used question generation model.

        Returns:
            str: Name of the model.
        """
        return 'Phi'
