"""Module with NLI module tests."""

import pytest

from knowledge_verificator.nli import Relation, infer_relation

@pytest.mark.parametrize('premise,hypothesis,expected', [
    ('You know Alice.', 'You don\'t know Alice.', Relation.CONTRADICTION),
])
def test_basic_examples(premise: str, hypothesis: str, expected: Relation) -> None:
    """
    Test if basic examples of relations between premise and hypothesis
    are assessed right by NLI module.
    """
    assert infer_relation(premise=premise, hypothesis=hypothesis) == expected
