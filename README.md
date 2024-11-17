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


## Usage

Before running the **Knowledge Verificator**, you need to [install Docker](https://docs.docker.com/engine/install/).

When Docker is installed, use the `run.sh` script to start the application:
```bash
./run.sh
```
The script handles building the image (approximately 10 minutes)
and running it (approximately 30 seconds).
Building the image happens only once, before the first usage of the application.

**Notice**: By default, only CPU is used. To enable GPU support, you have to install Nvidia Container Toolkit and configure it to cooperate with Docker by yourself. Then, you may use:
```bash
./run.sh --gpu
```

## Development

If you are interested in contributing to the project by submitting source code, you have to have finish all the steps described below.

### Prerequisites
You have to have the following tools installed:
- the Python build and dependency management system: [poetry](https://github.com/python-poetry/poetry)
- the JavaScript package manager: [npm](https://docs.npmjs.com/)

### Installation Steps

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

#### Frontend

Install the modules required by the frontend.
```bash
npm install --prefix frontend
```

#### Running

And then run the application (make sure you are in the root directory of the repository).
```bash
poetry run python knowledge_verificator/main.py
```
