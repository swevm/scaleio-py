# Imports
from im_generic_object import Im_Generic_Object
from node import Node_Object
from sds_device import Sds_Device_Object

class Sds_Object(Im_Generic_Object):
    """
    Python object representation of a SDS.
    To add a SDS to a faultset this is where its done. SDSs cannot be added to FaultSets after they have been added to protectiondomain. API wise they can be removed and re added (not sure how re-add is done though)
    
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
        self.node=Node_Object.from_dict(node)
        self.nodeInfo=nodeInfo
        self.sdsName=sdsName
        self.protectionDomain = protectionDomain
        self.faultSet=faultSet # Is this as easy as giving a string with a Faultset name??? (Its not documented)
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
