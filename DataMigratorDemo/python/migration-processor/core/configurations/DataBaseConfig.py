import logging

from Core.Configurations import AbstractConfig

LOGGER = logging.getLogger(__name__)


class DataBaseConfig(AbstractConfig):
    def __init__(self, access_config_path: str, job_config_path: str, destination_config_path: str):
        super().__init__(access_config_path, job_config_path, destination_config_path)
        self._url = url
        self._user_name = user_name
        self._password = password
        self._schema_name = schema_name

    def load_job_config(self, job_config) -> None:
        super()._format = (job_config['file_Type'])['file_Type'].upper()
        super()._job_name = job_config['jobName']
        self.source_path = job_config['path']
        # super()._job_version = FIXME in the Config file first