"""Module with performance experiments of Question Generation module."""

from functools import cache
from pathlib import Path
from typing import Callable
import warnings
import torch
import yaml  # type: ignore[import-untyped]
import numpy as np
from sentence_transformers import SentenceTransformer

from knowledge_verificator.qg.qg_model_factory import QuestionGenerationModel
from knowledge_verificator.utils.metrics import (
    calculate_bleu_4,
    calculate_meteor,
    calculate_rouge_lcs,
    calculate_rouge_n,
)
from tests.model.runner import Metric, Result

warnings.filterwarnings('ignore')


def get_test_data() -> list[dict[str, dict]]:
    """
    Retrieve test data from a YAML file.

    Returns:
        list[dict[str, str]]: List of dictionaries each having
            keys: context, question, answer.
    """
    with open(
        Path('tests/model/qg_test_data.yaml'), 'rt', encoding='utf-8'
    ) as fd:
        what = yaml.safe_load(fd)
        return what


def measure_qg_performance_with_cosine_similarity() -> list[Result]:
    """
    Test performance of the question generation module using cosine similarity
    between a reference and generated question by all QG models, provided that
    it has received context and an answer (if required).
    """
    model = SentenceTransformer('sentence-transformers/all-distilroberta-v1')

    def evaluate_with_cosine_similarity(reference: str, hypothesis: str):
        sentences = [hypothesis, reference]
        embeddings = model.encode(sentences)
        similarities = model.similarity(embeddings, embeddings)
        return float(similarities.tolist()[1][0])

    return _calculate_metric(
        metric=Metric.COSINE_SIMILARITY,
        evaluation_function=evaluate_with_cosine_similarity,
    )


@cache
def _generate_responses() -> dict[str, list[dict[str, str]]]:
    test_data = get_test_data()
    response_data: dict[str, list[dict[str, str]]] = {}

    for qg_model in QuestionGenerationModel:
        qg = qg_model.value()

        model_name = qg.get_model()

        response_data[model_name] = []

        for test_item in test_data:
            item = test_item['item']
            suggested_answer = item['answer']
            context = item['context']
            reference_question = item['question']

            generated_question = qg.generate(
                answer=suggested_answer, context=context
            )['question']

            response_data[model_name].append(
                {
                    'reference_question': reference_question,
                    'generated_question': generated_question,
                }
            )

        del qg
        torch.cuda.empty_cache()
    return response_data


def _calculate_metric(
    metric: Metric,
    evaluation_function: Callable,
) -> list[Result]:
    """
    Calculate a metric with a provided evaluation function.

    Args:
        metric (Metric): Metric, which is measured.
        evaluation_function (callable): Its header should be:
            `def callback(reference_question: str, generated_question: str) -> float`.

    Returns:
        list[Result]: List of evaluations of test data items.
    """
    model_responses = _generate_responses()
    results: list[Result] = []

    for model_name, questions_with_responses in model_responses.items():
        data_points: np.ndarray = np.zeros(
            shape=(len(questions_with_responses), 1)
        )
        for i, question_response_pair in enumerate(questions_with_responses):
            data_points[i] = evaluation_function(
                question_response_pair['reference_question'],
                question_response_pair['generated_question'],
            )

        results.append(
            Result(
                metric=metric,
                data_points=data_points,
                model_name=model_name,
            )
        )

    return results


def measure_qg_performance_with_bleu_4() -> list[Result]:
    """
    Measure performance of the QG module with the BLEU-4 score.

    Returns:
        list[Result]: List of evaluations of test data items.
    """
    return _calculate_metric(
        metric=Metric.BLEU_4, evaluation_function=calculate_bleu_4
    )


def measure_qg_performance_with_meteor() -> list[Result]:
    """
    Measure performance of the QG module with the METEOR score.

    Returns:
        list[Result]: List of evaluations of test data items.
    """
    return _calculate_metric(
        metric=Metric.METEOR, evaluation_function=calculate_meteor
    )


def measure_qg_performance_with_rouge_3() -> list[Result]:
    """
    Measure performance of the QG module with the ROUGE-3 score.

    Returns:
        list[Result]: List of evaluations of test data items.
    """

    def calc_rouge_3(reference: str, hypothesis: str) -> float:
        return calculate_rouge_n(
            reference=reference, hypothesis=hypothesis, n=3
        )

    return _calculate_metric(
        metric=Metric.ROUGE_3, evaluation_function=calc_rouge_3
    )


def measure_qg_performance_with_rouge_lcs() -> list[Result]:
    """
    Measure performance of the QG module with the ROUGE-LCS score.

    Returns:
        list[Result]: List of evaluations of test data items.
    """
    return _calculate_metric(
        metric=Metric.ROUGE_3, evaluation_function=calculate_rouge_lcs
    )
