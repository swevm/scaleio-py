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

class SIO_Generic_Object(object):
    @classmethod
    def get_class_name(cls):
        """
        A helper method that returns the name of the class.  Used by __str__ below
        """
        return cls.__name__

    def __str__(self):
        """
        A convinience method to pretty print the contents of the class instance
        """
        # to show include all variables in sorted order
        return "<{}> @ {}:\n".format(self.get_class_name(), id(self)) + "\n".join(
            ["  %s: %s" % (key.rjust(22), self.__dict__[key]) for key in sorted(set(self.__dict__))])

    def __repr__(self):
        return self.__str__()

class ScaleIO_System(SIO_Generic_Object):
    def __init__(self,
        id=None,
        name=None,
        systemVersionName=None,
        primaryMdmActorIpList = None, #List
        primaryMdmActorPort = None,
        secondaryMdmActorIpList = None, #List
        secondaryMdmActorPort = None, 
        tiebreakerMdmIpList = None,  #List
        tiebreakerMdmPort = None, # This one is defined in ScaleIO 1.30 API, but seem not present in 1.31??
        tiebreakerMdmActorPort = None,
        mdmMode = None, #Single or Cluster
        mdmClusterState = None, # NotClustered or ClusteredNormal or ClusteredDegraded or ClusteredTiebreakerDown or ClusteredDegradedTiebreakerDown
        mdmManagementIpList = None, # List
        mdmManagementPort = None, 
        capacityAlertHighThresholdPercent = None,
        capacityAlertCriticalThresholdPercent = None,
        installId = None, 
        swid = None, # This one seem not to return anything. Its define din 1.30. What about 1.31????
        daysInstalled = None, 
        maxCapacityInGb = None,
        capacityTimeLeftInDays = None, 
        enterpriseFeaturesEnabled = None, 
        defaultIsVolumeObfuscated = None,
        isInitialLicense = None, 
        restrictedSdcModeEnabled = None,
        remoteReadOnlyLimitState = None,
        links = None
  
    ):
        self.id=None
        self.name=None
        self.system_version_name = systemVersionName
        self.primary_mdm_actor_ip_list = []
        for ip in primaryMdmActorIpList:
            self.primary_mdm_actor_ip_list.append(ip)
        self.primary_mdm_actor_port = primaryMdmActorPort
        self.secondary_mdm_actor_ip_list = secondaryMdmActorIpList
        self.secondary_mdm_actor_port = secondaryMdmActorPort 
        self.tiebreaker_mdm_ip_list = tiebreakerMdmIpList
        self.tiebreaker_mdm_port = tiebreakerMdmPort
        self.tiebreaker_mdm_actor_port = tiebreakerMdmPort
        self.mdm_mode = mdmMode
        self.mdm_cluster_state = mdmClusterState
        self.mdm_management_ip_list = mdmManagementIpList
        self.mdm_management_port = mdmManagementPort 
        self.capacity_alert_high_threshold_percent = capacityAlertHighThresholdPercent
        self.capacity_alert_critical_threshold_percent = capacityAlertCriticalThresholdPercent
        self.install_id = installId
        self.swid = swid 
        self.days_installed = daysInstalled 
        self.max_caapcity_in_gb = maxCapacityInGb
        self.capacity_time_left_in_days = capacityTimeLeftInDays 
        self.enterprise_features_enabled = enterpriseFeaturesEnabled
        self.default_is_volume_obfuscated = defaultIsVolumeObfuscated
        self.is_initial_license = isInitialLicense
        self.restricted_sdc_mode_enabled = restrictedSdcModeEnabled
        self.remote_readonly_limit_state = remoteReadOnlyLimitState
        self.links = []
        for link in links:
            self.links.append(Link(link['href'],link['rel']))        
        

    @staticmethod
    def from_dict(dict):
        """
        A convinience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return ScaleIO_System(**dict)
    
class ScaleIO_Storage_Pool(SIO_Generic_Object): 
    def __init__(self,
        id=None,
        name=None,
        links=None,
        sparePercentage=None,
        rebuildEnabled=None,
        rebalanceEnabled=None,
        rebuildIoPriorityPolicy=None, #unlimited or limitNumOfConcurrentIos or favorAppIos or dynamicBwThrottling
        rebalanceIoPriorityPolicy=None, 
        rebuildIoPriorityNumOfConcurrentIosPerDevice=None, 
        rebalanceIoPriorityNumOfConcurrentIosPerDevice=None, 
        rebuildIoPriorityBwLimitPerDeviceInKbps=None, 
        rebalanceIoPriorityBwLimitPerDeviceInKbps=None,
        rebuildIoPriorityAppIopsPerDeviceThreshold=None, 
        rebalanceIoPriorityAppIopsPerDeviceThreshold=None,
        rebuildIoPriorityAppBwPerDeviceThresholdInKbps=None, 
        rebalanceIoPriorityAppBwPerDeviceThresholdInKbps=None,
        rebuildIoPriorityQuietPeriodInMsec=None,
        rebalanceIoPriorityQuietPeriodInMsec=None,
        numOfParallelRebuildRebalanceJobsPerDevice=None,
        protectionDomainId=None, 
        zeroPaddingEnabled=None,
        useRmcache=None, 
        rmcacheWriteHandlingMode=None #Passthrough or Cached
    ):
        self.id=id
        self.name=name
        self.links = []
        for link in links:
            self.links.append(Link(link['href'], link['rel']))
        self.spare_percentage=sparePercentage
        self.rebuild_enabled=rebuildEnabled
        self.rebalance_enabled=rebalanceEnabled
        self.revuild_io_prioroti_policy=rebuildIoPriorityPolicy #unlimited or limitNumOfConcurrentIos or favorAppIos or dynamicBwThrottling
        self.rebalance_prioritiy_policy=rebalanceIoPriorityPolicy
        self.rebuild_io_prioroity_num_of_concurrent_ios_per_device=rebuildIoPriorityNumOfConcurrentIosPerDevice 
        self.rebalance_io_priority_num_of_concurrent_ios_per_device=rebalanceIoPriorityNumOfConcurrentIosPerDevice 
        self.revuild_io_priority_bw_limits_per_device_in_kbps=rebuildIoPriorityBwLimitPerDeviceInKbps 
        self.rebalance_io_priority_bw_limit_per_device_in_kbps=rebalanceIoPriorityBwLimitPerDeviceInKbps
        self.rebuild_io_priority_app_iops_per_device_threshold=rebuildIoPriorityAppIopsPerDeviceThreshold 
        self.rebalance_io_priority_app_iops_per_devicE_threshold=rebalanceIoPriorityAppIopsPerDeviceThreshold
        self.rebuild_io_priority_app_bw_per_device_threshold_in_kbps=rebuildIoPriorityAppBwPerDeviceThresholdInKbps 
        self.rebalance_priority_apps_bw_per_device_threshold_in_kbps=rebalanceIoPriorityAppBwPerDeviceThresholdInKbps
        self.rebuild_io_priority_quite_period_in_msec=rebuildIoPriorityQuietPeriodInMsec
        self.reabalance_io_priority_quiet_period_in_msec=rebalanceIoPriorityQuietPeriodInMsec
        self.num_of_parallel_rebuild_rebalance_job_per_device=numOfParallelRebuildRebalanceJobsPerDevice
        self.protection_domain_id=protectionDomainId 
        self.zero_padding_enabled=zeroPaddingEnabled
        self.use_rm_cache=useRmcache 
        self.rmcache_write_handling_mode=rmcacheWriteHandlingMode       
    
    @staticmethod
    def from_dict(dict):
        """
        A convinience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return ScaleIO_Storage_Pool(**dict)

