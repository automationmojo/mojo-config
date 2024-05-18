

__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []

from typing import List, Tuple, Union

import json
import os
import shutil
import yaml

from mojo.config.synchronization.configurationsynchronizerbase import ConfigurationSynchronizerBase

class DirectorySynchronizer(ConfigurationSynchronizerBase):
    """
        A directory configuration synchronizer.
    """

    def __init__(self, storage_uri: str, local_store: str):
        super().__init__(storage_uri, local_store)
        return

    def try_publish(self, venue: str, user: str, config_name: str) -> List[str]:

        errors = []

        try:
            config_format, config_info = self._load_local_config("landscapes", config_name)
            if config_format is not None:
                self._publish_configuration(venue, user, "landscapes", config_name, config_format, config_info)
        except Exception as xcpt:
            errors.append(str(xcpt))

        try:
            config_format, config_info = self._load_local_config("topologies", config_name)
            if config_format is not None:
                self._publish_configuration(venue, user, "topologies", config_name, config_format, config_info)
        except Exception as xcpt:
            errors.append(str(xcpt))

        try:
            config_format, config_info = self._load_local_config("runtimes", config_name)
            if config_format is not None:
                self._publish_configuration(venue, user, "runtimes", config_name, config_format, config_info)
        except Exception as xcpt:
            errors.append(str(xcpt))

        try:
            config_format, config_info = self._load_local_config("credentials", config_name)
            if config_format is not None:
                self._publish_configuration(venue, user, "credentials", config_name, config_format, config_info)
        except Exception as xcpt:
            errors.append(str(xcpt))

        return errors
    
    def try_retrieve(self, venue: str, user: str, config_name: str) -> bool:

        errors = []

        try:
            config_format, config_info = self._load_stored_config(venue, user, "landscapes", config_name)
            if config_format is not None:
                self._save_configuration(venue, user, "landscapes", config_name, config_format, config_info)
        except Exception as xcpt:
            errors.append(str(xcpt))
        
        try:
            config_format, config_info = self._load_stored_config(venue, user, "topologies", config_name)
            if config_format is not None:
                self._save_configuration(venue, user, "topologies", config_name, config_format, config_info)
        except Exception as xcpt:
            errors.append(str(xcpt))
        
        try:
            config_format, config_info = self._load_stored_config(venue, user, "runtimes", config_name)
            if config_format is not None:
                self._save_configuration(venue, user, "runtimes", config_name, config_format, config_info)
        except Exception as xcpt:
            errors.append(str(xcpt))
        
        try:
            config_format, config_info = self._load_stored_config(venue, user, "credentials", config_name)
            if config_format is not None:
                self._save_configuration(venue, user, "credentials", config_name, config_format, config_info)
        except Exception as xcpt:
            errors.append(str(xcpt))

        return errors
    
    def _load_stored_config(self, venue: str, user: str, config_class: str, config_name: str) -> Union[Tuple[str, dict], Tuple[None, None]]:

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

    def _save_configuration(self, venue: str, user: str, config_class: str, config_name: str, config_format: str, config_info):
        
        config_format = None
        config_info = None

        if not os.path.exists(self._local_store):
            os.makedirs(self._local_store)

        local_config_dir = os.path.join(self._local_store, config_class)
        if not os.path.exists(local_config_dir):
            os.makedirs(local_config_dir)

        local_config_file = os.path.join(local_config_dir, f"{config_name}.{config_format}")
        with open(local_config_file, "w+") as cf:
            if config_format == "json":
                json.dump(config_info, cf, indent=4)
            elif config_format == "yaml":
                yaml.dump(config_info, cf, indent=4)
            else:
                errmsg = f"Unknown configuration format config_format={config_format}"
                raise ValueError(errmsg)

        return