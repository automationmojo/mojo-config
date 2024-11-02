
__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []


from threading import RLock

from mojo.collections.wellknown import ContextSingleton
from mojo.collections.contextpaths import ContextPaths
from mojo.collections.mergemap import MergeMap

from mojo.credentials.credentialmanager import CredentialManager
from mojo.dataprofiles.dataprofilemanager import DataProfileManager

from mojo.config.configurationmaps import CONFIGURATION_MAPS


CREDENTIAL_MANAGER_SINGLETON = None
DATAPROFILE_MANAGER_SINGLETON = None

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


def DataProfileManagerSingleton() -> DataProfileManager:
    """
        Instantiates and gets a global instance of the :class:`DataProfileManager` class.  The
        :class:`DataProfileManager` provides for management of data source connectivity information profiles.
    """
    global DATAPROFILE_MANAGER_SINGLETON

    if DATAPROFILE_MANAGER_SINGLETON is None:
        SINGLETON_LOCK.acquire()
        try:

            if DATAPROFILE_MANAGER_SINGLETON is None:
                dataprofiles = {}
                if CONFIGURATION_MAPS.LANDSCAPE_CONFIGURATION_MAP is not None and \
                    len(CONFIGURATION_MAPS.LANDSCAPE_CONFIGURATION_MAP) > 0:
                    lscape: MergeMap = CONFIGURATION_MAPS.LANDSCAPE_CONFIGURATION_MAP
                    if "dataprofiles" in lscape:
                        dataprofiles = lscape["dataprofiles"]

                ctx = ContextSingleton()
                landscape_uris = ctx.lookup(ContextPaths.CONFIG_LANDSCAPE_URIS, [])

                profilemgr = DataProfileManager()
                profilemgr.load_datasource_profiles(dataprofiles, source_uris=landscape_uris)
                DATAPROFILE_MANAGER_SINGLETON = profilemgr
                
        finally:
            SINGLETON_LOCK.release()
    
    return DATAPROFILE_MANAGER_SINGLETON
