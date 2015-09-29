# Standard lib imports
# None

# Third party imports
# None

# Project level imports
from scaleiopy.api.scaleio.mapping.volume import SIO_Volume



class Volume(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection        

    @property
    def get(self):
        pass
    
    def create_volume(self, volName, volSizeInMb, pdObj, spObj, thinProvision=True, **kwargs): #v1.32 require storagePoolId when creating a volume
        # Check if object parameters are the correct ones, otherwise throw error
        self.conn.connection._check_login()    
        if thinProvision:
            volType = 'ThinProvisioned'
        else:
            volType = 'ThickProvisioned'
        # ScaleIO v1.31 demand protectionDomainId in JSON but not storgePoolId. v1.32 is fine with storeagePoolId only
        volumeDict = {'protectionDomainId': pdObj.id, 'storagePoolId': spObj.id, 'volumeSizeInKb': str(int(volSizeInMb) * 1024),  'name': volName, 'volumeType': volType}
        response = self.conn.connection._do_post("{}/{}".format(self.conn.connection._api_url, "types/Volume/instances"), json=volumeDict)

        if kwargs:
            for key, value in kwargs.iteritems():
                if key == 'enableMapAllSdcs' and value == True:
                    self.map_volume_to_sdc(self.conn.connection.get_volume_by_name(volName), enableMapAllSdcs=True)
                if key == 'mapToSdc':
                    if value:
                        for innerKey, innerValue in kwargs.iteritems():
                            if innerKey == 'enableMapAllSdcs':
                                    if innerValue == True:
                                        self.map_volume_to_sdc(self.conn.connection.get_volume_by_name(volName), enableMapAllSdcs=True)
                                    else:
                                        self.map_volume_to_sdc(self.conn.connection.get_volume_by_name(volName), self.get_sdc_by_name(value))
        return response

    def is_valid_volsize(self,volsize):
        """
        Convenience method that round input to valid ScaleIO Volume size (8GB increments)
        :param volsize: Size in MB
        :rtype int: Valid ScaleIO Volume size rounded to nearest 8GB increment above or equal to volsize
        """
        
        if type(volsize) is int:
            size_temp = divmod(volsize, 8192)
            if size_temp[1] > 0: # If not on 8GB boundary
                return int((1 + size_temp[0]) * 8192) # Always round to next 8GB increment
        else:
            return int(volsize)

    def delete_volume(self, volObj, removeMode='ONLY_ME', **kwargs):
        """
        removeMode = 'ONLY_ME' | 'INCLUDING_DESCENDANTS' | 'DESCENDANTS_ONLY' | 'WHOLE_VTREE'
        Using kwargs it will be possible to tell delete_volume() to unmap all SDCs before delting. Not working yet
        """
        if kwargs:
            for key, value in kwargs.iteritems():
                if key =='autoUnmap' and value ==True:
                    # Find all mapped SDS to this volObj
                    # Call unmap for all of them
                    if self.get_volume_all_sdcs_mapped(volObj):
                        try:
                            self.conn.cluster.unmap_volume_from_sdc(volObj, enableMapAllSdcs=False)
                        except:
                            raise RuntimeError("delete_volume() - enableMapAllSdcs error")
                    else: # All SDS not enabled so loop through all mapped SDCs of volume and remove one by one                        
                        for sdc in self.get_sdc_for_volume(volObj):
                            try:
                                self.unmap_volume_from_sdc(volObj, self.get_sdc_by_id(sdc['sdcId']))
                            except:
                                raise RuntimeError("delete_volume() - unmap_volume_from_sdc() error")
        # TODO:
        # Check if object parameters are the correct ones, otherwise throw error
        self.conn.connection._check_login()
        deleteVolumeDict = {'removeMode': removeMode}
        try:
            response = self.conn.connection._do_post("{}/{}{}/{}".format(self.conn.connection._api_url, "instances/Volume::", volObj.id, 'action/removeVolume'), json=deleteVolumeDict)
        except:
            raise RuntimeError("delete_volume() - Communication error with ScaleIO Gateway")
        return response
    

    def map_volume_to_sdc(self, volumeObj, sdcObj=None, allowMultipleMappings=False, **kwargs):
        """
        Map a Volume to SDC
        :param volumeObj: ScaleIO Volume object
        :param sdcObj: ScaleIO SDC object
        :param allowMultipleMappings: True to allow more than one SDC to be mapped to volume
        :return: POST request response
        :rtype: Requests POST response object
        """
        self.conn.connection._check_login()
        if kwargs:
            for key, value in kwargs.iteritems():
                if key == 'enableMapAllSdcs':
                    if value == True:
                        mapVolumeToSdcDict = {'allSdcs': 'True'}
        else:
            mapVolumeToSdcDict = {'sdcId': sdcObj.id, 'allowMultipleMappings': str(allowMultipleMappings).upper()}
        response = self.conn.connection._do_post("{}/{}{}/{}".format(self._api_url, "instances/Volume::", volumeObj.id, 'action/addMappedSdc'), json=mapVolumeToSdcDict)
        return response

    def get_volume_all_sdcs_mapped(self, volObj):
        if volObj.mappingToAllSdcsEnabled == True:
            return True
        return False

    def unmap_volume_from_sdc(self, volObj, sdcObj=None, **kwargs):
        """
        Unmap a Volume from SDC or all SDCs
        :param volObj: ScaleIO Volume object
        :param sdcObj: ScaleIO SDC object
        :param \**kwargs:
        :Keyword Arguments:
        *disableMapAllSdcs* (``bool``) -- True to disable all SDCs mapping
        :return: POST request response
        :rtype: Requests POST response object
        :raise RuntimeError: If failure happen during communication with REST Gateway - Need to be cleaned up and made consistent to return understandable errors
        """
        # TODO:
        # Check if object parameters are the correct ones, otherwise throw error
        # ADD logic for ALL SDC UNMAP
        # For all SDC unmapVolumeFromDict = {'allSdc':'True'} False can be used
        self.conn.connection._check_login()
        if kwargs:
            for key, value in kwargs.iteritems():
                if key == 'enableMapAllSdcs' and value == False:
                    if self.get_volume_all_sdcs_mapped(volObj): # Check if allSdc?s is True before continuing
                        unmapVolumeFromSdcDict = {'allSdcs': 'False'}
        else:
                unmapVolumeFromSdcDict = {'sdcId': sdcObj.id}
        try:
            response = self.conn.connection._do_post("{}/{}{}/{}".format(self.conn.connection._api_url, "instances/Volume::", volObj.id, 'action/removeMappedSdc'), json=unmapVolumeFromSdcDict)
        except:
            raise RuntimeError("unmap_volume_from_sdc() - Cannot unmap volume")
        return response


    def get_volumes_for_sdc(self, sdcObj):
        """
        :param sdcObj: SDC object
        :return: list of Volumes attached to SDC
        :rtyoe: ScaleIO Volume object
        """
        self.conn.connection._check_login()
        all_volumes = []
        response = self.conn.connection._do_get("{}/{}{}/{}".format(self.conn.connection._api_url, 'instances/Sdc::', sdcObj.id, 'relationships/Volume')).json()
        for sdc_volume in response:
            all_volumes.append(
                Volume.from_dict(sdc_volume)
            )
        return all_volumes

    def get_volume_by_id(self, id):
        """
        Get ScaleIO Volume object by its ID
        :param name: ID of volume
        :return: ScaleIO Volume object
        :raise KeyError: No Volume with specified ID found
        :rtype: ScaleIO Volume object
        """
        for vol in self.conn.volumes:
            if vol.id == id:
                return vol
        raise KeyError("Volume with ID " + id + " not found")
    
    def get_volumes_for_vtree(self, vtreeObj):
        """
        :param vtreeObj: VTree object
            Protection Domain Object
        :return: list of Volumes attached to VTree
        :rtype: ScaleIO Volume object
        """
        self.conn.connection._check_login()
        all_volumes = []
        response = self._do_get("{}/{}{}/{}".format(self.conn.connection._api_url, 'instances/VTree::', vtreeObj.id, 'relationships/Volume')).json()
        for vtree_volume in response:
            all_volumes.append(
                Volume.from_dict(vtree_volume)
            )
        return all_volumes

    def get_volume_by_name(self, name):
        """
        Get ScaleIO Volume object by its Name
        :param name: Name of volume
        :return: ScaleIO Volume object
        :raise KeyError: No Volume with specified name found
        :rtype: ScaleIO Volume object
        """
        for vol in self.conn.volumes:
            if vol.name == name:
                return vol
        raise KeyError("Volume with NAME " + name + " not found")
    
    
    def resize_volume(self, volumeObj, sizeInGb, bsize=1000):
        """
        Resize a volume to new GB size, must be larger than original.
        :param volumeObj: ScaleIO Volume Object
        :param sizeInGb: New size in GB (have to be larger than original)
        :param bsize: 1000
        :return: POST request response
        :rtype: Requests POST response object
        """
        current_vol = self.get_volume_by_id(volumeObj.id)
        if current_vol.size_kb > (sizeInGb * bsize * bsize):
            raise RuntimeError(
                "resize_volume() - New size needs to be bigger than: %d KBs" % current_vol.size_kb)
        
        resizeDict = { 'sizeInGB' : str(sizeInGb) }
        response = self.conn.connection._do_post("{}/{}{}/{}".format(
            self.conn.connection._api_url, "instances/Volume::", volumeObj.id, 'action/setVolumeSize'), json=resizeDict)
        return response
    
    def create_snapshot(self, systemId, snapshotSpecificationObject):
        """
        Create snapshot for list of volumes
        :param systemID: Cluster ID 
        :param snapshotSpecificationObject: Of class SnapshotSpecification
        :rtype: SnapshotGroupId
        """
        self.conn.connection._check_login()
        #try:
        response = self.conn.connection._do_post("{}/{}{}/{}".format(self.conn.connection._api_url, "instances/System::", systemId, 'action/snapshotVolumes'), json=snapshotSpecificationObject.__to_dict__())
        #except:
        #    raise RuntimeError("create_snapshot_by_system_id() - Error communicating with ScaleIO gateway")
        return response
        
    def delete_snapshot(self, systemId, snapshotGroupId):
        """
        :param systemId: ID of Cluster
        :param snapshotGroupId: ID of snapshot group ID to be removed
        
        
        /api/instances/System::{id}/action/removeConsistencyGroupSnapshots
        type: POST
        Required:
            snapGroupId
        Return:
            numberOfVolumes - number of volumes that were removed because of this operation
        
        """
        #try:
        consistencyGroupIdDict = {'snapGroupId':snapshotGroupId}
        self.conn.connection._check_login()
        response = self.conn.connection._do_post("{}/{}{}/{}".format(self.conn.connection._api_url, "instances/System::", systemId, 'action/removeConsistencyGroupSnapshots'), json=consistencyGroupIdDict)
        #except:
        #    raise RuntimeError("delete_snapshot() - Error communicating wit ScaleIO gateway")
        return response
    
    def get_snapshots_by_vol(self, volObj):
        all_snapshots_for_vol = []
        for volume in self.get_volumes_for_vtree(self.get_vtree_by_id(volObj.vtree_id)):
            if volume.ancestor_volume is not None:
                 all_snapshots_for_vol.append(volume)
        return all_snapshots_for_vol

    def get_vtree_by_id(self,id):
        for vtree in self.vtrees:
            if vtree.id == id:
                return vtree
        raise KeyError("VTree with ID " + id + " not found")

    def get_vtree_by_name(self,name):
        for vtree in self.vtrees:
            if vtree.name == name:
                return vtree
        raise KeyError("VTree with NAME " + name + " not found")
    
    """
    def get_snapshot_group_id_by_vol_name(self, volname):
        pass
    
    def get_snapshot_group_id_by_vol_id(self, volid):
        pass
    """

    def get_sdc_for_volume(self, volObj):
        """
        Get list of SDC mapped to a specific volume
        :param volObj: ScaleIO volume object
        :return: List of ScaleIO SDC objects (empty list if no mapping exist)
        :rtype: SDC object
        """
        sdcList = []
        if volObj.mapped_sdcs is not None:
            for sdc in volObj.mapped_sdcs:
                sdcList.append(sdc)
        if len(sdcList) == 0:
            self.conn.logger.debug("No SDCs mapped to volume: %s-(%s)" % (volObj.name, volObj.id))
            return []
        # returning an empty list is
        # valid for snapshots or volumes.
        return sdcList
