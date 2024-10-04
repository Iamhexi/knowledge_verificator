"""Module with utilities supporting creation of CLI menus."""

from typing import Any
from knowledge_verificator.io_handler import console
from knowledge_verificator.utils.string import clip_text


def choose_from_menu(
    menu_elements: list[Any],
    plural_name: str,
    attribute_to_show: str = '',
    max_line_width: int = 40,
) -> Any | None:
    """
    Prompt a user to choose an element from a list via terminal.

    Args:
        menu_elements (list[str]): List of elements to choose from.
            Elements should be convertible to `str` (implement `__str__` method).
        plural_name (str): Plural name of the elements. For example: options, paragraphs or names.
        attribute_to_show (str): Attribute, which should be shown. If empty, print an entire object.
        max_line_width (int): Maximum line width in number of columns. By default: 40.

    Returns:
        any | None: Element of a list or None if a user provided incorrect value via a terminal.
    """
    console.print(f'Available {plural_name}:')
    for i, element in enumerate(menu_elements):
        option_name = ''
        if attribute_to_show:
            option_name = getattr(element, attribute_to_show)
        else:
            option_name = element
        console.print(f'[{i+1}] {clip_text(option_name, max_line_width)}')
    material_choice = input('Your choice: ')
    console.print()

    incorrect_choice_warning = (
        'This is incorrect choice. Next time, provide a number '
        'next to a element from the list of available ones.'
    )
    if not material_choice.isnumeric():
        console.print(incorrect_choice_warning)
        return None

    chosen_index = int(material_choice) - 1
    if chosen_index < 0 or chosen_index >= len(menu_elements):
        console.print(incorrect_choice_warning)
        return None

    return menu_elements[chosen_index]
