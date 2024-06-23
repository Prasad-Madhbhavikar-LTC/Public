__all__ = [
    'ConfigType',
    'AbstractConfig',
    'AbstractAccessConfig',
    'AbstractJobConfig',
    'AbstractConnectorConfig',
    'connectors',
    # 'DataBaseConfig'
]

import calendar
import logging
import time
from abc import ABC, abstractmethod
from enum import auto, Enum

import yaml

LOGGER = logging.getLogger(__name__)


class ConfigType(Enum):
    ACCESS = auto()
    SOURCE = auto()
    DESTINATION = auto()
    JOB = auto()


class AbstractConfig(ABC):
    def __init__(self, config_type: ConfigType, config_path: str):
        super().__init__()
        self.__config_type: ConfigType = config_type
        self.__config_path: str = config_path
        self._sign: str = ""
        self._version: str = f"0.0.{calendar.timegm(time.gmtime())}"

    def load(self) -> bool:
        try:
            with open(self.__config_path, "r") as file:
                config = yaml.safe_load(file)
                self._read_config(config)
                self._version = config['version']
                self._sign = config['sign']

                return self.__evaluate_signature(self._sign)
        except FileNotFoundError as exc:
            LOGGER.error("File not found: %s", self.__config_path, exc_info=exc)
        except yaml.YAMLError as exc:
            LOGGER.error("Error parsing YAML file: %s", self.__config_path, exc_info=exc)

    def __evaluate_signature(self, signature: str) -> bool:
        # FIXME: Evaluate and compare the signature
        return True

    @abstractmethod
    def _read_config(self, config: dict) -> None:
        raise NotImplementedError("Subclass must implement _read_config() method")


class AbstractAccessConfig(AbstractConfig):
    def __init__(self, config_path: str):
        super().__init__(ConfigType.ACCESS, config_path)

    @abstractmethod
    def _read_config(self, config: dict) -> None:
        raise NotImplementedError("Subclass must implement _read_config() method")


class AbstractConnectorConfig(AbstractConfig):
    def __init__(self, config_type: ConfigType, config_path: str):
        super().__init__(config_type, config_path)

    @abstractmethod
    def _read_config(self, config: dict) -> None:
        pass


class AbstractJobConfig(AbstractConfig):
    def __init__(self, config_path: str):
        super().__init__(ConfigType.ACCESS, config_path)

    @abstractmethod
    def _read_config(self, config: dict) -> None:
        pass


class ConfigLoader(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ConfigLoader, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def read(access_config_path: str, job_config_path: str, destination_config_path: str) -> AbstractConfig:
        pass
#         config: AbstractConfig1
#
#         try:
#             with open(job_config_path, "r") as file:
#                 job_data = yaml.safe_load(file)
#                 match job_data['file_Type'].upper():
#                     case Format.CSV:
#                         config = FileSystemConfig(access_config_path, job_config_path, destination_config_path)
#                     case Format.TABLE:
#                         config = DataBaseConfig(access_config_path, job_config_path, destination_config_path)
#                     case Format.UNSUPPORTED | _:
#                         raise ValueError(f"Config for {format} format not supported")
#                 config.load(job_data)
#
#         except FileNotFoundError as exc:
#             LOGGER.error("File not found: %s", job_config_path, exc_info=exc)
#         except yaml.YAMLError as exc:
#             LOGGER.error("Error parsing YAML file: %s", job_config_path, exc_info=exc)
#
#         return config
