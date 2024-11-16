"""Module with performance experiments of Question Generation module."""

from pathlib import Path
import yaml  # type: ignore[import-untyped]
import numpy as np
from sentence_transformers import SentenceTransformer

from knowledge_verificator.qg.t5_flan_base import T5FlanBase
from tests.model.runner import Metric, Result


def measure_qg_performance_with_cosine_similarity() -> Result:
    """
    Test performance of question generation module using cosine similarity
    between reference question and generated by a model, provided that it
    has received context and an answer (if required).
    """
    model = SentenceTransformer('sentence-transformers/all-distilroberta-v1')

    test_data = None
    with open(
        Path('tests/model/qg_test_data.yaml'), 'rt', encoding='utf-8'
    ) as fd:
        test_data = yaml.safe_load(fd)

    qg = T5FlanBase()
    metric = Metric.COSINE_SIMILARITY
    model_name = qg.get_model()
    data_points: np.ndarray = np.zeros(shape=(len(test_data), 1))

    for i, test_item in enumerate(test_data):
        item = test_item['item']
        suggested_answer = item['answer']
        context = item['context']
        reference_question = item['question']

        generated_question = qg.generate(
            answer=suggested_answer, context=context
        )['question']

        sentences = [generated_question, reference_question]

        embeddings = model.encode(sentences)

        # Outputs tensor:
        # 1.0 abc
        # abc 1.0
        similarities = model.similarity(embeddings, embeddings)

        data_point = float(similarities.tolist()[1][0])
        data_points[i] = data_point

    return Result(
        metric=metric,
        data_points=data_points,
        model_name=model_name,
    )
