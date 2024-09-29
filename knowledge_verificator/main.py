"""Main module with CLI definition."""

from rich.text import Text

from knowledge_verificator.io_handler import logger, console
from knowledge_verificator.answer_chooser import AnswerChooser
from knowledge_verificator.materials import MaterialDatabase
from knowledge_verificator.nli import NaturalLanguageInference, Relation
from knowledge_verificator.qg import QuestionGeneration


if __name__ == '__main__':
    qg_module = QuestionGeneration()
    chooser = AnswerChooser()

    while True:
        console.print('Where you want to learn from?')
        console.print('[1] knowledge database')
        console.print('[2] my own paragraph')
        user_choice = input('Your choice: ')
        console.print()

        match user_choice:
            case '1':
                try:
                    DB_PATH = './data'
                    material_db = MaterialDatabase(DB_PATH)
                except FileNotFoundError:
                    console.print(
                        f'In the `{DB_PATH}` there is no database. '
                        'Try using your own materials.'
                    )
                    continue

                if not material_db.materials:
                    console.print(
                        'The knowledge database exists but is empty. '
                        'Try using your own materials.'
                    )
                    continue

                console.print('Available materials:')
                for i, material in enumerate(material_db.materials):
                    console.print(f'[{i+1}] {material.title}')
                material_choice = input('Your choice: ')
                console.print()

                INCORRECT_CHOICE_WARNING = (
                    'This is incorrect choice. Next time, provide a number '
                    'next to a material from the list of available ones.'
                )
                if not material_choice.isnumeric():
                    console.print(INCORRECT_CHOICE_WARNING)
                    continue

                chosen_index = int(material_choice) - 1
                if chosen_index < 0 or chosen_index >= len(
                    material_db.materials
                ):
                    console.print(INCORRECT_CHOICE_WARNING)
                    continue

                material = material_db.materials[chosen_index]
                # TODO: A user should be able to choose a paragraph.
                paragraph = material.paragraphs[0]

                console.print('Learn this paragraph: ')
                console.print(paragraph)
                console.print()
                input('Press ENTER when ready.')

            case '2':
                console.print('Enter a paragraph you would like to learn: ')
                paragraph = input().strip()

            case _:
                console.print('Unrecognised option, try again!')

        logger.debug('Loaded the following paragraph:\n %s', paragraph)

        chosen_answer = chooser.choose_answer(paragraph=paragraph)
        if not chosen_answer:
            raise ValueError(
                'The supplied paragaph is either too short or too general. '
                'Please, try providing a longer or more specific paragraph.'
            )

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

        nli_module = NaturalLanguageInference()
        relation = nli_module.infer_relation(
            premise=paragraph, hypothesis=user_answer
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
