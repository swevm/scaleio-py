# Imports
from im_generic_object import Im_Generic_Object

class Primary_Mdm_Object(Im_Generic_Object):
    """
    Python object representation of a MDM (Primary and Secondary look the same configuration wise.
    """
    
    def __init__(self,
        node=None,
        nodeInfo=None,
        managementIPs=None,
        mdmIPs=None
    ):
        # Data retrieved is a JSON representation of a primary MDM with 'node' as its root
        self.managementIPs=[]
        if managementIPs:
            for mgmtIP in managementIPs:
                self.managementIPs.append(mgmtIP)
        self.node=ScaleIO_Node_Object.from_dict(node)
        self.nodeInfo=nodeInfo
        
    @staticmethod
    def from_dict(dict):
        """
        A convinience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return Primary_Mdm_Object(**dict)


