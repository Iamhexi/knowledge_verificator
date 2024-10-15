"""
Module handling Input/Output, including parsing CLI arguments, providing
an instance of `rich` console, and an instance of a preconfigured `Logger`.
"""

from argparse import ArgumentParser
from functools import cache
from logging import Logger
from pathlib import Path
from rich.console import Console
from rich.logging import RichHandler

from knowledge_verificator.utils.configuration_parser import (
    Configuration,
    ConfigurationParser,
)


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
def get_config() -> Configuration:
    """
    Get configuration of the system.

    Returns:
        Configuration: Instance of configuration.
    """
    _parser = get_argument_parser()
    args = _parser.parse_args()

    _configuration_parser = ConfigurationParser(configuration_file=args.config)
    config = _configuration_parser.parse_configuration()

    _logging_handler.setLevel(config.logging_level)
    logger.addHandler(_logging_handler)

    return config


console = Console()
logger = Logger('main_logger')

_logging_handler = RichHandler(rich_tracebacks=True)
