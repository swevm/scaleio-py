# Imports

# Project imports
from scaleiopy.api.scaleio.mapping.sio_generic_object import SIO_Generic_Object
from scaleiopy.api.scaleio.mapping.link import Link

#class ScaleIO_SDC(SIO_Generic_Object):
class SDC(SIO_Generic_Object):
    """ ScaleIO SDC Class representation """
    
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
        self.guid = sdcGuid
        self.links = []
        for link in links:
            self.links.append(Link(link['href'], link['rel']))

    @staticmethod
    def from_dict(dict):
        """
        A convenience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return SDC(**dict)
