import json
import requests
import time
from requests.auth import HTTPBasicAuth
from requests_toolbelt import SSLAdapter
from requests_toolbelt import MultipartEncoder
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl
import logging
import time
from os import listdir
from os.path import isfile, join
import logging

from pprint import pprint


class Im_Generic_Object(object):
    @classmethod
    def get_class_name(cls):
        """
        A helper method that returns the name of the class.  Used by __str__ below
        """
        return cls.__name__

    def __str__(self):
        """
        A convinience method to pretty print the contents of the class instance
        """
        # to show include all variables in sorted order
        return "<{}> @ {}:\n".format(self.get_class_name(), id(self)) + "\n".join(
            ["  %s: %s" % (key.rjust(22), self.__dict__[key]) for key in sorted(set(self.__dict__))])

    def __repr__(self):
        return self.__str__()
    
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def to_DICT(self):
        return self.__dict__
    
class ScaleIO_Node_Object(Im_Generic_Object):
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
        return ScaleIO_Node_Object(**dict)

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

class Mdm_Object(Im_Generic_Object):
    """
    Python object representation of a MDM (primary or secondary look eactly the same configuration wise).
    """
    
    def __init__(self,
        node=None,
        nodeInfo=None,
        managementIPs=None,
        mdmIPs = None
    ):
        self.managementIPs=[]
        if managementIPs:
            for mgmtIP in managementIPs:
                self.managementIPs.append(mgmtIP)
        self.node=ScaleIO_Node_Object.from_dict(node)
        self.nodeInfo=nodeInfo
        self.mdmIPs = []
        if mdmIPs:
            for mdmIP in mdmIPs:
                self.mdmIPs.append(mdmIP)
                
    @staticmethod
    def from_dict(dict):
        """
        A convinience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return Mdm_Object(**dict)

class Tb_Object(Im_Generic_Object):
    """
    Python object representation of a TB.
    """
    
    def __init__(self,
        node=None,
        nodeInfo=None,
        tbIPs=None
    ):
        self.node=ScaleIO_Node_Object.from_dict(node)
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

class Sdc_Object(Im_Generic_Object):
    """
    Python object representation of a MDM (primary or secondary look eactly the same configuration wise).
    """
    
    def __init__(self,
        node=None,
        nodeInfo=None,
        splitterRpaIp=None
    ):
        self.node=ScaleIO_Node_Object.from_dict(node)
        self.nodeInfo=nodeInfo
        self.splitterRpaIp=splitterRpaIp
        
    @staticmethod
    def from_dict(dict):
        """
        A convinience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return Sdc_Object(**dict)

class Sds_Device_Object(Im_Generic_Object):
    """
    Python object representation of a MDM (primary or secondary look eactly the same configuration wise).
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

class Sds_Object(Im_Generic_Object):
    """
    Python object representation of a SDS.
    """
    
    def __init__(self,
        node=None,
        nodeInfo=None,
        sdsName=None,
        protectionDomain=None,
        faultSet=None,
        allIPs=None,
        sdsOnlyIPs=None,
        sdcOnlyIPs=None,
        devices=None,
        optimized=None,
        port=None
    ):
        self.node=ScaleIO_Node_Object.from_dict(node)
        self.nodeInfo=nodeInfo
        self.sdsName=sdsName
        self.protectionDomain = protectionDomain
        self.faultSet=faultSet
        self.allIPs=[]
        for allIp in allIPs:
            self.allIPs.append(allIp)
        self.sdsOnlyIPs=[]
        if sdsOnlyIPs:
            for sdsOnlyIp in sdsOnlyIPs:
                self.sdsOnlyIPs.append(sdsOnlyIp)
        self.sdcOnlyIPs=[]
        if sdcOnlyIPs:
            for sdcOnlyIp in sdcOnlyIPs:
                self.sdcOnlyIPs.append(sdcOnlyIp)
        self.devices=[]
        if devices:
            for device in devices:
                self.devices.append(Sds_Device_Object.from_dict(device))
        self.optimized=optimized
        self.port=port
    
    def addDevice(self, devicePath, storagePool, deviceName):
        #print "Add Device:"
        device_dict = {'devicePath': devicePath, 'storagePool': storagePool, 'deviceName': deviceName}
        #pprint (device_dict) #(Sds_Device_Object(devicePath, storagePool, deviceName).to_JSON())
        self.devices.append(Sds_Device_Object.from_dict(device_dict))
        
    def removeDevice(devObject):
        pass
    
        
    @staticmethod
    def from_dict(dict):
        """
        A convinience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return Sds_Object(**dict)

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
        if dict['callHomeConfiguration'] == 'None':
            return None
        return Call_Home_Configuration_Object(**dict)

class Remote_Syslog_Configuration_Object(Im_Generic_Object):
    """
    Python object representation of a MDM (primary or secondary look eactly the same configuration wise).
    """
    
    def __init__(self,
        ip=None,
        port=None,
        facility=None
    ):
        self.ip=ip
        self.port=port
        self.facility=facility
        
    @staticmethod
    def from_dict(dict):
        """
        A convinience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        if dict['remoteSysogConfiguration'] == 'None':
            return None
        return Remote_Syslog_Configuration_Object(**dict)

class ScaleIO_System_Object(Im_Generic_Object):
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
            self.callHomeConfiguration=Call_Home_Configuration_Object.from_dict(callHomeConfiguration)
        if remoteSyslogConfiguration is None:
            self.remoteSyslogConfiguration = None
        else:
            self.remoteSyslogConfiguration=Remote_Syslog_Configuration_Object.from_dict(remoteSyslogConfiguration)

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
        A convinience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return ScaleIO_System_Object(**dict)
    


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s: %(levelname)s %(module)s:%(funcName)s | %(message)s', level=logging.WARNING)
    print "Cannot run this code by direct call to script"
