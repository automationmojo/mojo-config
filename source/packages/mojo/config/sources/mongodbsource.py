
from typing import Tuple, Union

import re

from mojo.errors.exceptions import ConfigurationError
from mojo.config.configurationformat import ConfigurationFormat
from mojo.config.sources.configurationsourcebase import (
    ConfigurationSourceBase
)

class MongoDBSource(ConfigurationSourceBase):

    schema = "mongodb"
    parse_exp = re.compile(r"couchdb://(?P<host>[a-zA-Z\.0-9\-]+)/(?P<database>[a-zA-Z\.0-9\-]+)/(?P<catagory>[a-zA-Z\.0-9\-]+)")

    def __init__(self, uri: str, host: str, port: int, database: str, category: str):
        super().__init__(uri)
        self._host = host
        self._port = port
        self._database = database
        self._category = category
        return
    
    @property
    def category(self) -> str:
        return self._category

    @property
    def database(self) -> str:
        return self._database

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @classmethod
    def parse(cls, uri: str) -> Union[None, "MongoDBSource"]:

        rtnobj = None

        mobj = cls.parse_exp.match(uri)
        if mobj is not None:
            try:
                import pymongo
            except ImportError:
                errmsg = "You must install the 'pymongo' module in order to use mongodb sources."
                raise ConfigurationError(errmsg)

            matchinfo = mobj.groupdict()
            host = matchinfo["host"]
            port = matchinfo["port"]
            database = matchinfo["database"]
            category = matchinfo["category"]
            rtnobj = MongoDBSource(uri, host, port, database, category)

        return rtnobj

    def try_load_configuration(self, config_name: str) -> Union[Tuple[ConfigurationFormat, str], Tuple[None, None]]:
        
        config_format = None
        config_content = None

        return config_format, config_content
