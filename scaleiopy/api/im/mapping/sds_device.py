# Imports
from im_generic_object import Im_Generic_Object

class Sds_Device_Object(Im_Generic_Object):
    """
    Python object representation of a SDS Device

    """
    
    def __init__(self,
        devicePath=None,
        storagePool=None,
        deviceName=None
    ):
        self.devicePath=devicePath
        self.storagePool=storagePool
        self.deviceName=deviceName
    
    @staticmethod
    def from_dict(dict):
        """
        A convinience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return Sds_Device_Object(**dict)


