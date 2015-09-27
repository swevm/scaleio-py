# Imports

# Project imports
from scaleiopy.api.scaleio.mapping.sio_generic_object import SIO_Generic_Object
from scaleiopy.api.scaleio.mapping.link import Link


#class ScaleIO_Fault_Set(SIO_Generic_Object):
class Fault_Set(SIO_Generic_Object):

    """ ScaleIO Faultset Class repreentation """
    
    def __init__(self,
        id=None,
        name=None,
        protectionDomainId=None,
        links=None

    ):
        self.id=id
        self.name=name
        self.protectionDomainId=protectionDomainId
        self.links = []
        for link in links:
            self.links.append(Link(link['href'],link['rel']))

    @staticmethod
    def from_dict(dict):
        """
        A convenience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return Fault_Set(**dict)
    