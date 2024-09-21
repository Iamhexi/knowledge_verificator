"""Main module with CLI definition."""

import logging

from logging import Logger

from knowledge_verificator.answer_chooser import AnswerChooser
from knowledge_verificator.nli import NaturalLanguageInference, Relation
from knowledge_verificator.qg import QuestionGeneration


if __name__ == '__main__':
    logger = Logger('main_logger')
    # TODO: Take logger level from CLI or config file.
    # Set logging to standard output (handle 2.) stream.
    logging_handler = logging.StreamHandler()
    logging_handler.setLevel(logging.DEBUG)
    logger.addHandler(logging_handler)

    chooser = AnswerChooser()
    qg_module = QuestionGeneration()

    paragraph = input('Enter a paragraph you would like to learn: ')
    logger.debug('Loaded the following paragraph:\n %s', paragraph)

    # Answer is a randomly choosen word.
    chosen_answer = chooser.choose_answer(paragraph=paragraph)
    # words = paragraph.split(' ')
    # chosen_answer = random.choice(words)
    logger.debug(
        'The `%s` has been chosen as the answer, based on which the question will be generated.',
        chosen_answer,
    )

    # TODO: Implement the module choosing a right phrase as a worthy answer.
    # Skip word such as: like, the, a, for, what (How are they collectively called?)
    question_with_context = qg_module.generate(
        answer=chosen_answer, context=paragraph
    )
    question = question_with_context['question']
    logger.debug(
        'Question Generation module has supplied the question: %s', question
    )

    user_answer = input(
        f'Answer the question with full sentence. {question} \n Your answer.: '
    )

    nli_module = NaturalLanguageInference()
    relation = nli_module.infer_relation(
        premise=paragraph, hypothesis=user_answer
    )

    match relation:
        case Relation.ENTAILMENT:
            feedback = 'correct.'
        case Relation.CONTRADICTION:
            feedback = f'wrong. Correct answer is {chosen_answer}'
        case Relation.NEUTRAL:
            feedback = 'not directly associated with the posed question.'

    print(f'Your answer is {feedback}')
