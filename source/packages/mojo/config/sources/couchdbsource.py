
from typing import Dict, Optional, Tuple, Union

import re
import traceback

from mojo.errors.exceptions import ConfigurationError
from mojo.config.configurationformat import ConfigurationFormat
from mojo.config.sources.configurationsourcebase import (
    ConfigurationSourceBase
)

class CouchDBSource(ConfigurationSourceBase):

    scheme = "couchdb"
    parse_exp = re.compile(r"couchdb://(?P<scheme>[htps]+)\+(?P<host>[a-zA-Z\.0-9\-]+)(?P<port>[:0-9]+)*/(?P<database>[a-zA-Z\.0-9\-]+)")

    def __init__(self, uri: str, cscheme: str, host: str, database: str, port: Optional[int]):
        super().__init__(uri)
        self._cscheme = cscheme
        self._host = host
        self._database = database
        self._port = port
        return

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
    def parse(cls, uri: str) -> Union[None, "CouchDBSource"]:

        rtnobj = None

        mobj = cls.parse_exp.match(uri)
        if mobj is not None:
            try:
                import couchdb
            except ImportError:
                errmsg = "You must install the 'couchdb' module in order to use couchdb sources."
                raise ConfigurationError(errmsg)

            matchinfo = mobj.groupdict()

            cscheme = matchinfo["scheme"]
            host = matchinfo["host"]

            port = None
            if "port" in matchinfo and matchinfo["port"] is not None:
                port = int(matchinfo["port"].lstrip(":"))
            
            database = matchinfo["database"]

            rtnobj = CouchDBSource(uri, cscheme, host, database, port)

        return rtnobj
    
    def try_load_configuration(self, config_name: str, credentials: Dict[str, Tuple[str, str]]) -> Union[Tuple[ConfigurationFormat, dict], Tuple[None, None]]:
        
        config_info = None
        config_format = None

        try:
            dburi = None
            
            if self._port is not None:
                dburi = f"{self._cscheme}://{self._host}:{self._port}/{self._database}"
            else:
                dburi = f"{self._cscheme}://{self._host}/{self._database}"

            import couchdb

            db = couchdb.Database(dburi)

            if credentials is not None and self._host in credentials:
                username, password = credentials[self._host]
                db.resource.credentials = (username, password)

            config_info = db.get(config_name)
            config_format = ConfigurationFormat.JSON

        except:
            errmsg = traceback.format_exc()
            print(errmsg)
            config_info = None

        return config_format, config_info
