"""Module with Question Generation module tests."""

import pytest

from transformers import set_seed  # type: ignore[import-untyped]
from knowledge_verificator.qg.t5_flan_base import T5FlanBase


@pytest.fixture
def qg():
    """
    Provide non-deterministically initialized instance of
    the Question Generation model.
    """
    set_seed(0)
    question_generation = T5FlanBase()
    return question_generation


@pytest.mark.parametrize(
    'question,answer,context',
    (
        (
            'What is the color of the apple?',
            'red',
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