class ScaleIO_Protection_Domain(SIO_Generic_Object):
    def __init__(self,
        id=None,
        links=None,
        name=None,
        overallIoNetworkThrottlingEnabled=None,
        overallIoNetworkThrottlingInKbps=None,
        protectionDomainState=None,
        rebalanceNetworkThrottlingEnabled=None,
        rebalanceNetworkThrottlingInKbps=None,
        rebuildNetworkThrottlingEnabled=None,
        rebuildNetworkThrottlingInKbps=None,
        systemId=None
    ):
        self.id=id
        self.links = []
        for link in links:
            self.links.append(Link(link['href'], link['rel']))
        self.name=name
        self.overall_network_throttle_enabled=overallIoNetworkThrottlingEnabled
        self.overall_network_throttle_kbps=overallIoNetworkThrottlingInKbps
        self.protection_domain_state=protectionDomainState
        self.rebalance_network_throttle_enabled=rebalanceNetworkThrottlingEnabled
        self.rebalance_network_throttle_kbps=rebalanceNetworkThrottlingInKbps
        self.rebuild_network_throttle_enabled=rebuildNetworkThrottlingEnabled
        self.rebuild_network_throttle_kbps=rebuildNetworkThrottlingInKbps
        self.system_id=systemId


    @staticmethod
    def from_dict(dict):
        """
        A convinience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return ScaleIO_Protection_Domain(**dict)

class ScaleIO_Volume(SIO_Generic_Object):
    def __init__(self,
                 ancestorVolumeId=None,
                 consistencyGroupId=None,
                 creationTime=None,
                 id=None,
                 isObfuscated=None,
                 links=False,
                 mappedScsiInitiatorInfo=None,
                 mappedSdcInfo=None,
                 mappingToAllSdcsEnabled=None,
                 name=None,
                 sizeInKb=0,
                 storagePoolId=None,
                 useRmcache=False,
                 volumeType=None,
                 vtreeId=None
    ):
        self.id = id
        self.links = []
        for link in links:
            self.links.append(Link(link['href'], link['rel']))
        self.ancestor_volume = ancestorVolumeId
        self.consistency_group_id=consistencyGroupId
        self.creation_time=time.gmtime(creationTime)
        self.id=id
        self.name = name
        self.is_obfuscated = isObfuscated
        self.mapped_scsi_initiators = mappedScsiInitiatorInfo
        self.mapped_sdcs = mappedSdcInfo
        self.size_kb = sizeInKb
        self.storage_pool_id = storagePoolId
        self.use_cache = useRmcache
        self.volume_type = volumeType
        self.vtree_id = vtreeId
        self.mappingToAllSdcsEnabled = mappingToAllSdcsEnabled


    @staticmethod
    def from_dict(dict):
        """
        A convinience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return ScaleIO_Volume(**dict)

