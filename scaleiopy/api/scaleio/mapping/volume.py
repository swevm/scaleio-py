# Imports

# Project imports
from scaleiopy.api.scaleio.mapping.sio_generic_object import SIO_Generic_Object
from scaleiopy.api.scaleio.mapping.link import Link
import time

#class ScaleIO_Volume(SIO_Generic_Object):
class Volume(SIO_Generic_Object):

    """ ScaleIO Volume Class representation """
    
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
        A convenience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return Volume(**dict)
