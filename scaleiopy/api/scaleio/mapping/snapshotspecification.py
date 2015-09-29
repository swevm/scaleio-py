# Imports

# Project imports
from scaleiopy.api.scaleio.mapping.sio_generic_object import SIO_Generic_Object


class SIO_SnapshotSpecification(SIO_Generic_Object):
    """
    Input: list of SIO Snapshot definitions
            For example: { "snapshotDefs": [ {" volumeId":"2dd9132300000000", "snapshotName":"000_snap1"}, {"volumeId":"2dd9132300000004", "snapshotName":"004_snap1" }]}
    If adding more than one Volume to a Snapshot definition it will autoamtically be trated as a consistency group
    
    Return:
        volumeIdList snapshotGroupId
        for example:
        {"volumeIdList":[ "2dd9132400000001"], "snapshotGroupId":"d2e53daf00000001"}
    """
    def __init__(self):
        self._snapshotList = []
    
    def addVolume(self, volObj, snapName=None):
        if snapName is None:
            self._snapshotList.append({"volumeId": volObj.id, "snapshotName": volObj.name + "snapshot"})
        else:
            self._snapshotList.append({"volumeId": volObj.id, "snapshotName": snapName})

    def removeVolume(self, volObj):
        for i in range(len(self._snapshotList)):
            if self._snapshotList[i]['volumeId'] == volObj.id:
                del self._snapshotList[i]
                break
    
    def __to_dict__(self):
        return {"snapshotDefs" : self._snapshotList}

