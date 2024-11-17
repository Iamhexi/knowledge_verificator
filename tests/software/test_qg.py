"""Module with Question Generation module tests."""

from time import time
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
    'answer,context',
    (
        (
            'red',
            'The red apple is on a tree.',
        ),
        (
            'main memory',
            (
                'A computer has different types of memory: CPU registers, '
                'three-level cache, main memory and mass memory'
            ),
        ),
    ),
)
def test_basic_question_generation(answer: str, context: str, qg):
    """Test if generating in very simple case works as expected."""
    max_inference_period = 30  # in seconds
    before_inference = time()
    output = qg.generate(answer=answer, context=context)
    after_inference = time()

    keys = ('answer', 'context', 'question')

    for key, value in output.items():
        assert key in keys
        assert len(value) > 0
        if key == 'question':
            assert value.endswith('?')

    assert (
        inference_time := after_inference - before_inference
    ) < max_inference_period, (
        f'Inference time has exceeded its limit of {max_inference_period} s.'
        f' Inference consumed {inference_time} s.'
    )
