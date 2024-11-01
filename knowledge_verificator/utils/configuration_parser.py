"""Module with the parser for YAML configuration files."""

from dataclasses import dataclass
from enum import Enum
import logging
from pathlib import Path
import sys
from typing import Any
import yaml  # type: ignore[import-untyped]

from knowledge_verificator.nli import NaturalLanguageInferenceModel
from knowledge_verificator.qg.qg_model_factory import (
    QuestionGenerationModel,  # type: ignore[import-untyped]
)


class OperatingMode(Enum):
    """
    Available mode of operating for the application.

    These modes mean:
    - EXPERIMENT - implemented experiments on available language models
        are run. These experiments aim at measuring quality of results
        produced by the models.
    - CLI - interactive command-line interface mode.
        It allows a user to perform actions in terminal.
    - CLIENT_SERVER - an HTTP server is started, which serves as the
        backend. Graphical user interface (GUI) in a form of webpage
        is served as the frontend.
    - SERVER - an HTTP server is started as an API. The built-in
        frontend is not used. This is useful if one wants to build
        a custom frontend for the existing backend.
    """

    EXPERIMENT = 'EXPERIMENT'
    CLI = 'CLI'
    CLIENT_SERVER = 'CLIENT_SERVER'
    SERVER = 'SERVER'


@dataclass
class Configuration:
    """
    A dataclass storing a parsed configuration.

    Names of the attributes are used in this database are used in
    a YAML configuration file.

    Attributes:
        learning_materials (Path): Path to a directory containing learning materials.
        logging_level (str): One of `DEBUG`, `INFO`, `WARNING`, `ERROR`,
            `CRITICAL`. Minimal level of a message to be logged.
        mode (OperatingMode): Operating mode of application. Different mode serve
            different purposes.
        experiment_implementation (Path): Path to a directory containing
            implementation of experiments on language models.
        experiment_results (Path): Path to a directory, where results
            should be saved.
    """

    learning_materials: Path
    experiment_implementation: Path
    experiment_results: Path
    question_generation_model: QuestionGenerationModel
    natural_language_inference_model: NaturalLanguageInferenceModel
    logging_level: str = 'WARNING'
    mode: OperatingMode = OperatingMode.CLIENT_SERVER
    production_mode: bool = True
    backend_address: str = '127.0.0.1'
    backend_port: int = 8000
    frontend_address: str = '127.0.0.1'
    frontend_port: int = 3000
    protocol: str = 'http'

    def __post_init__(self) -> None:
        logger = logging.Logger('Configuration parser', level=logging.DEBUG)
        # Convert to a proper datatypes.
        try:
            if not isinstance(self.natural_language_inference_model, str):
                raise ValueError(
                    'Incorrect value for `natural_language_inference_model` '
                    'configuration option: '
                    f'{self.natural_language_inference_model}.'
                )

            self.natural_language_inference_model = (
                NaturalLanguageInferenceModel[
                    self.natural_language_inference_model.upper()  # pylint: disable=no-member
                ]
            )

        except KeyError as e:
            logger.critical(
                'Unknown configuration option for `natural_language_inference`: %s.',
                e,
            )
            sys.exit(1)

        try:
            if not isinstance(self.question_generation_model, str):
                raise ValueError(
                    'Incorrect value for `question_generation_model` '
                    'configuration option: '
                    f'{self.question_generation_model}.'
                )
            self.question_generation_model = QuestionGenerationModel[
                self.question_generation_model.upper()  # pylint: disable=no-member
            ]
        except KeyError as e:
            logger.critical(
                'Unknown configuration option for `question_generation_model`: %s.',
                e,
            )
            sys.exit(1)

        self.mode: OperatingMode = OperatingMode(self.mode)
        self.experiment_implementation = Path(self.experiment_implementation)
        self.experiment_results = Path(self.experiment_results)


class ConfigurationParser:
    """Class, which loads and parses a YAML configuration."""

    def __init__(self, configuration_file: Path) -> None:
        """
        Load a YAML configuration file and, optionally, re-create a JS file
        with the most current configuration.
        """
        self._config_file: Path | None = None
        self._config_data: dict = {}
        self.load_configuration(configuration_file)

        # Update configuration for the built-in frontend only.
        config = self.parse_configuration()
        if config.mode == OperatingMode.CLIENT_SERVER:
            self.update_javascript_configuration(
                Path('frontend/src/lib/config.js')
            )

    def update_javascript_configuration(self, js_config: Path) -> None:
        """
        Re-create a JavaScript configuration file to be compliant
        with a YAML configuration.

        Create a JavaScript configuration file with a constant API_URL, which
        supplies an URL to backend for the frontend.

        Args:
            js_config (Path): Path to a JavaScript configuration file.
        """

        backend_address = self._config_data['backend_address']
        backend_port = self._config_data['backend_port']
        protocol = self._config_data['protocol']
        js_config_content = f"export const API_URL = '{protocol}://{backend_address}:{backend_port}'; // Do not edit manually.\n"

        with open(js_config.resolve(), 'wt', encoding='utf-8') as fd:
            fd.write(js_config_content)

    def parse_configuration(self) -> Configuration:
        """
        Parse the previously loaded YAML configuration file to an instance
        of `Configuration`.

        Returns:
            Configuration: Parsed configuration of the application.
        """
        configuration_arguments: dict[str, Any] = {}
        # Attributes of `Configuration` are YAML keys.
        for option_name, _ in Configuration.__annotations__.items():
            configuration_arguments[option_name] = self._config_data[
                option_name
            ]

        # Feed key, value pairs to constructor.
        return Configuration(**configuration_arguments)

    def load_configuration(self, configuration_path: Path) -> None:
        """
        Load a configuration from a YAML file.

        This method should be used only if you want to:
        - either load a new configuration file,
        - or reload configuration file after it was changed.

        Args:
            configuration_path (Path): Path to a YAML configuration file.

        Raises:
            ValueError: Raised if a configuration file is inaccessible due
                to an incorrect path, denied access, not having it set up, or
                some other reason.
        """
        self._config_file = configuration_path.resolve()
        if self._config_file is None:
            raise ValueError(
                'Configuration file was not supplied and has value of None. '
                'Provide a path to the configuration file before parsing it.'
            )
        with open(self._config_file, 'rt', encoding='utf-8') as fd:
            self._config_data = yaml.safe_load(fd)
