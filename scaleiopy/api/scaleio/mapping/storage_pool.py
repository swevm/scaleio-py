# Import

# Project imports
from scaleiopy.api.scaleio.mapping.sio_generic_object import SIO_Generic_Object
from scaleiopy.api.scaleio.mapping.link import Link


class Storage_Pool(SIO_Generic_Object):
    """ ScaleIO Storage Pool Class representation """
    
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
        rmcacheWriteHandlingMode=None, #Passthrough or Cached
        # v1.32 specific
        backgroundScannerMode = None, 
        backgroundScannerBWLimitKBps = None
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
        # v1.32 specific
        self.backgroundScanneMode = backgroundScannerMode
        self.backgroundScannerBWLimitKBps = backgroundScannerBWLimitKBps
    @staticmethod
    def from_dict(dict):
        """
        A convenience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return Storage_Pool(**dict)
