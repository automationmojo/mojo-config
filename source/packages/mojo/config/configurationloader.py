
from typing import Dict, List, Optional, Tuple

import os
import json
import yaml
import base64

from cryptography.fernet import Fernet

from mojo.config.sources.configurationsourcebase import ConfigurationSourceBase
from mojo.config.sources.couchdbsource import CouchDBSource
from mojo.config.sources.directorysource import DirectorySource
from mojo.config.sources.mongodbsource import MongoDBSource
from mojo.config.sources.httpsource import HttpSource

from mojo.errors.exceptions import ConfigurationError, SemanticError

from mojo.config.configurationformat import ConfigurationFormat
from mojo.config.cryptography import generate_fernet_key

class ConfigurationLoader:
    """
        The :class:`ConfigurationLoader` provides configuration loading from multiple references and
        source classes.
    """

    def __init__(self, source_uris: List[str], credentials: Optional[Dict[str, Tuple[str, str]]] = None):
        self._source_uris = [uri.strip() for uri in source_uris]
        self._credentials = credentials
        self._sources: List[ConfigurationSourceBase] = []
        self._initialize()
        return

    @property
    def source_uris(self) -> List[str]:
        return self._source_uris

    @property
    def sources(self) -> List[ConfigurationSourceBase]:
        return self._sources

    def load_configuration_from_file(self, config_file: str, key: Optional[str] = None, keyphrase: Optional[str] = None) -> dict:
        """
            Loads a configuration directly from a file.

            :param config_name: The path to the configuration file to load.
            :param key: An optional key to use for encrypted configurations.
            :param keyphrase: An optional phrase to use for generating the decryption key.

            :returns: A deep dictionary containing the configuration that was loaded.
        """

        if key is not None and keyphrase is not None:
            errmsg = "The 'load_configuration' method should be called with either 'key' or 'keyphrase' but not both."
            raise SemanticError(errmsg)

        if keyphrase is not None:
            key = generate_fernet_key(keyphrase)

        config_info = None

        _, fileext = os.path.splitext(config_file)

        if fileext in [".yaml", ".yml"]:
            with open(config_file, 'r') as cf:
                config_info = yaml.safe_load(cf)
        elif fileext == ".json":
            with open(config_file, 'r') as cf:
                config_info = json.load(cf)

        if "encrypted_content" in config_info:
            if "format" in config_info:
                config_format = config_info["format"]

            decryptor = Fernet(key)
            
            encrypted_content = base64.b64decode(config_info["encrypted_content"])
            
            plain_content = decryptor.decrypt(encrypted_content).decode('utf-8')

            if config_format == ConfigurationFormat.YAML:
                config_info = yaml.safe_load(plain_content)
            elif config_format == ConfigurationFormat.JSON:
                config_info = json.loads(plain_content)
            else:
                errmsg = "UnExpected error parsing decrypted configuration content.  Un-supported format."
                raise ConfigurationError(errmsg)

        return config_info

    def load_configuration_by_name(self, config_name: str, key: Optional[str] = None, keyphrase: Optional[str] = None) -> Tuple[str, dict]:
        """
            Searches a list of sources to locate a configuration by name and then loads the configuration.

            :param config_name: The name of the configuration to load.
            :param key: An optional key to use for encrypted configurations.
            :param keyphrase: An optional phrase to use for generating the decryption key.

            :returns: A tuple with the uri used to locate the configuration and the configuration found
        """
        
        if key is not None and keyphrase is not None:
            errmsg = "The 'load_configuration' method should be called with either 'key' or 'keyphrase' but not both."
            raise SemanticError(errmsg)

        if keyphrase is not None:
            key = generate_fernet_key(keyphrase)

        config_info = None
        config_format = None
        config_uri = None

        for src in self._sources:
            config_format, config_info = src.try_load_configuration(config_name, self._credentials)
            if config_info is not None:
                config_uri = f"{src.uri}/{config_name}"
                break

        if config_info is None:
            errmsg_list = [
                f"Unable to locate configuration name='{config_name}'",
                "CHECKED SOURCES:"
            ]

            for uri in self.source_uris:
                errmsg_list.append(f"    {uri}")

            errmsg = os.linesep.join(errmsg_list)
            raise ConfigurationError(errmsg)

        if "encrypted_content" in config_info:

            if "format" in config_info:
                config_format = config_info["format"]

            decryptor = Fernet(key)
            
            encrypted_content = base64.b64decode(config_info["encrypted_content"])
            
            plain_content = decryptor.decrypt(encrypted_content).decode('utf-8')

            if config_format == ConfigurationFormat.YAML:
                config_info = yaml.safe_load(plain_content)
            elif config_format == ConfigurationFormat.JSON:
                config_info = json.loads(plain_content)
            else:
                errmsg = "UnExpected error parsing decrypted configuration content.  Un-supported format."
                raise ConfigurationError(errmsg)

        return config_uri, config_info

    def _initialize(self):

        for uri in self._source_uris:
            if uri.startswith(CouchDBSource.scheme):
                src = CouchDBSource.parse(uri)

                if src is None:
                    errmsg = f"CouchDBSource encountered an error parsing configuration source uri='{uri}'"
                    raise ConfigurationError(errmsg)

                self._sources.append(src)

            elif uri.startswith(MongoDBSource.scheme):
                src = MongoDBSource.parse(uri)
                
                if src is None:
                    errmsg = f"MongoDBSource encountered an error parsing configuration source uri='{uri}'"
                    raise ConfigurationError(errmsg)
                
                self._sources.append(src)

            elif uri.startswith(HttpSource.scheme) or uri.startswith("https"):
                src = HttpSource.parse(uri)
                
                if src is None:
                    errmsg = f"HttpSource encountered an error parsing configuration source uri='{uri}'"
                    raise ConfigurationError(errmsg)
                
                self._sources.append(src)

            else:
                src = DirectorySource.parse(uri)
                
                if src is None:
                    errmsg = f"DirectorySource encountered an error parsing configuration source uri='{uri}'"
                    raise ConfigurationError(errmsg)

                self._sources.append(src)

        return