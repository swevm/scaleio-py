# Imports

# Project imports
from scaleiopy.api.scaleio.mapping.sio_generic_object import SIO_Generic_Object
from scaleiopy.api.scaleio.mapping.link import SIO_Link


#class ScaleIO_Vtree(SIO_Generic_Object):
class SIO_Vtree(SIO_Generic_Object):
    """ ScaleIO VTree Class repreentation
        For every Volume created there alway at least one VTree
    """
    
    def __init__(self,
        id=None,
        name=None,
        baseVolumeId=None,
        storagePoolId=None,
        links=None
    ):
        self.id=id
        self.name=name
        self.baseVolumeId=baseVolumeId
        self.storagePoolId=storagePoolId
        self.links = []
        for link in links:
            self.links.append(SIO_Link(link['href'],link['rel']))
            
    @staticmethod
    def from_dict(dict):
        """
        A convenience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return SIO_Vtree(**dict)

