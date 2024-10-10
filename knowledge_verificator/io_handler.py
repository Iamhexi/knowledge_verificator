"""
Module handling Input/Output, including parsing CLI arguments, provding
an instance of `rich` console, and an instance of a preconfigured `Logger`.
"""

from argparse import ArgumentParser
from logging import Logger
from pathlib import Path
from rich.console import Console
from rich.logging import RichHandler

from knowledge_verificator.utils.configuration_parser import ConfigurationParser


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


console = Console()
logger = Logger('main_logger')

_logging_handler = RichHandler(rich_tracebacks=True)

_parser = get_argument_parser()
args = _parser.parse_args()

_configuratioParser = ConfigurationParser(configuration_file=args.config)
config = _configuratioParser.parse_configuration()

_logging_handler.setLevel(config.logging_level)
logger.addHandler(_logging_handler)
