# Imports
from im_generic_object import Im_Generic_Object

class Remote_Syslog_Configuration_Object(Im_Generic_Object):
    """
    Python object representation of a Remote Syslog Logging.
    """
    
    def __init__(self,
        ip=None,
        port=None,
        facility=None
    ):
        self.ip=ip
        self.port=port
        self.facility=facility #Must be a number between 1-23

    @staticmethod
    def from_dict(dict):
        """
        A convinience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return Remote_Syslog_Configuration_Object(**dict)
    