"""Module with an interactive command-line interface."""

from rich.text import Text

from knowledge_verificator.io_handler import logger, console, get_config
from knowledge_verificator.answer_chooser import AnswerChooser
from knowledge_verificator.materials import MaterialDatabase
from knowledge_verificator.nli import NaturalLanguageInference, Relation
from knowledge_verificator.qg.qg_model_factory import create_model
from knowledge_verificator.utils.menu import choose_from_menu


def display_feedback(relation: Relation, chosen_answer: str) -> None:
    """
    Display feedback to a terminal.

    Args:
        relation (Relation): Relation between a reference answer and the
            answer provided by a user. Either they are consistent, not
            consistent or they are independent claims.
        chosen_answer (str): An answer provided by a user.
    """
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


def run_cli_mode():
    """
    Run an interactive command-line interface.

    Raises:
        ValueError:
    """
    config = get_config()
    qg_module = create_model(config.question_generation_model)
    ac_module = AnswerChooser()
    nli_module = NaturalLanguageInference(
        model=config.natural_language_inference_model
    )

    while True:
        options = ['knowledge database', 'my own paragraph']
        user_choice = choose_from_menu(
            menu_elements=options, plural_name='options'
        )

        match user_choice:
            case 'knowledge database':
                try:
                    material_db = MaterialDatabase(config.learning_materials)
                except FileNotFoundError:
                    console.print(
                        f'In the `{config.learning_materials}` there is no database. '
                        'Try using your own materials.'
                    )
                    continue

                if not material_db.materials:
                    console.print(
                        'The knowledge database exists but is empty. '
                        'Try using your own materials.'
                    )
                    continue

                material = choose_from_menu(
                    material_db.materials,
                    plural_name='materials',
                    attribute_to_show='title',
                )

                if material is None:
                    continue

                available_paragraphs: list[str] = [
                    _paragraph
                    for _paragraph in material.paragraphs
                    if ac_module.choose_answer(_paragraph) is not None
                ]

                paragraph = choose_from_menu(available_paragraphs, 'paragraphs')

                if paragraph is None:
                    continue

                paragraph = str(paragraph)
                console.print('Learn this paragraph: ')
                console.print(paragraph)
                console.print()
                input('Press ENTER when ready.')

            case 'my own paragraph':
                console.print('Enter a paragraph you would like to learn: ')
                paragraph = input().strip()

            case _:
                console.print('Unrecognised option, try again!')
                continue

        logger.debug('Loaded the following paragraph:\n %s', paragraph)

        chosen_answer = ac_module.choose_answer(paragraph=paragraph)
        if not chosen_answer:
            logger.error(
                'The supplied paragraph is either too short or too general. '
                'Please, try providing a longer or more specific paragraph.'
            )
            continue

        console.clear()

        logger.debug(
            'The `%s` has been chosen as the answer, based on which question '
            'will be generated.',
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
            f'\nAnswer the question with full sentence. {question} \nYour answer: '
        )
        user_answer = input().strip()
        relation = nli_module.infer_relation(
            premise=paragraph, hypothesis=user_answer
        )

        display_feedback(relation=relation, chosen_answer=chosen_answer)
