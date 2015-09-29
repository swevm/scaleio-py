import json
import requests
from requests.auth import HTTPBasicAuth
from requests_toolbelt import SSLAdapter
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl
import logging
import time
import sys


from pprint import pprint

# API specific imports
from scaleiopy.api.scaleio.mapping.sio_generic_object import SIO_Generic_Object
from scaleiopy.api.scaleio.system import SIO_System
from scaleiopy.api.scaleio.mapping.sdc import SIO_SDC
from scaleiopy.api.scaleio.mapping.sds import SIO_SDS
from scaleiopy.api.scaleio.mapping.volume import SIO_Volume
from scaleiopy.api.scaleio.mapping.storage_pool import SIO_Storage_Pool
from scaleiopy.api.scaleio.mapping.protection_domain import SIO_Protection_Domain
from scaleiopy.api.scaleio.mapping.faultset import SIO_Fault_Set
from scaleiopy.api.scaleio.mapping.ip_list import SIO_IP_List
from scaleiopy.api.scaleio.mapping.link import SIO_Link
from scaleiopy.api.scaleio.mapping.snapshotspecification import SIO_SnapshotSpecification
from scaleiopy.api.scaleio.mapping.vtree import SIO_Vtree
from scaleiopy.api.scaleio.mapping.statistics import SIO_Statistics

from scaleiopy.api.scaleio.metering.statistics import Statistics
from scaleiopy.api.scaleio.common.connection import Connection
from scaleiopy.api.scaleio.provisioning.volume import Volume
from scaleiopy.api.scaleio.cluster.cluster import Cluster
from scaleiopy.api.scaleio.cluster.storagepool import StoragePool
from scaleiopy.api.scaleio.cluster.protectiondomain import ProtectionDomain
from scaleiopy.api.scaleio.cluster.faultset import FaultSet


# How to remove this one. Let Requests inherit from this class???
class TLS1Adapter(HTTPAdapter):
    """
    A custom HTTP adapter we mount to the session to force the use of TLSv1, which is the only thing supported by
    the gateway.  Python 2.x tries to establish SSLv2/3 first which failed.
    """
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)          
                                       

