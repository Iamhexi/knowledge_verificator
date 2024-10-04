"""Module with Question Generation module tests."""

import pytest

from transformers import set_seed  # type: ignore[import-untyped]
from knowledge_verificator.qg import QuestionGeneration


@pytest.fixture
def qg():
    """
    Provide non-deterministically initialized instance of
    the `QuestionGeneration` class.
    """
    set_seed(0)
    question_generation = QuestionGeneration()
    return question_generation


@pytest.mark.parametrize(
    'question,answer,context',
    (
        (
            'Where is the red apple located?',
            'Tree',
            'The red apple is on a tree.',
        ),
    ),
)
def test_basic_question_generation(
    question: str, answer: str, context: str, qg
):
    """Test if generating in very simple case works as expected."""
    output = qg.generate(answer=answer, context=context)
    expected = {
        'question': question,
        'answer': answer,
        'context': context,
    }

    assert output == expected
