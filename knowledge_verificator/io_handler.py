import logging

from logging import Logger
from rich.console import Console
from rich.logging import RichHandler
from argparse import ArgumentParser


def get_argument_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog='knowledge_verificator',
    )

    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help=(
            'Turn on debug mode, which shows all logs including those from '
            '`debug` and `info` levels.'
        ),
    )

    return parser


console = Console()
logger = Logger('main_logger')

logging_handler = RichHandler(rich_tracebacks=True)

parser = get_argument_parser()
args = parser.parse_args()

logging_level = logging.WARNING
if args.debug:
    logging_level = logging.DEBUG

logging_handler.setLevel(logging_level)
logger.addHandler(logging_handler)
