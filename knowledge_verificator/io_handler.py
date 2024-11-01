"""
Module handling Input/Output, including parsing CLI arguments, providing
an instance of `rich` console, and an instance of a preconfigured `Logger`.
"""

from argparse import ArgumentParser
from functools import cache
from logging import Logger
from pathlib import Path
import sys
from rich.console import Console
from rich.logging import RichHandler
from rich.markup import escape

from knowledge_verificator.utils.configuration_parser import (
    Configuration,
    ConfigurationParser,
)

console = Console()


def get_argument_parser() -> ArgumentParser:
    """
    Provide an instance of the CLI arguments parser.

    Returns:
        ArgumentParser: Configured instance of argument parser.
    """
    arg_parser = ArgumentParser(
        prog='knowledge_verificator',
        description='The system of knowledge verificator facilitating self-study.',
    )

    arg_parser.add_argument(
        '-c',
        '--config',
        default=Path('config.yaml'),
        action='store',
        type=Path,
        help=(
            'Path to a YAML configuration file that contain configuration '
            'of the system.'
        ),
    )

    return arg_parser


@cache
def config() -> Configuration:
    """
    Get configuration of the system.

    Returns:
        Configuration: Instance of configuration.
    """
    _parser = get_argument_parser()
    args = _parser.parse_args()

    _configuration_parser = ConfigurationParser(configuration_file=args.config)
    configuration = _configuration_parser.parse_configuration()

    _logging_handler.setLevel(configuration.logging_level)
    logger.addHandler(_logging_handler)

    if configuration.production_mode:

        def handle_exceptions_in_production_mode(
            exception_type, exception, traceback
        ):
            """
            An exception handler for production mode, which hides
            exception_type (the first argument) and traceback
            (the third argument) whilst printing erros in bold red
            text.
            """
            console.print(
                f'[bold red]The error has occured: {escape(str(exception))}. [/bold red]'
            )
            console.print(
                'Closing the application to prevent unexpected consequences.'
            )

        sys.excepthook = handle_exceptions_in_production_mode

    return configuration


logger = Logger('main_logger')

_logging_handler = RichHandler(rich_tracebacks=True)