class ScaleIO_SDC(SIO_Generic_Object):
    def __init__(self,
                 id=None,
                 links=None,
                 mdmConnectionState=None,
                 name=None,
                 onVmWare=None,
                 sdcApproved=False,
                 sdcGuid=None,
                 sdcIp=None,
                 systemId=None
    ):

        self.id = id
        self.name = name
        self.mdmConnectionState = mdmConnectionState
        self.sdcIp = sdcIp
        self.links = []
        for link in links:
            self.links.append(Link(link['href'], link['rel']))



    @staticmethod
    def from_dict(dict):
        """
        A convinience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return ScaleIO_SDC(**dict)

class ScaleIO_SDS(SIO_Generic_Object):
    def __init__(self,
                 drlMode=None,
                 ipList=None,
                 faultSetId=None,
                 id=None,
                 links=None,
                 mdmConnectionState=None,
                 membershipState=None,
                 name=None,
                 numOfIoBuffers=None,
                 onVmWare=None,
                 port=None,
                 protectionDomainId=None,
                 rmcacheEnabled=None,
                 rmcacheFrozen=None,
                 rmcacheMemoryAllocationState=None,
                 rmcacheSizeInKb=None,
                 sdsState=None
                 ):
        self.drl_mode = drlMode
        self.ip_list = []
        for ip in ipList:
            self.ip_list.append(IP_List(ip['ip'],ip['role']))
        self.fault_set_id = faultSetId
        self.id = id
        self.links = []
        for link in links:
            self.links.append(Link(link['href'],link['rel']))
        self.mdm_connection_state = mdmConnectionState
        self.membership_state = membershipState
        self.name = name
        self.number_io_buffers = int(numOfIoBuffers)
        self.on_vmware = onVmWare
        self.port = port
        self.protection_domain_id = protectionDomainId
        self.rm_cache_enabled = rmcacheEnabled
        self.rm_cache_frozen = rmcacheFrozen
        self.rm_cachem_memory_allocation = rmcacheMemoryAllocationState
        self.rm_cache_size_kb = rmcacheSizeInKb
        self.sds_state=sdsState

    @staticmethod
    def from_dict(dict):
        """
        A convinience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return ScaleIO_SDS(**dict)

