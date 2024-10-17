"""Natural Language Inference module with pre-trained RoBERTa-Large."""

import logging
from enum import Enum
from transformers import (  # type: ignore[import-untyped]
    AutoTokenizer,
    AutoModelForSequenceClassification,
)
import torch


class Relation(Enum):
    """Possible relations between premise and hypothesis."""

    ENTAILMENT = 'entailment'
    NEUTRAL = 'neutral'
    CONTRADICTION = 'contradiction'


class NaturalLanguageInferenceModel(Enum):
    """Enumeration of the available Natural Language Inference models."""

    ROBERTA = 'ynie/roberta-large-snli_mnli_fever_anli_R1_R2_R3-nli'
    ALBERT = 'ynie/albert-xxlarge-v2-snli_mnli_fever_anli_R1_R2_R3-nli'
    BART = 'ynie/bart-large-snli_mnli_fever_anli_R1_R2_R3-nli'
    ELECTRA = (
        'ynie/electra-large-discriminator-snli_mnli_fever_anli_R1_R2_R3-nli'
    )
    XLNET = 'ynie/xlnet-large-cased-snli_mnli_fever_anli_R1_R2_R3-nli'


class NaturalLanguageInference:
    """Implementation of Natural Language Inference module."""

    def __init__(self, model: NaturalLanguageInferenceModel) -> None:
        logging.getLogger('transformers.modeling_utils').setLevel(logging.ERROR)
        self.max_new_tokens = 256
        self.set_model(model)

    def set_model(self, model: NaturalLanguageInferenceModel) -> None:
        """
        Switch the language model and tokenizer based on the supplied option.

        Args:
            model (NaturalLanguageInferenceModel): Desired model.
        """
        self._model_type = model
        self.tokenizer = AutoTokenizer.from_pretrained(
            self._model_type.value, clean_up_tokenization_spaces=True
        )
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self._model_type.value
        )

    def get_model(self) -> str:
        """
        Get a pretty-formatted name of the currently loaded model.

        Returns:
            str: Name of the model.
        """
        return self._model_type.name

    def infer(
        self,
        premise: str,
        hypothesis: str,
        precision: int = 3,
    ) -> dict[Relation, float]:
        """
        Infer probabilities whether between `premise` and `hypothesis` occurs
        entailment, neutrality, and contradiction.

        Parameters
        ----------
        premise : str
            Premise, which is the ground truth.
        hypothesis : str
            Hypothesis, which is evaluated with `premise`.
        precision : int
            Number of decimal places, to which calculations should be rounded, by default 3.

        Returns
        -------
        dict[str, float]
            Relations names (entailment, neutrality, and contradiction) and
            their corresponding probabilities.
        """

        tokenized_input_seq_pair = self.tokenizer.encode_plus(
            premise,
            hypothesis,
            max_length=self.max_new_tokens,
            return_token_type_ids=True,
            truncation=True,
        )

        input_ids = (
            torch.Tensor(tokenized_input_seq_pair['input_ids'])
            .long()
            .unsqueeze(0)
        )

        token_type_ids = None
        # `bart` model does not have `token_type_ids`.
        if self._model_type != NaturalLanguageInferenceModel.BART:
            token_type_ids = (
                torch.Tensor(tokenized_input_seq_pair['token_type_ids'])
                .long()
                .unsqueeze(0)
            )

        attention_mask = (
            torch.Tensor(tokenized_input_seq_pair['attention_mask'])
            .long()
            .unsqueeze(0)
        )

        outputs = self.model(
            input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            labels=None,
        )

        predicted_probability = torch.softmax(outputs[0], dim=1)[
            0
        ].tolist()  # batch_size only one

        entailment = round(predicted_probability[0], precision)
        neutral = round(predicted_probability[1], precision)

        return {
            Relation.ENTAILMENT: entailment,
            Relation.NEUTRAL: neutral,
            Relation.CONTRADICTION: round(
                1.0 - entailment - neutral, precision
            ),
        }

    def infer_relation(
        self,
        premise: str,
        hypothesis: str,
    ) -> Relation:
        """
        Infer the most probable type of relationship between `premise` and
        `hypothesis`.
        """
        inference = self.infer(
            premise=premise, hypothesis=hypothesis, precision=10
        )

        max_probability = 0.0
        most_probable = Relation.CONTRADICTION
        for relation, probability in inference.items():
            if probability > max_probability:
                max_probability = probability
                most_probable = relation
        return most_probable


def get_available_nli_models() -> list[str]:
    """
    Get names of all the available Natural Language Inference models.

    Returns:
        list[str]: List of models' names.
    """
    return [model.name for model in NaturalLanguageInferenceModel]
