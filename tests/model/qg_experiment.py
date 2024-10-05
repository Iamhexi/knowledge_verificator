"""Module with performance experiments of Question Generation module."""

import numpy as np
from sentence_transformers import SentenceTransformer

from knowledge_verificator.qg import QuestionGeneration
from tests.model.runner import Metric, Result


def measure_qg_performance_with_cosine_similarity() -> Result:
    """
    Test performance of question generation module using cosine similarity
    between reference question and generated by a model, provided that it
    has received context and an answer (if required).
    """
    model = SentenceTransformer('sentence-transformers/all-distilroberta-v1')

    test_data = [
        {
            'question': 'What color is the sky during the day?',
            'context': 'During the day, the sky appears blue.',
            'answer': 'blue',
        },
        {
            'question': 'What is the function of the frontend in software development?',
            'context': 'In software development, the terms frontend and backend refer to the distinct roles of the user interface (frontend) and the data management layer (backend) of an application. In a client-server architecture, the client typically represents the frontend, while the server represents the backend, even if some presentation tasks are handled by the server.',
            'answer': 'presentation layer',
        },
    ]

    qg = QuestionGeneration()
    metric = Metric.COSINE_SIMILARITY
    model_name = qg.trained_model_path.split('/')[1]
    data_points: np.ndarray = np.zeros(shape=(len(test_data), 1))

    for i, test_item in enumerate(test_data):
        suggested_answer = test_item['answer']
        context = test_item['context']
        reference_question = test_item['question']

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