class ScaleIO(SIO_Generic_Object):
    """
    The ScaleIO class provides a pythonic way to interact with a ScaleIO cluster
    Depends: Working ScaleIO cluster and configured API gateway
    
    Provides:
    * API Login
    * Create/Delete Volume
    * Map/Unmap Volume to host
    * GET storagepools, systemobject, protectiondomains, sdc, sdc, volumes

    """
    def __init__(self, api_url, username, password, verify_ssl=False, debugLevel=None):
        """
        Initializes the class

        :param api_url: Base URL for the API.  Often the MDM host.
        :type api_url: str
        :param username: Username to login with
        :type username: str
        :param password: Password
        :type password: str
        :return: A ScaleIO object
        :rtype: ScaleIO Object
        """

        logging.basicConfig(format='%(asctime)s: %(levelname)s %(module)s:%(funcName)s | %(message)s',
            level=self._get_log_level(debugLevel))
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Logger initialized!")


        # Feature group init
        
        # API -> Connection
        self.connection = Connection(self, api_url, username, password, verify_ssl=False, debugLevel=None)
        self.connection._check_login() # Login. Otherwise login is called upon first API operation
        # API -> Statistics
        self.statistics = Statistics(self)
        self.provisioning = Volume(self)
        # API -> cluster level
        self.cluster = Cluster(self)
        self.cluster_sp = StoragePool(self)
        self.cluster_pd = ProtectionDomain(self)
        self.cluster_sds = Sds(self)
        self.cluster_sdc = Sdc(self)
        
        self.faultset = FaultSet(self)
        

    @staticmethod
    def _get_log_level(level):
        """
        small static method to get logging level
        :param str level: string of the level e.g. "INFO"
        :returns logging.<LEVEL>: appropriate debug level
        """
        # default to DEBUG
        if level is None or level == "DEBUG":
            return logging.DEBUG

        level = level.upper()
        # Make debugging configurable
        if level == "INFO":
            return logging.INFO
        elif level == "WARNING":
            return logging.WARNING
        elif level == "CRITICAL":
            return logging.CRITICAL
        elif level == "ERROR":
            return logging.ERROR
        elif level == "FATAL":
            return logging.FATAL
        else:
            raise Exception("UnknownLogLevelException: enter a valid log level")

    # Common properties that interact with API
    @property
    def system(self):
        """
        Returns a `list` of all the `System` objects to the cluster.  Updates every time - no caching.
        :return: a `list` of all the `System` objects known to the cluster.
        :rtype: list
        """
        self.connection._check_login()
        response = self.connection._do_get("{}/{}".format(self.connection._api_url, "types/System/instances")).json()
        all_system_objects = []
        for system_object in response:
            all_system_objects.append(SIO_System.from_dict(system_object))
        return all_system_objects

    @property
    def storage_pools(self):
        """
        Returns a `list` of all the `System` objects to the cluster.  Updates every time - no caching.
        :return: a `list` of all the `System` objects known to the cluster.
        :rtype: list
        """
        self.connection._check_login()
        response = self.connection._do_get("{}/{}".format(self.connection._api_url, "types/StoragePool/instances")).json() 
        all_storage_pools = []
        for storage_pool_object in response:
            all_storage_pools.append(SIO_Storage_Pool.from_dict(storage_pool_object))
        return all_storage_pools
    
    @property
    def sdc(self):
        """
        Returns a `list` of all the `ScaleIO_SDC` known to the cluster.  Updates every time - no caching.
        :return: a `list` of all the `ScaleIO_SDC` known to the cluster.
        :rtype: list
        """
        self.connection._check_login()
        response = self.connection._do_get("{}/{}".format(self.connection._api_url, "types/Sdc/instances")).json()       
        all_sdc = []
        for sdc in response:
            all_sdc.append(
                SIO_SDC.from_dict(sdc)
            )
        return all_sdc

    @property
    def sds(self):
        """
        Returns a `list` of all the `ScaleIO_SDS` known to the cluster.  Updates every time - no caching.
        :return: a `list` of all the `ScaleIO_SDS` known to the cluster.
        :rtype: list
        """
        self.connection._check_login()
        response = self.connection._do_get("{}/{}".format(self.connection._api_url,"types/Sds/instances")).json()
        all_sds = []
        for sds in response:
            all_sds.append(
                SIO_SDS.from_dict(sds)
            )
        return all_sds

    @property
    def volumes(self):
        """
        Returns a `list` of all the `Volume` known to the cluster.  Updates every time - no caching.
        :return: a `list` of all the `Volume` known to the cluster.
        :rtype: list
        """
        self.connection._check_login()
        response = self.connection._do_get("{}/{}".format(self.connection._api_url, "types/Volume/instances")).json()
        all_volumes = []
        for volume in response:
            all_volumes.append(
                SIO_Volume.from_dict(volume)
            )
        return all_volumes

    @property
    def snapshots(self):
        """
        Get all Volumes of type Snapshot.  Updates every time - no caching.
        :return: a `list` of all the `ScaleIO_Volume` that have a are of type Snapshot.
        :rtype: list
        """
        self.connection._check_login()
        response = self.connection._do_get("{}/{}".format(self.connection._api_url, "types/Volume/instances")).json()
        all_volumes_snapshot = []
        for volume in response:
            if volume['volumeType'] == 'Snapshot':
                all_volumes_snapshot.append(
                    Volume.from_dict(volume)
            )
        return all_volumes_snapshot

    @property
    def protection_domains(self):
        """
        :rtype: list of Protection Domains
        """
        self.connection._check_login()
        response = self.connection._do_get("{}/{}".format(self.connection._api_url, "types/ProtectionDomain/instances")).json()
        all_pds = []
        for pd in response:
            all_pds.append(
                SIO_Protection_Domain.from_dict(pd)
            )
        return all_pds

    @property
    def fault_sets(self):
        """
        You can only create and configure Fault Sets before adding SDSs to the system, and configuring them incorrectly
        may prevent the creation of volumes. An SDS can only be added to a Fault Set during the creation of the SDS.
        :rtype: list of Faultset objects
        """
        self.connection._check_login()
        response = self.connection._do_get("{}/{}".format(self.connection._api_url, "types/FaultSet/instances")).json()
        all_faultsets = []
        for fs in response:
            all_faultsets.append(
                SIO_Fault_Set.from_dict(fs)
            )
        return all_faultsets

    @property
    def vtrees(self):
        """
        Get list of VTrees from ScaleIO cluster
        :return: List of VTree objects - Can be empty of no VTrees exist
        :rtype: VTree object
        """
        self.connection._check_login()
        response = self.connection._do_get("{}/{}".format(self.connection._api_url, "types/VTree/instances")).json()
        all_vtrees = []
        for vtree in response:
            all_vtrees.append(
                SIO_Vtree.from_dict(vtree)
            )
        return all_vtrees


    def get_system_objects(self):
        return self.system
    
    def get_system_id(self):
        return self.system[0].id


    def is_ip_addr(self, ipstr):
        """
        Convenience method to verify if string is an IP addr?
        :param ipstr: Stinrg containing IP address
        :rtype True if string is a valid IP address
        """
        ipstr_chunks = ipstr.split('.')
        if len(ipstr_chunks) != 4:
            return False
        for ipstr_chunk in ipstr_chunks:
            if not ipstr_chunk.isdigit():
                return False
            ipno_part = int(ipstr_chunk)
            if ipno_part < 0 or ipno_part > 255:
                return False
        return True
    '''
    ***************************
    *** DEPRECEATED METHODS ***
    ***************************
    '''
    
    # Connectoin related methods
    def login(self):
        return self.connection.login()
    
    def _check_login(self):
        return self.connection._check_login()
    
    def get_api_version(self):
        return self.connection.get_api_version()
    
    def _do_get(self, url, **kwargs):
        return self.connection._do_get(url, kwargs)
    
    def _do_post(self, url, **kwargs):
        return self.connection._do_post(url, kwargs)
    

    # Volume related methods
    def create_volume(self, volName, volSizeInMb, pdObj, spObj, thinProvision=True, **kwargs):
        return self.provisioning.create_volume(volName, volSizeInMb, pdObj, spObj, thinProvision, kwargs)
    
    def delete_volume(self, volObj, removeMode='ONLY_ME', **kwargs):
        return self.provisioning.delete_volume(volObj, removeMode, kwargs)

    def map_volume_to_sdc(self, volumeObj, sdcObj=None, allowMultipleMappings=False, **kwargs):
        return self.provisioning.map_volume_to_sdc(volumeObj, sdcObj, allowMultipleMappings, kwargs)

    def unmap_volume_from_sdc(self, volObj, sdcObj=None, **kwargs):
        return self.provisioning.unmap_volume_from_sdc(volObj, sdcObj, kwargs)
    
    def get_volumes_for_sdc(self, sdcObj):
        return self.provisioning.get_volumes_for_sdc(sdcObj)

    def get_volume_by_id(self, id):
        return self.provisioning.get_volume_by_id(id)
    
    def get_volumes_for_vtree(self, vtreeObj):
        return self.provisioning.get_volumes_for_vtree(vtreeObj)
    
    def get_volume_by_name(self, name):
        return self.provisioning.get_volume_by_name(name)
    
    def resize_volume(self, volumeObj, sizeInGb, bsize=1000):
        return self.provisioning.resize_volume(volumeObj, sizeInGb, bsize)
    
    def create_snapshot(self, systemId, snapshotSpecificationObject):
        return self.provisioning.create_snapshot(systemId, snapshotSpecificationObject)
    
    def delete_snapshot(self, systemId, snapshotGroupId):
        return self.provisioning.delete_snapshot(systemId, snapshotGroupId)
    
    def get_snapshots_by_vol(self, volObj):
        return self.provisioning.get_snapshots_by_vol(volObj)
    
    def get_vtree_by_id(self,id):
        return self.provisioning.get_vtree_by_id(id)
    
    def get_sdc_for_volume(self, volObj):
        return self.provisioning.get_sdc_for_volume(volObj)
    
    # StoragePool related methods
    def get_storage_pool_by_name(self, name):
        return self.cluster_sp.get_storage_pool_by_name(name)
    
    def get_storage_pool_by_id(self, id):
        return self.cluster_sp.get_storage_pool_by_id(id)
    
    # ProtectionDomain related methods
    def get_pd_by_name(self, name):
        return self.cluster_pd.get_pd_by_name(name)
    
    def get_pd_by_id(self, id):
        return self.cluster_pd.get_pd_by_id(id)
    
    def create_protection_domain(self, pdObj, **kwargs):
        return self.cluster_pd.create_protection_domain(pdObj, kwargs)
    
    def delete_potection_domain(self, pdObj):
        return self.cluster_pd.delete_potection_domain(pdObj)
    
    # FaultSet related methods
    def get_faultset_by_id(self, id):
        return self.faultset.get_faultset_by_id(id)
    
    def get_faultset_by_name(self,name):
        return self.faultset.get_faultset_by_name(name)
    
    def set_faultset_name(self, name, fsObj):
        return self.faultsetdef.set_faultset_name(name, fsObj)
    
    # SDS related methods
    def set_sds_name(self, name, sdsObj):
        return self.cluster_sds.set_sds_name(name, sdsObj)
    
    def unregisterSds(self, sdsObj):
        return self.cluster_sds.unregisterSds(sdsObj)
    
    def registerSds(self, sdsObj, **kwargs):
        return self.cluster_sds.registerSds(sdsObj, kwargs)
    
    def get_sds_in_faultset(self, faultSetObj):
        return self.cluster_sds.get_sds_in_faultset(faultSetObj)
    
    def get_sds_by_name(self,name):
        return self.cluster_sds.get_sds_by_name(name)
    
    def get_sds_by_ip(self,ip):
        return self.cluster_sds.get_sds_by_ip(ip)
    
    def get_sds_by_id(self,id):
        return self.cluster_sds.get_sds_by_id(id)
    
    # SDC related methods
    def set_sdc_name(self, name, sdcObj):
        return self.cluster_sdc.set_sdc_name(name, sdcObj)
    
    def get_sdc_by_name(self, name):
        return self.cluster_sdc.get_sdc_by_name(name)
    
    def get_sdc_by_id(self, id):
        return self.cluster_sdc.get_sdc_by_id(id)
    
    def get_sdc_by_guid(self, guid):
        return self.cluster_sdc.get_sdc_by_guid(guid)
    
    def get_sdc_by_ip(self, ip):
        return self.cluster_sdc.get_sdc_by_ip(ip)
    
    def unregisterSdc(self, sdcObj):
        return self.cluster_sdc.unregisterSdc(sdcObj)
    
    def registerSdc(self, sdcObj, **kwargs):
        return self.cluster_sdc.registerSdc(sdcObj, kwargs)
    

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "Usage: scaleio.py mdm_ip user pass"
    else:
        sio = ScaleIO("https://" + sys.argv[1] + "/api",sys.argv[2],sys.argv[3],False,"DEBUG") # HTTPS must be used as there seem to be an issue with 302 responses in Requests when using POST
        pprint(sio.system)
        pprint(sio.sdc)
        pprint(sio.sds)
        pprint(sio.volumes)
        pprint(sio.protection_domains)
        pprint(sio.storage_pools)
