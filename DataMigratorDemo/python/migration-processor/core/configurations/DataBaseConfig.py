import logging

from core.configurations import AbstractConnectorConfig

LOGGER = logging.getLogger(__name__)


class DataBaseConfig(AbstractConnectorConfig):


    def _read_config(self, config: dict) -> None:
        self._url = url
        self._user_name = user_name
        self._password = password
        self._schema_name = schema_name

    def load1(self, job_config) -> None:
        super()._format = (job_config['file_Type'])['file_Type'].upper()
        super()._job_name = job_config['jobName']
        self.source_path = job_config['path']
        # super()._job_version = FIXME in the Config file first

