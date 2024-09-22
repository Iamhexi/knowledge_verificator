"""Main module with CLI definition."""

from logger import logger, console
from rich.text import Text

from knowledge_verificator.answer_chooser import AnswerChooser
from knowledge_verificator.nli import NaturalLanguageInference, Relation
from knowledge_verificator.qg import QuestionGeneration


if __name__ == '__main__':
    chooser = AnswerChooser()
    qg_module = QuestionGeneration()

    console.print('Enter a paragraph you would like to learn: ')
    paragraph = input().strip()
    logger.debug('Loaded the following paragraph:\n %s', paragraph)

    chosen_answer = chooser.choose_answer(paragraph=paragraph)
    if not chosen_answer:
        raise ValueError(
            'The supplied paragaph is either too short or too general. '
            'Please, try providing a longer or more specific paragraph.'
        )

    logger.debug(
        'The `%s` has been chosen as the answer, based on which the question will be generated.',
        chosen_answer,
    )

    question_with_context = qg_module.generate(
        answer=chosen_answer, context=paragraph
    )
    question = question_with_context['question']
    logger.debug(
        'Question Generation module has supplied the question: %s', question
    )

    console.print(
        f'Answer the question with full sentence. {question} \n Your answer.: '
    )
    user_answer = input().strip()

    nli_module = NaturalLanguageInference()
    relation = nli_module.infer_relation(
        premise=paragraph, hypothesis=user_answer
    )

    match relation:
        case Relation.ENTAILMENT:
            feedback = 'correct'
            style = 'green'
        case Relation.CONTRADICTION:
            feedback = f'wrong. Correct answer is {chosen_answer}'
            style = 'red'
        case Relation.NEUTRAL:
            feedback = 'not directly associated with the posed question'
            style = 'yellow'

    feedback_text = Text(f'Your answer is {feedback}.', style=style)
    console.print(feedback_text)
