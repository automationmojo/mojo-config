

__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []

from typing import Dict, Tuple, Union

import re

from urllib.parse import quote_plus

from mojo.errors.exceptions import ConfigurationError

from mojo.config.synchronization.configsynchronizerbase import ConfigSynchronizerBase

class MongoDbConfigSynchronizer(ConfigSynchronizerBase):
    """
        A directory configuration synchronizer.
    """

    scheme = "mongodb"
    parse_exp = re.compile(r"mongodb://(?P<host>[a-zA-Z\.0-9\-]+)/(?P<database>[a-zA-Z\.0-9\-]+)")

    def __init__(self, storage_uri: str, scheme: str, host: str, port: Union[int, None], database: str, verify_certificate: bool = True):
        super().__init__(storage_uri)

        self._scheme = scheme
        self._host = host
        self._port = port
        self._database = database
        self._verify_certificate = verify_certificate
        return

    @classmethod
    def parse(cls, uri: str, verify_certificate: bool = True) -> Union[None, "MongoDbConfigSynchronizer"]:

        rtnobj = None

        mobj = cls.parse_exp.match(uri)
        if mobj is not None:
            try:
                import pymongo
            except ImportError:
                errmsg = "You must install the 'pymongo' module in order to use couchdb sources."
                raise ConfigurationError(errmsg)

            matchinfo = mobj.groupdict()

            scheme = matchinfo["scheme"]
            host = matchinfo["host"]

            port = None
            if "port" in matchinfo and matchinfo["port"] is not None:
                port = int(matchinfo["port"].lstrip(":"))
            
            database = matchinfo["database"]

            rtnobj = MongoDbConfigSynchronizer(uri, scheme, host, port, database, verify_certificate=verify_certificate)

        return rtnobj

    def _publish_configuration(self, venue: str, user: str, config_class: str, config_name: str, config_format: str, config_info: str, credentials: Dict[str, Tuple[str, str]]):
        
        username, password = credentials[self._host]
        dburi = f"mongodb+srv://{username}:{quote_plus(password)}@{self._host}/?retryWrites=true&w=majority"

        document_name = f"{config_class}-{user}-{config_name}"

        document_info = {
            "_id": document_name,
            "format": config_format,
            "config": config_info
        }

        import pymongo

        client = pymongo.MongoClient(dburi)

        try:
            db = client[self._database]

            collection = db[venue]
            
            collection.insert_one(document_info)
        finally:
            client.close()

        return
    
    def _retrieve_configuration(self, venue: str, user: str, config_class: str, config_name: str, credentials: Dict[str, Tuple[str, str]]) -> Union[Tuple[str, dict], Tuple[None, None]]:
        
        config_format = None
        config_info = None

        username, password = credentials[self._host]
        dburi = f"mongodb+srv://{username}:{quote_plus(password)}@{self._host}/?retryWrites=true&w=majority"

        document_name = f"{config_class}-{user}-{config_name}"

        import pymongo

        client = pymongo.MongoClient(dburi, tlsAllowInvalidCertificates=self._verify_certificate)

        try:
            db = client[self._database]

            collection = db[venue]

            document_info = collection.find_one({"_id": config_name})

            config_format = document_info["format"]
            config_info = document_info["config"]
        finally:
            client.close()

        return config_format, config_info