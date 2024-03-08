
__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import TYPE_CHECKING

from threading import RLock

from mojo.collections.wellknown import ContextSingleton
from mojo.collections.contextpaths import ContextPaths
from mojo.credentials.credentialmanager import CredentialManager
from mojo.config.configurationmaps import CONFIGURATION_MAPS


CREDENTIAL_MANAGER_SINGLETON = None


SINGLETON_LOCK = RLock()


def CredentialManagerSingleton() -> CredentialManager:
    """
        Instantiates and gets a global instance of the :class:`CredentialManager` class.  The
        :class:`CredentialManager` provides for management of credentials.
    """
    global CREDENTIAL_MANAGER_SINGLETON

    if CREDENTIAL_MANAGER_SINGLETON is None:
        SINGLETON_LOCK.acquire()
        try:

            if CREDENTIAL_MANAGER_SINGLETON is None:
                credential_info = {}
                if CONFIGURATION_MAPS.CREDENTIAL_CONFIGURATION_MAP is not None and \
                    len(CONFIGURATION_MAPS.CREDENTIAL_CONFIGURATION_MAP) > 0:
                    credential_info = CONFIGURATION_MAPS.CREDENTIAL_CONFIGURATION_MAP

                ctx = ContextSingleton()
                credential_uris = ctx.lookup(ContextPaths.CONFIG_CREDENTIAL_URIS, [])

                credmgr = CredentialManager()
                credmgr.load_credentials(credential_info, source_uris=credential_uris)
                CREDENTIAL_MANAGER_SINGLETON = credmgr
                
        finally:
            SINGLETON_LOCK.release()
    
    return CREDENTIAL_MANAGER_SINGLETON
