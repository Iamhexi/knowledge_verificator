# Natural Language Inference module - usage

To use Natural Language Inference(**NLI** module), import it, and use `infer()` function (to get probabilities of different relationships between `premise` and `hypothesis`) or infer_relation()` function (to just get the most probable relationship).

```python
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
```