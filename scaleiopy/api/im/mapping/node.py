# Imports
from im_generic_object import Im_Generic_Object

#class ScaleIO_Node_Object(Im_Generic_Object):
class Node_Object(Im_Generic_Object):
    """
    Do not use. Will be the common denominator for ScaleIO configuration nodes.
    All config object should inherit this base
    """
    
    def __init__(self,
        domain=None,
        liaPassword=None,
        nodeIPs=None,
        nodeName=None,
        ostype=None,
        password=None,
        userName=None
    ):
        self.domain=domain
        self.liaPassword=liaPassword
        self.nodeIPs=[]
        if nodeIPs:
            for nodeIp in nodeIPs:
                self.nodeIPs.append(nodeIp)
        self.nodeName=nodeName
        self.ostype=ostype
        self.password=password
        self.userName=userName
    
    @staticmethod
    def from_dict(dict):
        """
        A convinience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return Node_Object(**dict)

