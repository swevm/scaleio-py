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

    def get_sds_in_faultset(self, faultSetObj):
        """
        Get list of SDS objects attached to a specific ScaleIO Faultset
        :param faultSetObj: ScaleIO Faultset object
        :rtype: list of SDS in specified Faultset
        """
        self._check_login()
        response = self._do_get("{}/{}{}/{}".format(self._api_url, 'types/FaultSet::', faultSetObj.id, 'relationships/Sds')).json()
        all_sds = []
        for fss in response:
            all_sds.append(
                SDS.from_dict(pd)
            )
        return all_sds        
        
    def get_sds_by_name(self,name):
        """
        Get ScaleIO SDS object by its name
        :param name: Name of SDS
        :return: ScaleIO SDS object
        :raise KeyError: No SDS with specified name found
        :rtype: SDS object
        """
        for sds in self.sds:
            if sds.name == name:
                return sds
        raise KeyError("SDS of that name not found")
    '''
    def get_storage_pool_by_name(self, name):
        """
        Get ScaleIO StoragePool object by its name
        :param name: Name of StoragePool
        :return: ScaleIO StoragePool object
        :raise KeyError: No StoragePool with specified name found
        :rtype: StoragePool object
        """
        for storage_pool in self.storage_pools:
            if storage_pool.name == name:
                return storage_pool
        raise KeyError("Storage pool of that name not found")

    def get_storage_pool_by_id(self, id):
        """
        Get ScaleIO SDS ofbject by its id
        :param name: Name of StoragePool
        :return: ScaleIO StoraegPool object
        :raise KeyError: No StoragePool with specified id found
        :rtype: StoragePool object
        """
        for storage_pool in self.storage_pools:
            if storage_pool.id == id:
                return storage_pool
        raise KeyError("Storage Pool with that ID not found")
    '''
    
    def get_sds_by_ip(self,ip):
        """
        Get ScaleIO SDS object by its ip address
        :param name: IP address of SDS
        :return: ScaleIO SDS object
        :raise KeyError: No SDS with specified ip found
        :rtype: SDS object
        """
        if self.is_ip_addr(ip):
            for sds in self.sds:
                for sdsIp in sds.ipList:
                    if sdsIp == ip:
                        return sds
            raise KeyError("SDS of that name not found")
        else:
            raise ValueError("Malformed IP address - get_sds_by_ip()")
        
    def get_sds_by_id(self,id):
        """
        Get ScaleIO SDS object by its id
        :param name: ID of SDS
        :return: ScaleIO SDS object
        :raise KeyError: No SDS with specified id found
        :rtype: SDS object
        """
        for sds in self.sds:
            if sds.id == id:
                return sds
        raise KeyError("SDS with that ID not found")

    def get_sdc_by_name(self, name):
        """
        Get ScaleIO SDC object by its name
        :param name: Name of SDC
        :return: ScaleIO SDC object
        :raise KeyError: No SDC with specified name found
        :rtype: SDC object
        """
        for sdc in self.sdc:
            if sdc.name == name:
                return sdc
        raise KeyError("SDC of that name not found")

    def get_sdc_by_id(self, id):
        """
        Get ScaleIO SDC object by its id
        :param name: id of SDC
        :return: ScaleIO SDC object
        :raise KeyError: No SDC with specified id found
        :rtype: SDC object
        """
        for sdc in self.sdc:
            if sdc.id == id:
                return sdc
        raise KeyError("SDC with that ID not found")

    def get_sdc_by_guid(self, guid):
        """
        Get ScaleIO SDC object by its id
        :param name: guid of SDC
        :return: ScaleIO SDC object
        :raise KeyError: No SDC with specified id found
        :rtype: SDC object
        """
        for sdc in self.sdc:
            if sdc.guid == guid:
                return sdc
        raise KeyError("SDC with that GUID not found")

    def get_sdc_by_ip(self, ip):
        """
        Get ScaleIO SDC object by its ip
        :param name: IP address of SDC
        :return: ScaleIO SDC object
        :raise KeyError: No SDC with specified IP found
        :rtype: SDC object
        """
        if self.is_ip_addr(ip):
            for sdc in self.sdc:
                if sdc.sdcIp == ip:
                    return sdc
            raise KeyError("SDS of that name not found")
        else:
            raise ValueError("Malformed IP address - get_sdc_by_ip()")
    
    def get_sdc_for_volume(self, volObj):
        """
        Get list of SDC mapped to a specific volume
        :param volObj: ScaleIO volume object
        :return: List of ScaleIO SDC objects (empty list if no mapping exist)
        :rtype: SDC object
        """
        sdcList = []
        if volObj.mapped_sdcs is not None:
            for sdc in volObj.mapped_sdcs:
                sdcList.append(sdc)
        if len(sdcList) == 0:
            self.logger.debug("No SDCs mapped to volume: %s-(%s)" % (volObj.name, volObj.id))
            return []
        # returning an empty list is
        # valid for snapshots or volumes.
        return sdcList
    '''    
    def get_volumes_for_sdc(self, sdcObj):
        """
        :param sdcObj: SDC object
        :return: list of Volumes attached to SDC
        :rtyoe: ScaleIO Volume object
        """
        self._check_login()
        all_volumes = []
        response = self._do_get("{}/{}{}/{}".format(self._api_url, 'instances/Sdc::', sdcObj.id, 'relationships/Volume')).json()
        for sdc_volume in response:
            all_volumes.append(
                Volume.from_dict(sdc_volume)
            )
        return all_volumes        
    '''

    '''
    def get_pd_by_name(self, name):
        """
        Get ScaleIO ProtectionDomain object by its name
        :param name: Name of ProtectionDomain
        :return: ScaleIO ProtectionDomain object
        :raise KeyError: No ProtetionDomain with specified name found
        :rtype: ProtectionDomain object
        """
        for pd in self.protection_domains:
            if pd.name == name:
                return pd
        raise KeyError("Protection Domain NAME " + name + " not found")

    def get_pd_by_id(self, id):
        """
        Get ScaleIO ProtectionDomain object by its id
        :param name: ID of ProtectionDomain
        :return: ScaleIO ProctectionDomain object
        :raise KeyError: No ProtectionDomain with specified name found
        :rtype: ProtectionDomain object
        """
        for pd in self.protection_domains:
            if pd.id == id:
                return pd
        raise KeyError("Protection Domain with ID " + id + " not found")
    '''

    '''
    def get_volume_by_id(self, id):
        """
        Get ScaleIO Volume object by its ID
        :param name: ID of volume
        :return: ScaleIO Volume object
        :raise KeyError: No Volume with specified ID found
        :rtype: ScaleIO Volume object
        """
        for vol in self.volumes:
            if vol.id == id:
                return vol
        raise KeyError("Volume with ID " + id + " not found")
    '''
    
    '''
    def get_volumes_for_vtree(self, vtreeObj):
        """
        :param vtreeObj: VTree object
            Protection Domain Object
        :return: list of Volumes attached to VTree
        :rtype: ScaleIO Volume object
        """
        self._check_login()
        all_volumes = []
        response = self._do_get("{}/{}{}/{}".format(self._api_url, 'instances/VTree::', vtreeObj.id, 'relationships/Volume')).json()
        for vtree_volume in response:
            all_volumes.append(
                Volume.from_dict(vtree_volume)
            )
        return all_volumes
    '''
    
    '''
    def get_volume_by_name(self, name):
        """
        Get ScaleIO Volume object by its Name
        :param name: Name of volume
        :return: ScaleIO Volume object
        :raise KeyError: No Volume with specified name found
        :rtype: ScaleIO Volume object
        """
        for vol in self.volumes:
            if vol.name == name:
                return vol
        raise KeyError("Volume with NAME " + name + " not found")
    
    def get_volume_all_sdcs_mapped(self, volObj):
        if volObj.mappingToAllSdcsEnabled == True:
            return True
        return False
    '''
    
    def get_faultset_by_id(self, id):
        for fs in self.fault_sets:
            if fs.id == id:
                return fs
        raise KeyError("FaultSet with ID " + id + " not found")

    def get_faultset_by_name(self,name):
        for fs in self.fault_sets:
            if fs.name == name:
                return fs
        raise KeyError("FaultSet with NAME " + name + " not found")

    def get_vtree_by_id(self,id):
        for vtree in self.vtrees:
            if vtree.id == id:
                return vtree
        raise KeyError("VTree with ID " + id + " not found")

    def get_vtree_by_name(self,name):
        for vtree in self.vtrees:
            if vtree.name == name:
                return vtree
        raise KeyError("VTree with NAME " + name + " not found")
    
    def get_snapshots_by_vol(self, volObj):
        all_snapshots_for_vol = []
        for volume in self.get_volumes_for_vtree(self.get_vtree_by_id(volObj.vtree_id)):
            if volume.ancestor_volume is not None:
                 all_snapshots_for_vol.append(volume)
        return all_snapshots_for_vol
    
    """
    def get_snapshot_group_id_by_vol_name(self, volname):
        pass
    
    def get_snapshot_group_id_by_vol_id(self, volid):
        pass
    """
    
    def create_protection_domain(self, pdObj, **kwargs):
        # TODO:
        # Check if object parameters are the correct ones
        self._check_login()    
        response = self._do_post("{}/{}".format(self._api_url, "types/Volume/instances"), json=pdObj.__to_dict__()())
        return response
    
    def delete_potection_domain(self, pdObj):
        """
        :param pdObj: ID of ProtectionDomain
        
        type: POST
        Required:
            Protection Domain Object
        Return:
        """
        self._check_login()
        response = self._do_post("{}/{}{}/{}".format(self._api_url, "instances/ProtectionDomain::", pdObj.id, 'action/removeProtectionDomain'))
        return response
    
    def create_snapshot(self, systemId, snapshotSpecificationObject):
        """
        Create snapshot for list of volumes
        :param systemID: Cluster ID 
        :param snapshotSpecificationObject: Of class SnapshotSpecification
        :rtype: SnapshotGroupId
        """
        self._check_login()
        #try:
        response = self._do_post("{}/{}{}/{}".format(self._api_url, "instances/System::", systemId, 'action/snapshotVolumes'), json=snapshotSpecificationObject.__to_dict__())
        #except:
        #    raise RuntimeError("create_snapshot_by_system_id() - Error communicating with ScaleIO gateway")
        return response
        
    def delete_snapshot(self, systemId, snapshotGroupId):
        """
        :param systemId: ID of Cluster
        :param snapshotGroupId: ID of snapshot group ID to be removed
        
        
        /api/instances/System::{id}/action/removeConsistencyGroupSnapshots
        type: POST
        Required:
            snapGroupId
        Return:
            numberOfVolumes - number of volumes that were removed because of this operation
        
        """
        #try:
        consistencyGroupIdDict = {'snapGroupId':snapshotGroupId}
        self._check_login()
        response = self._do_post("{}/{}{}/{}".format(self._api_url, "instances/System::", systemId, 'action/removeConsistencyGroupSnapshots'), json=consistencyGroupIdDict)
        #except:
        #    raise RuntimeError("delete_snapshot() - Error communicating wit ScaleIO gateway")
        return response

    #def create_volume(self, volName, volSizeInMb, pdObj, thinProvision=True, **kwargs): # Worked in v1.31 but not in v1.32
    '''
    def create_volume(self, volName, volSizeInMb, pdObj, spObj, thinProvision=True, **kwargs): #v1.32 require storagePoolId when creating a volume
        # Check if object parameters are the correct ones, otherwise throw error
        self._check_login()    
        if thinProvision:
            volType = 'ThinProvisioned'
        else:
            volType = 'ThickProvisioned'
        # ScaleIO v1.31 demand protectionDomainId in JSON but not storgePoolId. v1.32 is fine with storeagePoolId only
        volumeDict = {'protectionDomainId': pdObj.id, 'storagePoolId': spObj.id, 'volumeSizeInKb': str(int(volSizeInMb) * 1024),  'name': volName, 'volumeType': volType}
        response = self._do_post("{}/{}".format(self._api_url, "types/Volume/instances"), json=volumeDict)

        if kwargs:
            for key, value in kwargs.iteritems():
                if key == 'enableMapAllSdcs' and value == True:
                    self.map_volume_to_sdc(self.get_volume_by_name(volName), enableMapAllSdcs=True)
                if key == 'mapToSdc':
                    if value:
                        for innerKey, innerValue in kwargs.iteritems():
                            if innerKey == 'enableMapAllSdcs':
                                    if innerValue == True:
                                        self.map_volume_to_sdc(self.get_volume_by_name(volName), enableMapAllSdcs=True)
                                    else:
                                        self.map_volume_to_sdc(self.get_volume_by_name(volName), self.get_sdc_by_name(value))
        return response
    '''

    def resize_volume(self, volumeObj, sizeInGb, bsize=1000):
        """
        Resize a volume to new GB size, must be larger than original.
        :param volumeObj: ScaleIO Volume Object
        :param sizeInGb: New size in GB (have to be larger than original)
        :param bsize: 1000
        :return: POST request response
        :rtype: Requests POST response object
        """
        current_vol = self.get_volume_by_id(volumeObj.id)
        if current_vol.size_kb > (sizeInGb * bsize * bsize):
            raise RuntimeError(
                "resize_volume() - New size needs to be bigger than: %d KBs" % current_vol.size_kb)
        
        resizeDict = { 'sizeInGB' : str(sizeInGb) }
        response = self._do_post("{}/{}{}/{}".format(
            self._api_url, "instances/Volume::", volumeObj.id, 'action/setVolumeSize'), json=resizeDict)
        return response

    def map_volume_to_sdc(self, volumeObj, sdcObj=None, allowMultipleMappings=False, **kwargs):
        """
        Map a Volume to SDC
        :param volumeObj: ScaleIO Volume object
        :param sdcObj: ScaleIO SDC object
        :param allowMultipleMappings: True to allow more than one SDC to be mapped to volume
        :return: POST request response
        :rtype: Requests POST response object
        """
        self._check_login()
        if kwargs:
            for key, value in kwargs.iteritems():
                if key == 'enableMapAllSdcs':
                    if value == True:
                        mapVolumeToSdcDict = {'allSdcs': 'True'}
        else:
            mapVolumeToSdcDict = {'sdcId': sdcObj.id, 'allowMultipleMappings': str(allowMultipleMappings).upper()}
        response = self._do_post("{}/{}{}/{}".format(self._api_url, "instances/Volume::", volumeObj.id, 'action/addMappedSdc'), json=mapVolumeToSdcDict)
        return response
    
    def unmap_volume_from_sdc(self, volObj, sdcObj=None, **kwargs):
        """
        Unmap a Volume from SDC or all SDCs
        :param volObj: ScaleIO Volume object
        :param sdcObj: ScaleIO SDC object
        :param \**kwargs:
        :Keyword Arguments:
        *disableMapAllSdcs* (``bool``) -- True to disable all SDCs mapping
        :return: POST request response
        :rtype: Requests POST response object
        :raise RuntimeError: If failure happen during communication with REST Gateway - Need to be cleaned up and made consistent to return understandable errors
        """
        # TODO:
        # Check if object parameters are the correct ones, otherwise throw error
        # ADD logic for ALL SDC UNMAP
        # For all SDC unmapVolumeFromDict = {'allSdc':'True'} False can be used
        self._check_login()
        if kwargs:
            for key, value in kwargs.iteritems():
                if key == 'enableMapAllSdcs' and value == False:
                    if self.get_volume_all_sdcs_mapped(volObj): # Check if allSdc?s is True before continuing
                        unmapVolumeFromSdcDict = {'allSdcs': 'False'}
        else:
                unmapVolumeFromSdcDict = {'sdcId': sdcObj.id}
        try:
            response = self._do_post("{}/{}{}/{}".format(self._api_url, "instances/Volume::", volObj.id, 'action/removeMappedSdc'), json=unmapVolumeFromSdcDict)
        except:
            raise RuntimeError("unmap_volume_from_sdc() - Cannot unmap volume")
        return response

    def delete_volume(self, volObj, removeMode='ONLY_ME', **kwargs):
        """
        removeMode = 'ONLY_ME' | 'INCLUDING_DESCENDANTS' | 'DESCENDANTS_ONLY' | 'WHOLE_VTREE'
        Using kwargs it will be possible to tell delete_volume() to unmap all SDCs before delting. Not working yet
        """
        if kwargs:
            for key, value in kwargs.iteritems():
                if key =='autoUnmap' and value ==True:
                    # Find all mapped SDS to this volObj
                    # Call unmap for all of them
                    if self.get_volume_all_sdcs_mapped(volObj):
                        try:
                            self.unmap_volume_from_sdc(volObj, enableMapAllSdcs=False)
                        except:
                            raise RuntimeError("delete_volume() - enableMapAllSdcs error")
                    else: # All SDS not enabled so loop through all mapped SDCs of volume and remove one by one                        
                        for sdc in self.get_sdc_for_volume(volObj):
                            try:
                                self.unmap_volume_from_sdc(volObj, self.get_sdc_by_id(sdc['sdcId']))
                            except:
                                raise RuntimeError("delete_volume() - unmap_volume_from_sdc() error")
        # TODO:
        # Check if object parameters are the correct ones, otherwise throw error
        self._check_login()
        deleteVolumeDict = {'removeMode': removeMode}
        try:
            response = self._do_post("{}/{}{}/{}".format(self._api_url, "instances/Volume::", volObj.id, 'action/removeVolume'), json=deleteVolumeDict)
        except:
            raise RuntimeError("delete_volume() - Communication error with ScaleIO Gateway")
        return response
    
    def set_sds_name(self, name, sdsObj):
        """
        Set name for SDS
        :param name: Name of SDS
        :param sdsObj: ScaleIO SDS object
        :return: POST request response
        :rtype: Requests POST response object
        """
        # TODO:
        # Check if object parameters are the correct type, otherwise throw error
        # UNSURE IF THIS IS CORRECT WAY TO SET SDS NAME
        self._check_login()
        sdsNameDict = {'sdsName': name}
        response = self._do_post("{}/{}{}/{}".format(self._api_url, "instances/Sds::", sdcObj.id, 'action/setSdsName'), json=sdsNameDict)    
        return response

    def set_sdc_name(self, name, sdcObj):
        """
        Set name for SDC
        :param name: Name of SDC
        :param sdcObj: ScaleIO SDC object
        :return: POST request response
        :rtype: Requests POST response object
        """
        # TODO:
        # Check if object parameters are the correct ones, otherwise throw error
        self._check_login()
        sdcNameDict = {'sdcName': name}
        response = self._do_post("{}/{}{}/{}".format(self._api_url, "instances/Sdc::", sdcObj.id, 'action/setSdcName'), json=sdcNameDict)    
        return response

    def set_faultset_name(self, name, fsObj):
        """
        Set name for Faultset
        :param name: Name of Faultset
        :param fsObj: ScaleIO FS object
        :return: POST request response
        :rtype: Requests POST response object
        """
        # Set name of FaultSet
        self._check_login()
        faultSetNameDict = {'Name': name}
        # This one is the most logical name comparing to other methods.
        response = self._do_post("{}/{}{}/{}".format(self._api_url, "types/FaultSet::", fsObj.id, 'instances/action/setFaultSetName'), json=faultSetNameSdcDict)    

        # This is how its documened in REST API Chapter
        #response = self._do_post("{}/{}{}/{}".format(self._api_url, "types/FaultSet::", fsObj.id, 'instances/action/setFaultSetName'), json=faultsetNameSdcDict)    
        return response    
    
    def unregisterSdc(self, sdcObj):
        """
        Unregister SDC from MDM/SIO Cluster
        :param sdcObj: ScaleIO SDC object
        :return: POST request response
        :rtype: Requests POST response object
        """
        # TODO:
        # Add code that unmap volume if mapped
        self._check_login()
        response = self._do_post("{}/{}{}/{}".format(self._api_url, "instances/Sdc::", sdcObj.id, 'action/removeSdc'))    
        return response

    def registerSdc(self, sdcObj, **kwargs):
        # Register existing SDS running SDS binary (need to be installed manually but not added to MDM)
        # 
        self._check_login()    

        response = self._do_post("{}/{}".format(self._api_url, "types/Sdc/instances"), json=sdcObj.__to_dict__())
        return response

    def unregisterSds(self, sdsObj):
        """
        Unregister SDS from MDM/SIO Cluster
        :param sdsObj: ScaleIO SDS objecty
        :return: POST request response
        :rtype: Requests POST response object
        """
        self._check_login()
        response = self._do_post("{}/{}{}/{}".format(self._api_url, "instances/Sds::", sdsObj.id, 'action/removeSds'))    
        return response    
    
    # /api/types/Sds/instance s
    def registerSds(self, sdsObj, **kwargs):
        """
        Register SDS with MDM/SIO Cluster
        :param sdsObj: ScaleIO SDS object
        :return: POST request response
        :rtype: Requests POST response object
        """
        # Register existing SDS running SDS binary (need to be installed manually but not added to MDM)
        # 
        self._check_login()    

        response = self._do_post("{}/{}".format(self._api_url, "types/Sds/instances"), json=sdsObj.__to_dict__())
        return response
    
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
    
    def is_valid_volsize(self,volsize):
        """
        Convenience method that round input to valid ScaleIO Volume size (8GB increments)
        :param volsize: Size in MB
        :rtype int: Valid ScaleIO Volume size rounded to nearest 8GB increment above or equal to volsize
        """
        
        if type(volsize) is int:
            size_temp = divmod(volsize, 8192)
            if size_temp[1] > 0: # If not on 8GB boundary
                return int((1 + size_temp[0]) * 8192) # Always round to next 8GB increment
        else:
            return int(volsize)

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
