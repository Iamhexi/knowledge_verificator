import logging

from logging import Logger
from rich.console import Console
from rich.logging import RichHandler

console = Console()
logger = Logger('main_logger')
# TODO: Take logger level from CLI or config file.


logging_handler = RichHandler(rich_tracebacks=True)
logging_handler.setLevel(logging.DEBUG)
logger.addHandler(logging_handler)
