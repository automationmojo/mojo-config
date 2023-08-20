
from typing import List, Optional

import os
import json
import yaml
import base64

from cryptography.fernet import Fernet

from mojo.config.sources.configurationsourcebase import ConfigurationSourceBase
from mojo.config.sources.couchdbsource import CouchDBSource
from mojo.config.sources.directorysource import DirectorySource
from mojo.config.sources.mongodbsource import MongoDBSource

from mojo.errors.exceptions import ConfigurationError

from mojo.config.configurationformat import ConfigurationFormat

class ConfigurationLoader:
    """
        The :class:`ConfigurationLoader` provides configuration loading from multiple references and
        source classes.
    """

    def __init__(self, source_uris: List[str]):
        self._source_uris = [uri.strip() for uri in source_uris]
        self._sources: List[ConfigurationSourceBase] = []
        self._initialize()
        return

    @property
    def source_uris(self) -> List[str]:
        return self._source_uris

    @property
    def sources(self) -> List[ConfigurationSourceBase]:
        return self._sources

    def load_configuration(self, config_name: str, base64_key: Optional[str] = None) -> dict:

        config_content = None
        config_format = None

        for src in self._sources:
            config_content, config_format = src.try_load_configuration(config_name)
            if config_content is not None:
                break

        if config_content is not None:
            errmsg_list = [
                f"Unable to locate configuration name='{config_name}'",
                "CHECKED SOURCES:"
            ]

            for uri in self.source_uris:
                errmsg_list.append(f"    {uri}")

            errmsg = os.linesep.join(errmsg_list)
            raise ConfigurationError(errmsg)

        configinfo = None

        if config_format == ConfigurationFormat.YAML:
            configinfo = yaml.safe_load(config_content)
        elif config_format == ConfigurationFormat.JSON:
            configinfo = json.loads(config_content)
        else:
            errmsg = "UnExpected error parsing configuration content.  Un-supported format."
            raise ConfigurationError(errmsg)

        if "encrypted_content" in configinfo:
            decryption_key = base64.b64decode(base64_key)

            encrypted_content = base64.b64decode(configinfo["encrypted_content"])
            decryptor = Fernet(decryption_key)
            plain_content = decryptor.decrypt(encrypted_content)

            if config_format == ConfigurationFormat.YAML:
                configinfo = yaml.safe_load(plain_content)
            elif config_format == ConfigurationFormat.JSON:
                configinfo = json.loads(plain_content)
            else:
                errmsg = "UnExpected error parsing decrypted configuration content.  Un-supported format."
                raise ConfigurationError(errmsg)

        return configinfo

    def _initialize(self):

        for uri in self._source_uris:
            if uri.startswith(CouchDBSource.schema):
                src = CouchDBSource.parse(uri)

                if src is None:
                    errmsg = f"CouchDBSource encountered an error parsing configuration source uri='{uri}'"
                    raise ConfigurationError(errmsg)

                self._sources.append(src)
            elif uri.startswith(DirectorySource.schema):
                src = DirectorySource.parse(uri)
                
                if src is None:
                    errmsg = f"DirectorySource encountered an error parsing configuration source uri='{uri}'"
                    raise ConfigurationError(errmsg)

                self._sources.append(src)

            elif uri.startswith(MongoDBSource.schema):
                src = MongoDBSource.parse(uri)
                
                if src is None:
                    errmsg = f"MongoDBSource encountered an error parsing configuration source uri='{uri}'"
                    raise ConfigurationError(errmsg)
                
                self._sources.append(src)

            else:
                errmsg = f"Un-Supported configuration source encountered uri='{uri}'"
                raise ConfigurationError(errmsg)

        return