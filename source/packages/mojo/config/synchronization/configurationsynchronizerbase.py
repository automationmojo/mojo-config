    

__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []

from typing import Tuple, Union


from abc import abstractmethod, ABC

import os

import json
import yaml


class ConfigurationSynchronizerBase(ABC):

    def __init__(self, storage_uri: str, local_store: str):
        """
            Creates a configuration sychronizer.

            :param connection: A connection string that is used to connect to the remote store.
            :param local_store: The path to the local root configuration directory. 
        """
        self._storage_uri = storage_uri
        self._local_store = local_store
        return
    
    @property
    def storage_uri(self):
        return self._storage_uri
    
    @property
    def local_store(self):
        return self._local_store
    
    @abstractmethod
    def try_publish(self, venue: str, user: str, config_name: str) -> bool:
        return
    
    @abstractmethod
    def try_retrieve(self, venue: str, user: str, config_name: str) -> bool:
        return
    
    def _load_local_config(self, config_class: str, config_name: str) -> Union[Tuple[str, dict], Tuple[None, None]]:

        config_format = None
        config_info = None

        config_file_cand = os.path.join(self._local_store, config_class, f"{config_name}.yaml")
        if os.path.exists(config_file_cand):
            config_file_found = config_file_cand
            with open(config_file_cand, 'r') as cf:
                config_info = yaml.safe_load(cf)
                config_format = "yaml"
        
        if config_file_found is not None:
            config_file_cand = os.path.join(self._local_store, config_class, f"{config_name}.json")
            with open(config_file_cand, 'r') as cf:
                config_info = json.load(cf)
                config_format = "json"

        return config_format, config_info