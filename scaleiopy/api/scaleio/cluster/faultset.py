# Standard lib imports
# None

# Third party imports
# None

# Project level imports
# None


class FaultSet(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection        

    @property
    def get(self):
        """
        Returns a `list` of all the `System` objects to the cluster.  Updates every time - no caching.
        :return: a `list` of all the `System` objects known to the cluster.
        :rtype: list
        """
        self.conn.connection._check_login()
        response = self.conn.connection._do_get("{}/{}".format(self.conn.connection._api_url, "types/System/instances")).json()
        all_system_objects = []
        for system_object in response:
            all_system_objects.append(self.conn.System.from_dict(system_object))
        return all_system_objects
    
    def get_faultset_by_id(self, id):
        for fs in self.conn.fault_sets:
            if fs.id == id:
                return fs
        raise KeyError("FaultSet with ID " + id + " not found")

    def get_faultset_by_name(self,name):
        for fs in self.conn.fault_sets:
            if fs.name == name:
                return fs
        raise KeyError("FaultSet with NAME " + name + " not found")
    
    def set_faultset_name(self, name, fsObj):
        """
        Set name for Faultset
        :param name: Name of Faultset
        :param fsObj: ScaleIO FS object
        :return: POST request response
        :rtype: Requests POST response object
        """
        # Set name of FaultSet
        self.conn.connection._check_login()
        faultSetNameDict = {'Name': name}
        # This one is the most logical name comparing to other methods.
        response = self.conn.connection._do_post("{}/{}{}/{}".format(self.conn.connection._api_url, "types/FaultSet::", fsObj.id, 'instances/action/setFaultSetName'), json=faultSetNameSdcDict)    

        # This is how its documented in REST API Chapter
        #response = self._do_post("{}/{}{}/{}".format(self._api_url, "types/FaultSet::", fsObj.id, 'instances/action/setFaultSetName'), json=faultsetNameSdcDict)    
        return response 