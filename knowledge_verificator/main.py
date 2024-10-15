"""Main module with CLI definition."""

from pathlib import Path
import sys

from knowledge_verificator.io_handler import get_config
from knowledge_verificator.utils.configuration_parser import OperatingMode
from knowledge_verificator.command_line import run_cli_mode
from knowledge_verificator.backend import ENDPOINTS
from tests.model.runner import ExperimentRunner

if __name__ == '__main__':
    config = get_config()
    match config.mode:
        case OperatingMode.EXPERIMENT:
            experiment_directory = Path(config.experiment_implementation)
            runner = ExperimentRunner(directory=experiment_directory)
            runner.run()
            sys.exit(0)

        case OperatingMode.CLI:
            run_cli_mode()

        case OperatingMode.BACKEND:
            import uvicorn

            uvicorn.run(
                ENDPOINTS,
                host='127.0.0.1',
                port=8000,
                reload=(not config.production_mode),
            )
