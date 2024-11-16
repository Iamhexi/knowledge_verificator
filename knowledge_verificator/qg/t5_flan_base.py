"""The module with implementation of fine-tuned version of T5 (called FLAN T5)."""

import warnings
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM  # type: ignore[import-untyped]
import torch
from knowledge_verificator.qg.base import QuestionGeneration


class T5FlanBase(QuestionGeneration):
    """Class for generating question based on supplied context."""

    def __init__(self) -> None:
        warnings.filterwarnings('ignore', category=FutureWarning)
        self.tokenizer = AutoTokenizer.from_pretrained('google/flan-t5-large')
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            'google/flan-t5-large', device_map='auto'
        )

        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu'
        )
        self.model = self.model  # .to(self.device)
        self.model.eval()

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
        input_ids = self.tokenizer(
            input_text, return_tensors='pt'
        ).input_ids.to(self.device)
        output_ids = self.model.generate(
            input_ids,
            max_length=100,
            temperature=0.5,  # Adjust temperature for randomness
            top_k=100,  # Limit to top-k words
            top_p=0.95,  # Nucleus sampling
            do_sample=True,  # Enable sampling
        )
        question = self.tokenizer.decode(
            output_ids[0], skip_special_tokens=True
        )

        input_text = (
            f'TEXT:\n{context}\n\n---\nPlease answer to the following '
            'question based on TEXT. Do not answer directly from TEXT. '
            f'{question}'
        )
        input_ids = self.tokenizer(
            input_text, return_tensors='pt'
        ).input_ids.to(self.device)
        output_ids = self.model.generate(input_ids)
        answer = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

        return {'question': question, 'answer': answer, 'context': context}

    def get_model(self) -> str:
        """
        Get a nicely-formatted name of the used question generation model.

        Returns:
            str: Name of the model.
        """
        return 'FLAN T5'
