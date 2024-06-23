import logging

from core.configurations import AbstractAccessConfig

LOGGER = logging.getLogger(__name__)


class Secret(AbstractAccessConfig):
    def _read_config(self, config: dict) -> None:
        self._url = ((config['config'])['secret'])['url']
        self._access_key = ((config['config'])['secret'])['access_key']
        self._secret_key = ((config['config'])['secret'])['secret_key']