class IP_List(object):
    def __init__(self, ip, role):
        self.ip = ip
        self.role = role

    def __str__(self):
        """
        A convinience method to pretty print the contents of the class instance
        """
        # to show include all variables in sorted order
        return "{} : IP: {} Role: {}".format("IP",self.ip,self.role)

    def __repr__(self):
        return self.__str__()

class Link(object):
    def __init__(self, href, rel):
        self.href = href
        self.rel = rel

    def __str__(self):
        """
        A convinience method to pretty print the contents of the class instance
        """
        # to show include all variables in sorted order
        return "{} : Target: '{}' Relative: '{}'".format("Link", self.href, self.rel)

    def __repr__(self):
        return self.__str__()

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
    The ScaleIO class provides a pythonic way to interact with and manage a ScaleIO cluster/
    """
    def __init__(self, api_url, username, password, verify_ssl=False):
        """
        Initializes the class

        :param api_url: Base URL for the API.  Often the MDM host.
        :type api_url: str
        :param username: Username to login with
        :type username: str
        :param password: Password
        :type password: str
        :return: A ScaleIO object
        :rtype: ScaleIO
        """

        self._username = username
        self._password = password
        self._api_url = api_url
        self._session = requests.Session()
        self._session.headers.update({'Accept': 'application/json', 'Version': '1.0'}) # Accept only json
        self._session.mount('https://', TLS1Adapter())
        self._verify_ssl = verify_ssl
        self._logged_in = False
        requests.packages.urllib3.disable_warnings() # Disable unverified connection warning.
    
    def _login(self):
        logging.info("Logging into " + "{}/{}".format(self._api_url, "login"))
        login_response = self._session.get(
            "{}/{}".format(self._api_url,"login"),
            verify=self._verify_ssl,
            auth=HTTPBasicAuth(self._username, self._password)
        ).json()
        self._auth_token = login_response
        self._session.auth = HTTPBasicAuth('',self._auth_token)
        self._logged_in = True

    def _check_login(self):
        if not self._logged_in:
            self._login()
        else:
            pass
        return None
    
    # FIX _do_get method, easier to have one place to do error handling than in all other methods that call _do_get()
    def _do_get(self, uri, **kwargs):
        """
        Convinient method for GET requests
        Returns http request status value from a POST request
        """
        #TODO:
        # Add error handling. Check for HTTP status here would be much more conveinent than in each calling method
        scaleioapi_post_headers = {'Content-type':'application/json','Version':'1.0'}
        try:
            response = self._session.get("{}/{}".format(self._api_url, uri)).json()
            #response = self._session.get(url, headers=scaleioapi_post_headers, **kwargs)
            if response.status_code == requests.codes.ok:
                return response
            else:
                raise RuntimeError("_do_get() - HTTP response error" + response.status_code)
        except:
            raise RuntimeError("_do_get() - Communication error with ScaleIO gateway")
        return response

    def _do_post(self, url, **kwargs):
        """
        Convinient method for POST requests
        Returns http request status value from a POST request
        """
        #TODO:
        # Add error handling. Check for HTTP status here would be much more conveinent than in each calling method
        scaleioapi_post_headers = {'Content-type':'application/json','Version':'1.0'}
        try:
            response = self._session.post(url, headers=scaleioapi_post_headers, **kwargs)
            if response.status_code == requests.codes.ok:
                return response
            else:
                raise RuntimeError("_do_post() - HTTP response error" + response.status_code)
        except:
            raise RuntimeError("_do_post() - Communication error with ScaleIO gateway")
        return response

    @property
    def system(self):
        """
        Returns a `list` of all the `System` objects to the cluster.  Updates every time - no caching.
        :return: a `list` of all the `System` objects known to the cluster.
        :rtype: list
        """
        self._check_login()
        try:
            response = self._session.get(
                "{}/{}".format(self._api_url, "types/System/instances")
                ).json()
        except:
            raise ("system() property - Communication error with ScaleIO gateway")
        #print "*** ScaleIO SYSTEM ***"
        #pprint(response)
        all_system_objects = []
        for system_object in response:
            all_system_objects.append(ScaleIO_System.from_dict(system_object))
        return all_system_objects

    @property
    def storage_pools(self):
        """
        Returns a `list` of all the `System` objects to the cluster.  Updates every time - no caching.
        :return: a `list` of all the `System` objects known to the cluster.
        :rtype: list
        """
        self._check_login()
        try:
            response = self._session.get(
                "{}/{}".format(self._api_url, "types/StoragePool/instances")
                ).json()
        except:
            raise ("system() property - Communication error with ScaleIO gateway")
        #print "*** ScaleIO STORAGE POOL ***"
        #pprint(response)
        all_storage_pools = []
        for storage_pool_object in response:
            all_storage_pools.append(ScaleIO_Storage_Pool.from_dict(storage_pool_object))
        return all_storage_pools
    
    @property
    def sdc(self):
        """
        Returns a `list` of all the `ScaleIO_SDC` known to the cluster.  Updates every time - no caching.
        :return: a `list` of all the `ScaleIO_SDC` known to the cluster.
        :rtype: list
        """
        self._check_login()
        try:
            response = self._session.get(
                "{}/{}".format(self._api_url, "types/Sdc/instances")
                ).json()
        except:
            raise RuntimeError("sdc() property - Communication error with ScaleIO gateway")        
        all_sdc = []
        for sdc in response:
            all_sdc.append(
                ScaleIO_SDC.from_dict(sdc)
            )
        return all_sdc

    @property
    def sds(self):
        """
        Returns a `list` of all the `ScaleIO_SDS` known to the cluster.  Updates every time - no caching.
        :return: a `list` of all the `ScaleIO_SDS` known to the cluster.
        :rtype: list
        """
        self._check_login()
        try:
            response = self._session.get(
                "{}/{}".format(self._api_url,"types/Sds/instances")
                ).json()
        except:
            raise RuntimeError("sds() property - Communication error with ScaleIO gateway") 
        all_sds = []
        for sds in response:
            all_sds.append(
                ScaleIO_SDS.from_dict(sds)
            )
        return all_sds

    @property
    def volumes(self):
        """
        Returns a `list` of all the `ScaleIO_Volume` known to the cluster.  Updates every time - no caching.
        :return: a `list` of all the `ScaleIO_Volume` known to the cluster.
        :rtype: list
        """
        self._check_login()
        try:
            response = self._session.get(
                "{}/{}".format(self._api_url, "types/Volume/instances")
                ).json()
            
            print "*************"
            pprint (response)
            print "*************"
        except:
            raise RuntimeError("volumes() property - Communication error with ScaleIO gateway") 
        all_volumes = []
        for volume in response:
            #pprint(volume)
            all_volumes.append(
                ScaleIO_Volume.from_dict(volume)
            )
        return all_volumes


    @property
    def protection_domains(self):
        """
        :rtype: list
        """
        self._check_login()
        try:
            response = self._session.get(
                "{}/{}".format(self._api_url, "types/ProtectionDomain/instances")
                ).json()
        except:
            raise RuntimeError("sdc() property - Communication error with ScaleIO gateway") 
        all_pds = []
        for pd in response:
            #pprint(pd)
            all_pds.append(
                ScaleIO_Protection_Domain.from_dict(pd)
            )
        return all_pds

    def get_system_objects(self):
        return self.system

    def get_sds_by_name(self,name):
        for sds in self.sds:
            if sds.name == name:
                return sds
        raise KeyError("SDS of that name not found")

    def get_storage_pool_by_name(self, name):
        for storage_pool in self.storage_pools:
            if storage_pool.name == name:
                return storage_pool
        raise KeyError("Storage pool of that name not found")

    def get_storage_pool_by_id(self, id):
        for storage_pool in self.storage_pools:
            if storage_pool.id == id:
                return storage_pool
        raise KeyError("Storage Pool with that ID not found")

    def get_sds_by_ip(self,ip):
        if is_ip_addr(ip):
            for sds in self.sds:
                for sdsIp in sds.ipList:
                    if sdsIp == ip:
                        return sds
            raise KeyError("SDS of that name not found")
        else:
            raise ValueError("Malformed IP address - get_sds_by_ip()")
        
    def get_sds_by_id(self,id):
        for sds in self.sds:
            if sds.id == id:
                return sds
        raise KeyError("SDS with that ID not found")

    def get_sdc_by_name(self, name):
        for sdc in self.sdc:
            if sdc.name == name:
                return sdc
        raise KeyError("SDC of that name not found")

    def get_sdc_by_id(self, id):
        for sdc in self.sdc:
            if sdc.id == id:
                return sdc
        raise KeyError("SDC with that ID not found")

    def get_sdc_by_ip(self, ip):
        if is_ip_addr(ip):
            for sdc in self.sdc:
                if sdc.sdcIp == ip:
                    return sdc
            raise KeyError("SDS of that name not found")
        else:
            raise ValueError("Malformed IP address - get_sdc_by_ip()")
    
    def get_sdc_for_volume(self, volObj):
        sdcList = []
        for sdc in volObj.mapped_sdcs:
            sdcList.append(sdc)
        #if len(sdcList) == 0:
        return sdcList
    
    def get_pd_by_name(self, name):
        for pd in self.protection_domains:
            if pd.name == name:
                return pd
        raise KeyError("Protection Domain of that name not found")

    def get_pd_by_id(self, id):
        for pd in self.protection_domains:
            if pd.id == id:
                return pd
        raise KeyError("Protection Domain with that ID not found")
    
    def get_volume_by_id(self, id):
        for vol in self.volumes:
            if vol.id == id:
                return vol
        raise KeyError("Volume with that ID not found")

    def get_volume_by_name(self, name):
        for vol in self.volumes:
            #print "vol.name = " + vol.name
            if vol.name == name:
                return vol
        raise KeyError("Volume with that NAME not found")
    
    def get_volume_all_sdcs_mapped(self, volObj):
        if volObj.mappingToAllSdcsEnabled == True:
            return True
        return False
    
    def create_volume_snapshot_by_system_id(self, systemObj, snapVolumeList, **kwargs):
        """
        /api/instances /System::{id}/action/snapshotVolumes
        type: POST
        Required:
            snapshotDefs - a list of combination of "volumeId" volume ID and "snapshotName" (optional field) snapshot name.
            For example: { "snapshotDefs": [ {" volumeId":"2dd9132300000000", "snapshotName":"snap1"}, {"volumeId":"12342 }]}
        Return:
            volumeIdList snapshotGroupId
            for example:
            {"volumeIdList":[ "2dd9132400000001"], "snapshotGroupId":"d2e53daf00000001"}
        """
        snapshotDict = {'snapshotDefs': snapVolumeList}
        try:
            response = self._do_post("{}/{}{}/{}".format(self._api_url, "instances/System::", systemObj.id, 'action/snapshotVolumes'))
        except:
            raise RuntimeError("create_volume_snapshort_by_system_id() - Error communicating with ScaleIO gateway")
        return response
        
    def delete_volume_snapshot(self, snapshotObj, **kwargs):
        pass
        """
        /api/instances/System::{id}/action/removeConsistencyGroupSnapshots
        type: POST
        Required:
            snapGroupId
        Return:
            numberOfVolumes - number of volumes that were removed because of this operation
        
        """
        #mapVolumeToSdcDict = {'sdcId': sdcObj.id, 'allowMultipleMappings': str(allowMultipleMappings).upper()}
        try:
            response = self._do_post("{}/{}{}/{}".format(self._api_url, "instances/System::", snapshotObj.id, 'action/removeConsistencyGroupSnapshots'))
        except:
            raise RuntimeError("delete_volume_snapshot() - Error communicating wit ScaleIO gateway")
        
        return response
    
    def create_volume_by_pd_name(self, volName, volSizeInMb, pdObj, thinProvision=True, **kwargs):
        # TODO:
        # Check if object parameters are the correct ones, otherwise throw error
        self._check_login()    
        if thinProvision:
            volType = 'ThinProvisioned'
        else:
            volType = 'ThickProvisioned'
        volumeDict = {'protectionDomainId': pdObj.id, 'volumeSizeInKb': str(volSizeInMb * 1024),  'name': volName, 'volumeType': volType}
        pprint(volumeDict)
        response = self._do_post("{}/{}".format(self._api_url, "types/Volume/instances"), json=volumeDict)

        if kwargs:
            print "Map created volume to SDC(s)"
            for key, value in kwargs.iteritems():
                if key == 'mapAll':
                    if value == True:
                        self.map_volume_to_sdc(self.get_volume_by_name(volName), mapAll=True)
                if key == 'mapToSdc':
                    if value:
                        for innerKey, innerValue in kwargs.iteritems():
                            if innerKey == 'mapAll':
                                    if innerValue == True:
                                        self.map_volume_to_sdc(self.get_volume_y_name(volName), mapAll=True)
                                    else:
                                        self.map_volume_to_sdc(self.get_volume_by_name(volName), value)
        return response

    def map_volume_to_sdc(self, volumeObj, sdcObj=None, allowMultipleMappings=False, **kwargs):
        # TODO:
        # Check if object parameters are the correct ones, otherwise throw error
        self._check_login()
        if kwargs:
            for key, value in kwargs.iteritems():
                if key == 'mapAll':
                    if value == True:
                        mapVolumeToSdcDict = {'allSdcs': 'True'}
        else:
            mapVolumeToSdcDict = {'sdcId': sdcObj.id, 'allowMultipleMappings': str(allowMultipleMappings).upper()}
        response = self._do_post("{}/{}{}/{}".format(self._api_url, "instances/Volume::", volumeObj.id, 'action/addMappedSdc'), json=mapVolumeToSdcDict)
        return response
    
    def unmap_volume_from_sdc(self, volObj, sdcObj=None, **kwargs):
        # TODO:
        # Check if object parameters are the correct ones, otherwise throw error
        # ADD logic for ALL SDC UNMAP
        # For all SDC unmapVolumeFromDict = {'allSdc':'True'} False can be used
        self._check_login()
        if kwargs:
            for key, value in kwargs.iteritems():
                if key == 'disableMapAllSdcs':
                    if value == True:
                        if self.get_volume_all_sdcs_mapped:
                            unmapVolumeFromSdcDict = {'allSdcs': 'False'}
        else:
                unmapVolumeFromSdcDict = {'sdcId': sdcObj.id}
        try:
            response = self._do_post("{}/{}{}/{}".format(self._api_url, "instances/Volume::", volObj.id, 'action/removeMappedSdc'), json=unmapVolumeFromSdcDict)
        except:
            raise RuntimeError("unmap_volume_from_sdc() - Communication error with ScaleIO gateway")
        return response

    def delete_volume(self, volObj, removeMode='ONLY_ME', **kwargs):
        """
        removeMode = 'ONLY_ME' | 'INCLUDING_DESCENDANTS' | 'DESCENDANTS_ONLY' | 'WHOLE_VTREE'
        Using kwargs it will be possible to tell delete_volume() to unmap all SDCs before delting. Not working yet
        """
        if kwargs:
            for key, value in kwargs.iteritems():
                if key =='autoUnmap':
                    # Find all mapped SDS to this volObj
                    # Call unmap for all of them
                    if self.get_volume_all_sdcs_mapped:
                        try:
                            self.unmap_volume_from_sdc(volObj, disableMapAllSdcs=True)
                        except:
                            raise RuntimeError("delete_volume() - Communication error with ScaleIO gateway")
        else:
            for sdcIdentDict in self.get_sdc_for_volume(volObj):
                try:
                    self.unmap_volume_from_sdc(volObj, sio.get_sdc_by_id(sdcIdentDict.sdcId))
                except:
                    raise RuntimeError("delete_volume() - Communication error with ScaleIO gateway")
        # TODO:
        # Check if object parameters are the correct ones, otherwise throw error
        self._check_login()
        deleteVolumeDict = {'removeMode': removeMode}
        try:
            response = self._do_post("{}/{}{}/{}".format(self._api_url, "instances/Volume::", volObj.id, 'action/removeVolume'), json=deleteVolumeDict)
        except:
            raise RuntimeError("delete_volume() - Communication error with ScaleIO Gateway")
        return response
    
 
    def delete_sdc_from_cluster(self, sdcObj):
        # TODO:
        # Check if object parameters are the correct ones, otherwise throw error
        self._check_login() 
        response = self._do_post("{}/{}{}/{}".format(self._api_url, "instances/Sdc::", sdcObj.id, 'action/removeSdc'))    
        return response  

    def set_sdc_name(self, name, sdcObj):
        # TODO:
        # Check if object parameters are the correct ones, otherwise throw error
        self._check_login()
        deleteVolumeDict = {'sdcName': name}
        response = self._do_post("{}/{}{}/{}".format(self._api_url, "instances/Sdc::", sdcObj.id, 'action/setSdcName'), json=unmapVolumeFromSdcDict)    
        return response
    
    #def set_volume_map_to_all_sdcs(self, volObj, enabled=False):
    #    self._check_login()
    # Research: Can there still exsit individual SDC mappings? API Guide say nothing about it.
    #    return self.map_volume_to_sdc(volobj, mapAll=True)
    
    def unregisterSdc(self, sdcObj):
        self._check_login()
        response = self._do_post("{}/{}{}/{}".format(self._api_url, "instances/Sdc::", sdcObj.id, 'action/removeSdc'), json=unmapVolumeFromSdcDict)    
        return response
    
    
    
     
    def is_ip_addr(ipstr):
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
    
    
    

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s: %(levelname)s %(module)s:%(funcName)s | %(message)s', level=logging.WARNING)
    if len(sys.argv) == 1:
        print "Usage: scaleio.py mdm_ip user pass"
    else:
        sio = ScaleIO("https://" + sys.argv[1] + "/api",sys.argv[2],sys.argv[3],verify_ssl=False) # HTTPS must be used as there seem to be an issue with 302 responses in Requests when using POST
        pprint(sio.system)
        pprint(sio.sdc)
        pprint(sio.sds)
        pprint(sio.volumes)
        pprint(sio.protection_domains)
        pprint(sio.storage_pools)
    