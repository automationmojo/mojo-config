
from typing import Tuple, Union

from abc import abstractmethod, ABC

from mojo.config.configurationformat import ConfigurationFormat

class ConfigurationSourceBase(ABC):

    scheme: str = "not-set"

    def __init__(self, uri: str):
        self._uri = uri
        return

    @property
    def uri(self):
        return self._uri

    @abstractmethod
    def parse(self, uri: str) -> Union[None, "ConfigurationSourceBase"]:
        return

    @abstractmethod
    def try_load_configuration(self, config_name: str) -> Union[Tuple[ConfigurationFormat, dict], Tuple[None, None]]:
        return
