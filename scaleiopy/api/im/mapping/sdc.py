# Imports
from im_generic_object import Im_Generic_Object
from node import Node_Object

class Sdc_Object(Im_Generic_Object):
    """
    Python object representation of a MDM (primary or secondary look eactly the same configuration wise).
    """
    
    def __init__(self,
        node=None,
        nodeInfo=None,
        splitterRpaIp=None
    ):
        self.node=Node_Object.from_dict(node)
        self.nodeInfo=nodeInfo
        self.splitterRpaIp=splitterRpaIp
        
    @staticmethod
    def from_dict(dict):
        """
        A convinience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return Sdc_Object(**dict)
