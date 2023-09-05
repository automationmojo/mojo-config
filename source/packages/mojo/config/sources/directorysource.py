
from typing import Dict, Optional, Tuple, Union

import json
import os
import re
import yaml

from mojo.errors.exceptions import ConfigurationError
from mojo.config.configurationformat import ConfigurationFormat
from mojo.config.sources.configurationsourcebase import (
    ConfigurationSourceBase
)


EXTENSION_TO_CONFIG_FORMAT = {
    "yml": ConfigurationFormat.YAML,
    "yaml": ConfigurationFormat.YAML,
    "json": ConfigurationFormat.JSON
}

class DirectorySource(ConfigurationSourceBase):

    schema = "dir"
    parse_exp = re.compile(r"dir://(?P<directory>[/s/S]+)")

    def __init__(self, uri: str, directory: str):
        super().__init__(uri)
        self._directory = os.path.expandvars(os.path.expanduser(directory))
        return

    @classmethod
    def parse(cls, uri: str) -> Union[None, "DirectorySource"]:

        rtnobj = None

        mobj = cls.parse_exp.match(uri)
        if mobj is not None:
            matchinfo = mobj.groupdict()
            directory = matchinfo["directory"]
            rtnobj = DirectorySource(uri, directory)
        else:
            rtnobj = DirectorySource(uri, uri)

        return rtnobj

    def try_load_configuration(self, config_name: str, credentials: Optional[Dict[str, Tuple[str, str]]]) -> Union[Tuple[ConfigurationFormat, dict], Tuple[None, None]]:
        
        config_format = None
        config_info = None

        for ext in ["yaml", "yml", "json"]:
            checkfile = os.path.join(self._directory, f"{config_name}.{ext}")
            if os.path.exists(checkfile):
                config_format = EXTENSION_TO_CONFIG_FORMAT[ext]
                with open(checkfile, 'r') as cf:
                    if config_format == ConfigurationFormat.YAML:
                        config_info = yaml.safe_load(cf)
                        if config_info == None: # We likely encountered an empty config file
                            config_info = {}
                    elif config_format == ConfigurationFormat.JSON:
                        config_info = json.load(cf)
                break

        if config_info is not None:
            config_format = None

        return config_format, config_info
