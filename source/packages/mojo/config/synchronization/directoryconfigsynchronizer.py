

__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []

from typing import Tuple, Union

import json
import os
import re
import yaml

from mojo.config.synchronization.configsynchronizerbase import ConfigSynchronizerBase

class DirectoryConfigSynchronizer(ConfigSynchronizerBase):
    """
        A directory configuration synchronizer.
    """

    scheme = "dir"
    parse_exp = re.compile(r"dir://(?P<directory>[/s/S]+)")

    def __init__(self, storage_uri: str, local_store: str):
        super().__init__(storage_uri)
        return


    def _retrieve_configuration(self, venue: str, user: str, config_class: str, config_name: str) -> Union[Tuple[str, dict], Tuple[None, None]]:

        config_format = None
        config_info = None

        storage_dir = os.path.join(self._storage_uri, venue, user, config_class)
        if os.path.exists(storage_dir):

            config_cand = os.path.join(storage_dir, f"{config_name}.json")
            if os.path.exists(config_cand):
                with open(config_cand, 'r') as cf:
                    config_info = json.load(cf)
                    config_format = "json"

            config_cand = os.path.join(storage_dir, f"{config_name}.yaml")
            if os.path.exists(config_cand):
                with open(config_cand, 'r') as cf:
                    config_info = yaml.safe_load(cf)
                    config_format = "yaml"

        return config_format, config_info


    def _publish_configuration(self, venue: str, user: str, config_class: str, config_name: str, config_format: str, config_info: str):

        storage_dir = os.path.join(self._storage_uri, venue, user, config_class)
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

        dest_file = os.path.join(storage_dir, f"{config_name}.{config_format}")
        with open(dest_file, 'w+') as cf:
            if config_format == "json":
                json.dump(config_info, cf, indent=4)
            elif config_format == "yaml":
                yaml.dump(config_info, cf, indent=4)
            else:
                errmsg = f"Unknown configuration format config_format={config_format}"
                raise ValueError(errmsg)

        return
