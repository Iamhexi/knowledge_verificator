"""Natural Language Inference module with pre-trained RoBERTa-Large."""

from enum import Enum
import operator
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import warnings
import logging


class Relation(Enum):
    """Possible relations between premise and hypothesis."""
    ENTAILMENT = 'entailment'
    NEUTRAL = 'neutral'
    CONTRADICTION = 'contradiction'


def infer(
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
        Hypothesis, which is evalutated with `premise`.
    precision : int
        Number of decimal places, to which calculations should be rounded, by default 3.

    Returns
    -------
    dict[str, float]
        Relations names (entailment, neutrality, and contradiction) and
        their corresponding probabilities.
    """

    max_length = 256

    hg_model_hub_name = "ynie/roberta-large-snli_mnli_fever_anli_R1_R2_R3-nli"
    # hg_model_hub_name = "ynie/albert-xxlarge-v2-snli_mnli_fever_anli_R1_R2_R3-nli"
    # hg_model_hub_name = "ynie/bart-large-snli_mnli_fever_anli_R1_R2_R3-nli"
    # hg_model_hub_name = "ynie/electra-large-discriminator-snli_mnli_fever_anli_R1_R2_R3-nli"
    # hg_model_hub_name = "ynie/xlnet-large-cased-snli_mnli_fever_anli_R1_R2_R3-nli"

    logging.getLogger("transformers").setLevel(logging.ERROR)
    warnings.filterwarnings('ignore', message="`clean_up_tokenization_spaces` was not set.")

    tokenizer = AutoTokenizer.from_pretrained(hg_model_hub_name)
    model = AutoModelForSequenceClassification.from_pretrained(hg_model_hub_name)

    tokenized_input_seq_pair = tokenizer.encode_plus(
        premise,
        hypothesis,
        max_length=max_length,
        return_token_type_ids=True,
        truncation=True,
    )

    input_ids = torch.Tensor(tokenized_input_seq_pair['input_ids']).long().unsqueeze(0)
    # remember bart doesn't have 'token_type_ids', remove the line below if you are using bart.
    token_type_ids = torch.Tensor(tokenized_input_seq_pair['token_type_ids']).long().unsqueeze(0)
    attention_mask = torch.Tensor(tokenized_input_seq_pair['attention_mask']).long().unsqueeze(0)

    outputs = model(
        input_ids,
        attention_mask=attention_mask,
        token_type_ids=token_type_ids,
        labels=None
    )

    predicted_probability = torch.softmax(outputs[0], dim=1)[0].tolist()  # batch_size only one

    entailment = round(predicted_probability[0], precision)
    neutral = round(predicted_probability[1], precision)
    contradiction = round(1. - entailment - neutral, precision)

    return {
        Relation.ENTAILMENT : entailment,
        Relation.NEUTRAL : neutral,
        Relation.CONTRADICTION : contradiction,
    }

def infer_relation(
    premise: str,
    hypothesis: str,
) -> Relation:
    """Infer the most probable type of relationship between `premise` and `hypothesis`."""
    inference = infer(premise=premise, hypothesis=hypothesis, precision=10)

    max_probability = 0.
    most_probable = Relation.CONTRADICTION
    for (relation, probability) in inference.items():
        if probability > max_probability:
            max_probability = probability
            most_probable = relation
    return most_probable
