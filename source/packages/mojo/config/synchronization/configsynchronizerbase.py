    

__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []

from typing import Dict, List, Optional, Tuple, Union


from abc import abstractmethod, ABC

import os

import json
import yaml


class ConfigSynchronizerBase(ABC):

    def __init__(self, storage_uri: str):
        """
            Creates a configuration sychronizer.

            :param connection: A connection string that is used to connect to the remote store.
            :param local_store: The path to the local root configuration directory. 
        """
        self._storage_uri = storage_uri
        return
    
    @property
    def storage_uri(self):
        return self._storage_uri
    
    def try_publish(self, local_store: str, venue: str, user: str, config_name: str, credentials: Optional[Dict[str, Tuple[str, str]]] = None) -> List[str]:

        errors = []

        try:
            config_format, config_info = self._load_local_config("landscapes", config_name)
            if config_format is not None:
                self._publish_configuration(venue, user, "landscapes", config_name, config_format, config_info, credentials=credentials)
        except Exception as xcpt:
            errors.append(str(xcpt))

        try:
            config_format, config_info = self._load_local_config("topologies", config_name)
            if config_format is not None:
                self._publish_configuration(venue, user, "topologies", config_name, config_format, config_info, credentials=credentials)
        except Exception as xcpt:
            errors.append(str(xcpt))

        try:
            config_format, config_info = self._load_local_config("runtimes", config_name)
            if config_format is not None:
                self._publish_configuration(venue, user, "runtimes", config_name, config_format, config_info, credentials=credentials)
        except Exception as xcpt:
            errors.append(str(xcpt))

        try:
            config_format, config_info = self._load_local_config("credentials", config_name)
            if config_format is not None:
                self._publish_configuration(venue, user, "credentials", config_name, config_format, config_info, credentials=credentials)
        except Exception as xcpt:
            errors.append(str(xcpt))

        return errors
    

    def try_retrieve(self, local_store: str, venue: str, user: str, config_name: str, credentials: Optional[Dict[str, Tuple[str, str]]] = None) -> bool:

        errors = []

        try:
            config_format, config_info = self._retrieve_configuration(venue, user, "landscapes", config_name, credentials=credentials)
            if config_format is not None:
                self._save_local_config(local_store, venue, user, "landscapes", config_name, config_format, config_info)
        except Exception as xcpt:
            errors.append(str(xcpt))
        
        try:
            config_format, config_info = self._retrieve_configuration(venue, user, "topologies", config_name, credentials=credentials)
            if config_format is not None:
                self._save_local_config(local_store, venue, user, "topologies", config_name, config_format, config_info)
        except Exception as xcpt:
            errors.append(str(xcpt))
        
        try:
            config_format, config_info = self._retrieve_configuration(venue, user, "runtimes", config_name, credentials=credentials)
            if config_format is not None:
                self._save_local_config(local_store, venue, user, "runtimes", config_name, config_format, config_info)
        except Exception as xcpt:
            errors.append(str(xcpt))
        
        try:
            config_format, config_info = self._retrieve_configuration(venue, user, "credentials", config_name, credentials=credentials)
            if config_format is not None:
                self._save_local_config(local_store, venue, user, "credentials", config_name, config_format, config_info)
        except Exception as xcpt:
            errors.append(str(xcpt))

        return errors
    
    def _load_local_config(self, local_store, config_class: str, config_name: str) -> Union[Tuple[str, dict], Tuple[None, None]]:

        config_format = None
        config_info = None

        config_file_cand = os.path.join(local_store, config_class, f"{config_name}.yaml")
        if os.path.exists(config_file_cand):
            config_file_found = config_file_cand
            with open(config_file_cand, 'r') as cf:
                config_info = yaml.safe_load(cf)
                config_format = "yaml"
        
        if config_file_found is not None:
            config_file_cand = os.path.join(local_store, config_class, f"{config_name}.json")
            with open(config_file_cand, 'r') as cf:
                config_info = json.load(cf)
                config_format = "json"

        return config_format, config_info
    
    @abstractmethod
    def _publish_configuration(self, venue: str, user: str, config_class: str, config_name: str, config_format: str, config_info: str, credentials: Dict[str, Tuple[str, str]]):
        return

    @abstractmethod
    def _retrieve_configuration(self, venue: str, user: str, config_class: str, config_name: str,  credentials: Dict[str, Tuple[str, str]]) -> Union[Tuple[str, dict], Tuple[None, None]]:
        return

    def _save_local_config(self, local_store: str, venue: str, user: str, config_class: str, config_name: str, config_format: str, config_info):

        if not os.path.exists(local_store):
            os.makedirs(local_store)

        local_config_dir = os.path.join(local_store, config_class)
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