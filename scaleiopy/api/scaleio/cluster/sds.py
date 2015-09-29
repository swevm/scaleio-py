# Standard lib imports
# None

# Third party imports
# None

# Project level imports
# None
from scaleiopy.api.scaleio.mapping.sds import SIO_SDS

class Sds(object):

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

    def set_sds_name(self, name, sdsObj):
        """
        Set name for SDS
        :param name: Name of SDS
        :param sdsObj: ScaleIO SDS object
        :return: POST request response
        :rtype: Requests POST response object
        """
        # TODO:
        # Check if object parameters are the correct type, otherwise throw error
        # UNSURE IF THIS IS CORRECT WAY TO SET SDS NAME
        self.conn.connection._check_login()
        sdsNameDict = {'sdsName': name}
        response = self.conn.connection._do_post("{}/{}{}/{}".format(self.conn.connection._api_url, "instances/Sds::", sdcObj.id, 'action/setSdsName'), json=sdsNameDict)    
        return response


    def unregisterSds(self, sdsObj):
        """
        Unregister SDS from MDM/SIO Cluster
        :param sdsObj: ScaleIO SDS objecty
        :return: POST request response
        :rtype: Requests POST response object
        """
        self.conn.connection._check_login()
        response = self.conn.connection._do_post("{}/{}{}/{}".format(self.conn.connection._api_url, "instances/Sds::", sdsObj.id, 'action/removeSds'))    
        return response    
    
    # /api/types/Sds/instance s
    def registerSds(self, sdsObj, **kwargs):
        """
        Register SDS with MDM/SIO Cluster
        :param sdsObj: ScaleIO SDS object
        :return: POST request response
        :rtype: Requests POST response object
        """
        # Register existing SDS running SDS binary (need to be installed manually but not added to MDM)
        # 
        self.conn.connection._check_login()    

        response = self.conn.connection._do_post("{}/{}".format(self.conn.connection._api_url, "types/Sds/instances"), json=sdsObj.__to_dict__())
        return response
    
    def get_sds_in_faultset(self, faultSetObj):
        """
        Get list of SDS objects attached to a specific ScaleIO Faultset
        :param faultSetObj: ScaleIO Faultset object
        :rtype: list of SDS in specified Faultset
        """
        self.conn.connection._check_login()
        response = self.conn.connection._do_get("{}/{}{}/{}".format(self.conn.connection._api_url, 'types/FaultSet::', faultSetObj.id, 'relationships/Sds')).json()
        all_sds = []
        for sds in response:
            all_sds.append(
                SIO_SDS.from_dict(sds)
            )
        return all_sds
    
    def get_sds_by_name(self,name):
        """
        Get ScaleIO SDS object by its name
        :param name: Name of SDS
        :return: ScaleIO SDS object
        :raise KeyError: No SDS with specified name found
        :rtype: SDS object
        """
        for sds in self.sds:
            if sds.name == name:
                return sds
        raise KeyError("SDS of that name not found")
    
    def get_sds_by_ip(self,ip):
        """
        Get ScaleIO SDS object by its ip address
        :param name: IP address of SDS
        :return: ScaleIO SDS object
        :raise KeyError: No SDS with specified ip found
        :rtype: SDS object
        """
        if self.conn.is_ip_addr(ip):
            for sds in self.sds:
                for sdsIp in sds.ipList:
                    if sdsIp == ip:
                        return sds
            raise KeyError("SDS of that name not found")
        else:
            raise ValueError("Malformed IP address - get_sds_by_ip()")
        
    def get_sds_by_id(self,id):
        """
        Get ScaleIO SDS object by its id
        :param name: ID of SDS
        :return: ScaleIO SDS object
        :raise KeyError: No SDS with specified id found
        :rtype: SDS object
        """
        for sds in self.sds:
            if sds.id == id:
                return sds
        raise KeyError("SDS with that ID not found")