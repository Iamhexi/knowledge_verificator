"""Module with string-related utility function."""


def clip_text(text: str, max_length: int) -> str:
    """
    Clip `text` if its length exceeds `max_length`.

    If the text was clipped, it has three dots `...` at the end. Otherwise,
    the text is returned unchanged.

    Args:
        text (str): Text to clip.
        max_length (int): Maximum allowed length. It will not be exceeded.

    Returns:
        str: Clipped text.
    """
    if max_length <= 4:
        raise ValueError(
            'Minimal reasonable value of `max_length` is 4 (one character '
            f'and three dots). Supplied value of {max_length}.'
        )
    text_length = len(text)
    if text_length > max_length:
        return text[: max_length - 3] + '...'
    return text
