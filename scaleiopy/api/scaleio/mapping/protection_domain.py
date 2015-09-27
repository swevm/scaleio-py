# Imports

# Project imports
from scaleiopy.api.scaleio.mapping.sio_generic_object import SIO_Generic_Object
from scaleiopy.api.scaleio.mapping.link import Link


class Protection_Domain(SIO_Generic_Object):
#class SIO_Protection_Domain(SIO_Generic_Object):
    """ ScaleIO Protection Domain Class representation """
    
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
        A convenience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return Protection_Domain(**dict)
