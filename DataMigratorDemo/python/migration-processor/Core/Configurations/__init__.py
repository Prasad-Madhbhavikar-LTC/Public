__all__ = [
    'ConfigFactory',
    'AbstractConfig',
    'FileSystemConfig',
    'DataBaseConfig'
]

import calendar
import logging
import time
from abc import ABC, abstractmethod

import yaml

from Core import Format
from Core.Configurations.DataBaseConfig import DataBaseConfig
from Core.Configurations.FileSystemConfig import FileSystemConfig

LOGGER = logging.getLogger(__name__)


class AbstractConfig(ABC):
    def __init__(self, access_config_path: str, job_config_path: str, destination_config_path: str):
        self._job_name: str
        self._job_config_path: str = job_config_path
        self._access_config_path: str = access_config_path
        self._destination_config_path: str = destination_config_path
        self._format: Format = Format.UNSUPPORTED
        self.__job_version: str = f"0.0.{calendar.timegm(time.gmtime())}"
        self.__access_version: str = f"0.0.{calendar.timegm(time.gmtime())}"
        self.__destination_version: str = f"0.0.{calendar.timegm(time.gmtime())}"

    @abstractmethod
    def load_job_config(self, job_config) -> None:
        raise NotImplementedError("Subclass must implement load_job_config() method")

    def load_access_config(self, access_config) -> None:
        # TODO: To be implemented
        pass

    def load_destination_config(self, destination_config) -> None:
        # TODO: To be implemented
        pass


class ConfigFactory(object):
    def __new__(cls) -> ConfigFactory:
        if not hasattr(cls, 'instance'):
            cls.instance = super(ConfigFactory, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def read_config(access_config_path: str, job_config_path: str, destination_config_path: str) -> AbstractConfig:
        config: AbstractConfig

        try:
            with open(job_config_path, "r") as file:
                job_data = yaml.safe_load(file)
                match job_data['file_Type'].upper():
                    case Format.CSV:
                        config = FileSystemConfig(access_config_path, job_config_path, destination_config_path)
                    case Format.TABLE:
                        config = DataBaseConfig(access_config_path, job_config_path, destination_config_path)
                    case Format.UNSUPPORTED | _:
                        raise ValueError(f"Config for {format} format not supported")
                config.load_job_config(job_data)

        except FileNotFoundError as exc:
            LOGGER.error("File not found: %s", job_config_path, exc_info=exc)
        except yaml.YAMLError as exc:
            LOGGER.error("Error parsing YAML file: %s", job_config_path, exc_info=exc)

        return config
