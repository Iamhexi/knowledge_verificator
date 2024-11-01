"""Main module with CLI definition."""

from pathlib import Path
import subprocess
import sys

import uvicorn
from knowledge_verificator.io_handler import config
from knowledge_verificator.utils.configuration_parser import OperatingMode
from knowledge_verificator.command_line import run_cli_mode
from tests.model.runner import ExperimentRunner


def run_backend() -> None:
    """Run the HTTP backend of the system."""

    uvicorn.run(
        'knowledge_verificator.backend:ENDPOINTS',
        host=config().backend_address,
        port=config().backend_port,
        reload=(not config().production_mode),
    )


def run_frontend() -> subprocess.Popen:
    """Run the built-in frontend of the system."""
    arguments = [
        'npm',
        'run',
        'dev',
        '--',
        '--port',
        str(config().frontend_port),
    ]
    return subprocess.Popen(args=arguments, cwd='frontend')


if __name__ == '__main__':
    match config().mode:
        case OperatingMode.EXPERIMENT:
            experiment_directory = Path(config().experiment_implementation)
            runner = ExperimentRunner(directory=experiment_directory)
            runner.run()
            sys.exit(0)

        case OperatingMode.CLI:
            run_cli_mode()

        case OperatingMode.SERVER:
            run_backend()

        case OperatingMode.CLIENT_SERVER:
            run_frontend()
            run_backend()
