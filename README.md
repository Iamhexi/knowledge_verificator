# Knowledge Verificator
[![Main CI pipeline](https://github.com/Iamhexi/knowledge_verificator/actions/workflows/main.yml/badge.svg)](https://github.com/Iamhexi/knowledge_verificator/actions/workflows/main.yml)

**Knowledge Verificator** is a tool for self-learning. It employs *Natural Language Processing* (NLP) techniques to facilitate and increase effectiveness of self-study.
The project has been created as the Bachelor's Thesis of Igor Sosnowicz.

Using **Knowledge Verificator** is simple. Step by step:
1. Insert a paragraph you want to teach yourself or choose something from a databaset of predefined ones.
1. **Knowledge Verificator** generates a question for you.
1. You answer the question.
1. Your question is evaluated and you get the feedback.
1. The process repeats as long as you like.


## Installation

### Install with `pipx`

If you have `pipx` already installed, use:

```bash
pipx install knowledge-verificator
```

### Install with `pip`

If you have `pip` already installed, use:

```bash
pip install knowledge-verificator
```

## Usage

### Run with `pipx`

If you have installed with `pipx`, run with:

```bash
pipx run knowledge-verificator
```

### Run with `pip`

If you have installed with `pip`, run with:

```bash
python -m knowledge_verificator
```

## Development

### Prerequisites
You have to have the following tools installed:
- build and dependency management system: [poetry](https://github.com/python-poetry/poetry)
- npm - javascript package manager

### Steps

#### Backend
1. Clone the repository.
    ```bash
    git clone git@github.com:Iamhexi/knowledge_verificator.git
    ```

1. Enter its directory.
    ```bash
    cd knowledge_verificator
    ```

1. Install all dependencies, also including the optional ones.
    ```bash
    poetry install --with test
    ```
---
As a one-liner:

```bash
git clone git@github.com:Iamhexi/knowledge_verificator.git && cd knowledge_verificator && poetry install --with test
```

#### Frontend

1. Change directory to `frontend`.
    ```bash
    cd frontend
    ```

1. Install the modules required by the frontend.
    ```bash
    npm install
    ```
---
As a one-liner:
```bash
cd frontend && npm install
```

---

And then run the application (make sure you are in the root directory of the repository).
```bash
poetry run python knowledge_verificator/main.py
```
