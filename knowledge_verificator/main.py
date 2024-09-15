"""Main module with CLI definition."""
from knowledge_verificator.nli import infer_relation

if __name__ == '__main__':
    premise = input("Premise: ")
    hypothesis = input("Hypothesis: ")
    print(
        infer_relation(
            premise=premise,
            hypothesis=hypothesis
        ).value
    )
