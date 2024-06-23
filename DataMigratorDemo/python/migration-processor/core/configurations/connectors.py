import logging

from core.configurations import AbstractConnectorConfig, ConfigType

LOGGER = logging.getLogger(__name__)


class FileSystemConfig(AbstractConnectorConfig):
    def __init__(self,config_type: ConfigType, config_path: str):
        super().__init__(config_type, config_path)
        self._path: str = ""
    def _read_config(self, config: dict) -> None:
        pass



# def __init__(self, access_config_path: str, job_config_path: str, destination_config_path: str):
    #     super().__init__(access_config_path, job_config_path, destination_config_path)
    #     self.source_path: str | None = None
    #
    # def load(self, job_config) -> None:
    #     super()._format = (job_config['file_Type'])['file_Type'].upper()
    #     super()._job_name = job_config['jobName']
    #     self.source_path = job_config['path']
    #     # super()._job_version = FIXME in the Config file first
