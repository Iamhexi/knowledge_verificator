"""Module with the parser for YAML configuration files."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any
import yaml  # type: ignore[import-untyped]


class OperatingMode(Enum):
    """
    Available mode of operating for the application.

    These modes mean:
    - EXPERIMENT - implemented experiments on available language models
        are run. These experiments aim at measuring quality of results
        produced by the models.
    - CLI - interactive command-line interface mode.
        It allows a user to perform actions in terminal.
    - BACKEND - an HTTP server is started, which serves as backend.
        Graphical user interface (GUI) in a form of webpage is served
        as frontend.
    """

    EXPERIMENT = 'EXPERIMENT'
    CLI = 'CLI'
    BACKEND = 'BACKEND'


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
    logging_level: str
    mode: OperatingMode
    experiment_implementation: Path
    experiment_results: Path

    def __init__(
        self,
        **kwargs,  # Records received from a YAML file.
    ) -> None:
        # Assign values to attributes.
        for attribute, value in kwargs.items():
            self.__setattr__(attribute, value)

        # Convert to a proper datatypes.
        self.learning_materials: Path = Path(kwargs['learning_materials'])
        self.mode: OperatingMode = OperatingMode(kwargs['mode'])
        self.experiment_implementation = Path(
            kwargs['experiment_implementation']
        )
        self.experiment_results = Path(kwargs['experiment_results'])


class ConfigurationParser:
    """Class, which loads and parses a YAML configuration."""

    def __init__(self, configuration_file: Path | str) -> None:
        """Load a YAML configuration file."""
        self._config_file: Path | None = None
        self._config_data: dict = {}
        self.load_configuration(configuration_path=configuration_file)

    def _load_from_configuration(self) -> None:
        if self._config_file is None:
            raise ValueError(
                'Configuration file was not supplied and has value of None. '
                'Provide a path to the configuration file before parsing it.'
            )
        with open(self._config_file, 'rt', encoding='utf-8') as fd:
            self._config_data = yaml.safe_load(fd)

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

    def load_configuration(self, configuration_path: Path | str) -> None:
        """
        Load a configuration of from a YAML file.

        This method should be used only if you want to:
        - either load a new configuration file,
        - or reload configuration file after it was changed.

        Args:
            configuration_path (Path | str): Path to a YAML configuration file.

        Raises:
            FileNotFoundError: Raised if a configuration file was not found.
        """
        if isinstance(configuration_path, str):
            configuration_path = Path(configuration_path)
        if not configuration_path.exists():
            raise FileNotFoundError(
                f'Configuration file {str(configuration_path)} was not found.'
            )
        self._config_file = configuration_path.resolve()
        self._load_from_configuration()
