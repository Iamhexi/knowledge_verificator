# Question Generation module - usage

To use Question Generation (**QG** module), import it, and use `generate()` method.

```python
from knowledge_verificator.qg import QuestionGeneration

if __name__ == '__main__':
    context = input('Provide context: ')
    answer = input('Answer: ')
    QG = QuestionGeneration()
    qa = QG.generate(answer, context)
    print(qa['question'])
```
