"""The implementation of QG module with the Tiny Llama 2.1 1.1B chatbot."""

import warnings
import torch
from transformers import pipeline
from knowledge_verificator.qg.base import QuestionGeneration


class TinyLama(QuestionGeneration):
    """Class for generating question based on supplied context."""

    def __init__(self) -> None:
        warnings.filterwarnings('ignore', category=FutureWarning)
        model_path = 'TinyLlama/TinyLlama-1.1B-Chat-v1.0'
        self.pipe = pipeline(
            'text-generation',
            model=model_path,
            torch_dtype=torch.bfloat16,
            device_map='auto',
        )

        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu'
        )

    def _send_prompt(self, system_prompt: str, prompt: str) -> str:
        messages = [
            {
                'role': 'system',
                'content': system_prompt,
            },
            {
                'role': 'user',
                'content': prompt,
            },
        ]
        prompt = self.pipe.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        outputs = self.pipe(
            prompt,
            max_new_tokens=165,
            do_sample=True,
            temperature=0.3,
            top_k=50,
            top_p=0.95,
        )
        return outputs[0]['generated_text']

    def generate(self, answer: str, context: str) -> dict[str, str]:
        """
        Generate a question based on a supplied context and answer.

        Args:
            answer (str): This answer is not used at all.
            context (str): Contextual information used to generate the question.

        Returns:
            dict[str, str]: Dictionary with a generated question, and a provided answer and context.
        """
        system_prompt = (
            'You are the system generating questions. '
            'Ask a question about the TEXT provided by a user. '
            'Your question cannot be taken directly from the text. '
            'Do not answer the question.'
        )
        question = self._send_prompt(
            system_prompt=system_prompt, prompt=context
        )

        system_prompt = (
            'Please answer to the following question based on TEXT. '
            'Do not answer directly from TEXT. '
        )
        prompt = f'TEXT:\n{context}' '\n\n---\n' f'QUESTION: {question}'
        answer = self._send_prompt(system_prompt=system_prompt, prompt=prompt)

        return {'question': question, 'answer': answer, 'context': context}

    def get_model(self) -> str:
        """
        Get a nicely-formatted name of the used question generation model.

        Returns:
            str: Name of the model.
        """
        return 'Gemma'
