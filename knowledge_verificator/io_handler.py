"""
Module handling Input/Output, including parsing CLI arguments, provding
an instance of `rich` console, and an instance of a preconfigured `Logger`.
"""

import logging

from argparse import ArgumentParser
from logging import Logger
from rich.console import Console
from rich.logging import RichHandler


def get_argument_parser() -> ArgumentParser:
    """
    Provide an instance of the CLI arguments paraser.

    Returns:
        ArgumentParser: Configured instance of argument parser.
    """
    arg_parser = ArgumentParser(
        prog='knowledge_verificator',
    )

    arg_parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        default=False,
        help=(
            'Turn on debug mode, which shows all logs including those from '
            '`debug` and `info` levels.'
        ),
    )

    arg_parser.add_argument(
        '-e',
        '--experiments',
        action='store_true',
        default=False,
        help='Run experiments instead of running an interactive mode.',
    )

    return arg_parser


console = Console()
logger = Logger('main_logger')

logging_handler = RichHandler(rich_tracebacks=True)

parser = get_argument_parser()
args = parser.parse_args()

LOGGING_LEVEL = logging.WARNING
if args.debug:
    LOGGING_LEVEL = logging.DEBUG

logging_handler.setLevel(LOGGING_LEVEL)
logger.addHandler(logging_handler)
