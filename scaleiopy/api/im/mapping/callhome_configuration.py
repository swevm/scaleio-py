# Imports
from im_generic_object import Im_Generic_Object

class Call_Home_Configuration_Object(Im_Generic_Object):
    """
    Python object representation of a MDM (primary or secondary look eactly the same configuration wise).
    """
    
    def __init__(self,
        emailFrom=None,
        mdmUsername=None,
        mdmPassword=None,
        customerName=None,
        host=None,
        port=None,
        tls=None,
        smtpUsername=None,
        smtpPassword=None,
        alertEmailTo=None,
        severity=None
    ):
        self.emailFrom=emailFrom
        self.mdmUsername=mdmUsername
        self.mdmPassword=mdmPassword
        self.customerName=customerName
        self.host=host
        self.port=port
        self.tls=tls
        self.smtpUsername=smtpUsername
        self.smtpPassword=smtpPassword
        self.alertEmailTo=alertEmailTo
        self.severity=severity

    @staticmethod
    def from_dict(dict):
        """
        A convinience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return Call_Home_Configuration_Object(**dict)
