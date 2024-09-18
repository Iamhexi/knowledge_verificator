"""Main module with CLI definition."""
<<<<<<< HEAD
||||||| parent of 0627c06 (feat(qg): implement basic QG module)
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
=======

if __name__ == '__main__':
    print('Currently nothing happens here.')
>>>>>>> 0627c06 (feat(qg): implement basic QG module)
