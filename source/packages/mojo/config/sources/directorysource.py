
from typing import Tuple, Union

import re

from mojo.errors.exceptions import ConfigurationError
from mojo.config.configurationformat import ConfigurationFormat
from mojo.config.sources.configurationsourcebase import (
    ConfigurationSourceBase
)

class DirectorySource(ConfigurationSourceBase):

    schema = "dir"
    parse_exp = re.compile(r"dir://(?P<directory>[/s/S]+)")

    def __init__(self, uri: str, directory: str):
        super().__init__(uri)
        self._directory = directory
        return

    @classmethod
    def parse(cls, uri: str) -> Union[None, "DirectorySource"]:

        rtnobj = None

        mobj = cls.parse_exp.match(uri)
        if mobj is not None:
            matchinfo = mobj.groupdict()
            directory = matchinfo["directory"]
            rtnobj = DirectorySource(uri, directory)

        return rtnobj

    def try_load_configuration(self, config_name: str) -> Union[Tuple[ConfigurationFormat, str], Tuple[None, None]]:
        
        config_format = None
        config_content = None

        return config_format, config_content
