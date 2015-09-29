# Imports

# External imports


# Project imports
from scaleiopy.api.scaleio.mapping.sio_generic_object import SIO_Generic_Object

from scaleiopy.api.scaleio.mapping.faultset import SIO_Fault_Set
from scaleiopy.api.scaleio.mapping.ip_list import SIO_IP_List
from scaleiopy.api.scaleio.mapping.link import SIO_Link
from scaleiopy.api.scaleio.mapping.protection_domain import SIO_Protection_Domain
from scaleiopy.api.scaleio.mapping.sdc import SIO_SDC
from scaleiopy.api.scaleio.mapping.sds import SIO_SDS
from scaleiopy.api.scaleio.mapping.snapshotspecification import SIO_SnapshotSpecification
from scaleiopy.api.scaleio.mapping.storage_pool import SIO_Storage_Pool
from scaleiopy.api.scaleio.mapping.volume import SIO_Volume
from scaleiopy.api.scaleio.mapping.vtree import SIO_Vtree

#class ScaleIO_System(SIO_Generic_Object):
class SIO_System(SIO_Generic_Object):

    """ Represents one ScaleIO cluster/installation as a class object  - Owns other classes that represents differenct ScaleIO components """
    
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
        self.id=id
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
        self.max_capacity_in_gb = maxCapacityInGb
        self.capacity_time_left_in_days = capacityTimeLeftInDays 
        self.enterprise_features_enabled = enterpriseFeaturesEnabled
        self.default_is_volume_obfuscated = defaultIsVolumeObfuscated
        self.is_initial_license = isInitialLicense
        self.restricted_sdc_mode_enabled = restrictedSdcModeEnabled
        self.remote_readonly_limit_state = remoteReadOnlyLimitState
        self.links = []
        for link in links:
            self.links.append(SIO_Link(link['href'],link['rel']))        
        

    @staticmethod
    def from_dict(dict):
        """
        A convenience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return SIO_System(**dict)
    