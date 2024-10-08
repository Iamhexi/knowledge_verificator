"""Main module with CLI definition."""

from pathlib import Path
import sys
from rich.text import Text

from knowledge_verificator.io_handler import logger, console, config
from knowledge_verificator.answer_chooser import AnswerChooser
from knowledge_verificator.materials import MaterialDatabase
from knowledge_verificator.nli import NaturalLanguageInference, Relation
from knowledge_verificator.qg import QuestionGeneration
from knowledge_verificator.utils.configuration_parser import OperatingMode
from knowledge_verificator.utils.menu import choose_from_menu
from tests.model.runner import ExperimentRunner


if __name__ == '__main__':
    qg_module = QuestionGeneration()
    chooser = AnswerChooser()

    if config.mode == OperatingMode.EXPERIMENT:
        experiment_directory = Path(config.experiment_implementation)
        runner = ExperimentRunner(directory=experiment_directory)
        runner.run()
        sys.exit(0)

    while True:
        options = ['knowledge database', 'my own paragraph']
        user_choice = choose_from_menu(
            menu_elements=options, plural_name='options'
        )

        match user_choice:
            case 'knowledge database':
                try:
                    STORAGE_PATH = './learning_assets'
                    material_db = MaterialDatabase(STORAGE_PATH)
                except FileNotFoundError:
                    console.print(
                        f'In the `{STORAGE_PATH}` there is no database. '
                        'Try using your own materials.'
                    )
                    continue

                if not material_db.materials:
                    console.print(
                        'The knowledge database exists but is empty. '
                        'Try using your own materials.'
                    )
                    continue

                material_titles = [
                    material.title for material in material_db.materials
                ]
                material = choose_from_menu(
                    material_db.materials,
                    plural_name='materials',
                    attribute_to_show='title',
                )

                if material is None:
                    continue

                PARAGRAPH = str(
                    choose_from_menu(material.paragraphs, 'paragraphs')
                )

                if PARAGRAPH is None:
                    continue

                console.print('Learn this paragraph: ')
                console.print(PARAGRAPH)
                console.print()
                input('Press ENTER when ready.')

            case 'my own paragraph':
                console.print('Enter a paragraph you would like to learn: ')
                PARAGRAPH = input().strip()

            case _:
                console.print('Unrecognised option, try again!')

        logger.debug('Loaded the following paragraph:\n %s', PARAGRAPH)

        chosen_answer = chooser.choose_answer(paragraph=PARAGRAPH)
        if not chosen_answer:
            raise ValueError(
                'The supplied paragraph is either too short or too general. '
                'Please, try providing a longer or more specific paragraph.'
            )

        console.clear()

        logger.debug(
            'The `%s` has been chosen as the answer, based on which question '
            'will be generated.',
            chosen_answer,
        )

        question_with_context = qg_module.generate(
            answer=chosen_answer, context=PARAGRAPH
        )
        question = question_with_context['question']
        logger.debug(
            'Question Generation module has supplied the question: %s', question
        )

        console.print(
            f'\nAnswer the question with full sentence. {question} \nYour answer: '
        )
        user_answer = input().strip()

        nli_module = NaturalLanguageInference()
        relation = nli_module.infer_relation(
            premise=PARAGRAPH, hypothesis=user_answer
        )

        match relation:
            case Relation.ENTAILMENT:
                FEEDBACK = 'correct'
                STYLE = 'green'
            case Relation.CONTRADICTION:
                FEEDBACK = f'wrong. Correct answer is {chosen_answer}'
                STYLE = 'red'
            case Relation.NEUTRAL:
                FEEDBACK = 'not directly associated with the posed question'
                STYLE = 'yellow'

        feedback_text = Text(f'Your answer is {FEEDBACK}.', style=STYLE)
        console.print(feedback_text)
