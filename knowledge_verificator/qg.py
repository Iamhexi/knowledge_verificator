"""Module with question generation model."""

import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration  # type: ignore[import-untyped]


class QuestionGeneration:  # pylint: disable=too-few-public-methods
    """Class for generating question based on supplied context."""

    def __init__(self) -> None:
        self.trained_model_path = (
            'ZhangCheng/T5-Base-Fine-Tuned-for-Question-Generation'
        )
        self.trained_tokenizer_path = (
            'ZhangCheng/T5-Base-Fine-Tuned-for-Question-Generation'
        )

        self.model = T5ForConditionalGeneration.from_pretrained(
            self.trained_model_path
        )

        self.tokenizer = T5Tokenizer.from_pretrained(
            self.trained_tokenizer_path,
            clean_up_tokenization_spaces=True,
            legacy=True,
        )

        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu'
        )
        self.model = self.model.to(self.device)
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
