"""Module with implementation of T5 Fine-Tuned Question Generation model."""

import warnings
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration  # type: ignore[import-untyped]
from knowledge_verificator.qg.base import QuestionGeneration


class T5FineTuned(QuestionGeneration):
    """Class for generating question based on supplied context."""

    def __init__(self) -> None:
        warnings.filterwarnings('ignore', category=FutureWarning)
        self._trained_model_path = (
            'ZhangCheng/T5-Base-Fine-Tuned-for-Question-Generation'
        )
        self._trained_tokenizer_path = (
            'ZhangCheng/T5-Base-Fine-Tuned-for-Question-Generation'
        )

        self.model = T5ForConditionalGeneration.from_pretrained(
            self._trained_model_path, device_map='auto'
        )

        self.tokenizer = T5Tokenizer.from_pretrained(
            self._trained_tokenizer_path,
            clean_up_tokenization_spaces=True,
            legacy=True,
        )

        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu'
        )
        self.model = self.model  # .to(self.device)
        self.max_length = 32
        self.model.eval()

    def generate(self, answer: str, context: str) -> dict[str, str]:
        """
        Generate a question based on a supplied context and answer.

        Args:
            answer (str): Correct answer to a question to be generated.
            context (str): Contextual information, useful for question generation.

        Returns:
            dict[str, str]: Dictionary with a generated question, and a provided answer and context.
        """
        input_text = f'<answer> {answer} <context> {context} '
        encoding = self.tokenizer.encode_plus(
            input_text,
            return_tensors='pt',
        )
        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)
        outputs = self.model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=self.max_length,
        )
        question = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True,
        )
        return {'question': question, 'answer': answer, 'context': context}

    def get_model(self) -> str:
        """
        Get a nicely-formatted name of the used question generation model.

        Returns:
            str: Name of the model.
        """
        return 'T5'
