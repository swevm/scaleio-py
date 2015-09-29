# Imports

# Project imports
from scaleiopy.api.scaleio.mapping.sio_generic_object import SIO_Generic_Object
from scaleiopy.api.scaleio.mapping.ip_list import SIO_IP_List
from scaleiopy.api.scaleio.mapping.link import SIO_Link

#class ScaleIO_SDS(SIO_Generic_Object):
class SIO_SDS(SIO_Generic_Object):
    """ ScaleIO SDS Class representation """
    
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
            self.ip_list.append(SIO_IP_List(ip['ip'],ip['role']))
        self.fault_set_id = faultSetId
        self.id = id
        self.links = []
        for link in links:
            self.links.append(SIO_Link(link['href'],link['rel']))
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
        A convenience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return SIO_SDS(**dict)
 