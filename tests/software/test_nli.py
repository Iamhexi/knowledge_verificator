"""Module with NLI module tests."""

import pytest

from knowledge_verificator.nli import Relation, NaturalLanguageInference


@pytest.fixture
def nli() -> NaturalLanguageInference:
    """Provide NaturalLanuageInference class for tests."""
    model = NaturalLanguageInference()
    return model


@pytest.mark.code_quality
@pytest.mark.parametrize(
    'premise,hypothesis,expected',
    [
        ('You know Alice.', "You don't know Alice.", Relation.CONTRADICTION),
        (
            'You are in love with Alice.',
            'You have an intimate relationship with Alice.',
            Relation.ENTAILMENT,
        ),
        (
            'Neutrons are located in the atomic nucleus.',
            'Wroclaw University of Science and Technology is a leading Polish university.',
            Relation.NEUTRAL,
        ),
    ],
)
def test_basic_examples(
    premise: str, hypothesis: str, expected: Relation, nli
) -> None:
    """
    Test if basic examples of relations between premise and hypothesis
    are assessed right by NLI module.
    """
    assert (
        nli.infer_relation(premise=premise, hypothesis=hypothesis) == expected
    )
