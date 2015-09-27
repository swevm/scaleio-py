# Imports

from mapping.im_generic_object import Im_Generic_Object

from scaleiopy.api.im.mapping.node import Node_Object
from scaleiopy.api.im.mapping.mdm import Mdm_Object
from scaleiopy.api.im.mapping.callhome_configuration import Call_Home_Configuration_Object
from scaleiopy.api.im.mapping.tb import Tb_Object
from scaleiopy.api.im.mapping.syslog_configuration import Remote_Syslog_Configuration_Object
from scaleiopy.api.im.mapping.sdc import Sdc_Object
from scaleiopy.api.im.mapping.sds import Sds_Object
from scaleiopy.api.im.mapping.sds_device import Sds_Device_Object
#from scaleiopy.api.im.system import System_Object

class System_Object(Im_Generic_Object):
    """
    Root configuration object
    """

    def __init__(self,
        installationId=None,
        mdmIPs=None,
        mdmPassword=None,
        liaPassword=None,
        licenseKey=None,
        primaryMdm=None,
        secondaryMdm=None,
        tb=None,
        sdsList=None,
        sdcList=None,
        callHomeConfiguration=None,
        remoteSyslogConfiguration=None
        
    ):
        self.installationId=installationId
        self.mdmIPs = []
        for mdmIP in mdmIPs:
            self.mdmIPs.append(mdmIP)
        self.mdmPassword=mdmPassword
        self.liaPassword=liaPassword
        self.licenseKey=licenseKey
        self.primaryMdm=Mdm_Object.from_dict(primaryMdm)
        self.secondaryMdm=Mdm_Object.from_dict(secondaryMdm)
        self.tb=Tb_Object.from_dict(tb)
        self.sdsList=[]
        for sds in sdsList:
            self.sdsList.append(Sds_Object.from_dict(sds))
        self.sdcList=[]
        for sdc in sdcList:
            self.sdcList.append(Sdc_Object.from_dict(sdc))
        if callHomeConfiguration is None:
            self.callHomeConfiguration = None
        else:
            self.callHomeConfiguration = callHomeConfiguration
        if remoteSyslogConfiguration is None:
            self.remoteSyslogConfiguration = None
        else:
            # Might be a good idea to check type(remoteSyslogConfiguration) and verify class type
            self.remoteSyslogConfiguration = remoteSyslogConfiguration
    def setLiaPassword(self, value):
        self.liaPassword = value
        
    def setMdmPassword(self, value):
        self.mdmPassword = value
    
    def addSds(self, sdsObj):
        self.sdsList.append(sdsObj)
    
    def removeSds(self, sdsObj):
        pass
    
    def addSdc(self, sdcObj):
        pass
    
    def removeSdc(self, sdcObj):
        pass
    
    def addCallHomeConfiguration(self, callhomeConfObj):
        self.callHomeConfiguration = callhomeConfObj.to_JSON()
    
    def removeCallHomeConfiguration(self):
        self.callHomeConfiguration = None
    
    def addSyslogConfiguration(self, syslogConfObj):
        self.remoteSyslogConfiguration = callhomeConfObj.to_JSON()
    
    def removeSyslogConfiguration(self):
        self.remoteSyslogConfiguration = None
    
    def addPrimaryMdm(self, mdmObj):
        pass
    
    def addSecondaryMdm(self, mdmObj):
        pass
    
    def addTb(self, tbObj):
        pass
    
    
    
    @staticmethod
    def from_dict(dict):
        """
        A convenience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return ScaleIO_System_Object(**dict)
    
