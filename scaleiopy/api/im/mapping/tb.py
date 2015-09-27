# Imports
from im_generic_object import Im_Generic_Object
from node import Node_Object

class Tb_Object(Im_Generic_Object):
    """
    Python object representation of a TB.
    """
    
    def __init__(self,
        node=None,
        nodeInfo=None,
        tbIPs=None
    ):
        self.node=Node_Object.from_dict(node)
        self.nodeInfo=nodeInfo
        self.tbIPs=[]
        if tbIPs:
            for tbIp in tbIPs:
                self.tbIPs.append(tbIp)
        
    @staticmethod
    def from_dict(dict):
        """
        A convinience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        #print "*** Class Tb_Object, from_dict(**dict) method:"
        #pprint (dict)
        return Tb_Object(**dict)
