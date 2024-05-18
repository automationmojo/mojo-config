

__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []

from mojo.config.synchronization.configurationsynchronizerbase import ConfigurationSynchronizerBase

class MongoDbSynchronizer(ConfigurationSynchronizerBase):
    """
        A directory configuration synchronizer.
    """

    def __init__(self, connection: str, local_store: str):
        super().__init__(connection, local_store)
        return

    def try_publish(self, user: str, config_name: str) -> bool:
        return
    
    def try_retrieve(self, user: str, config_name: str) -> bool:
        return
