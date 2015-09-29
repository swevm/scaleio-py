# Standard lib imports
# None

# Third party imports
# None

# Project level imports
# None


class Sdc(object):

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
    
    def set_sdc_name(self, name, sdcObj):
        """
        Set name for SDC
        :param name: Name of SDC
        :param sdcObj: ScaleIO SDC object
        :return: POST request response
        :rtype: Requests POST response object
        """
        # TODO:
        # Check if object parameters are the correct ones, otherwise throw error
        self.conn.connection._check_login()
        sdcNameDict = {'sdcName': name}
        response = self.conn.connection._do_post("{}/{}{}/{}".format(self.conn.connection._api_url, "instances/Sdc::", sdcObj.id, 'action/setSdcName'), json=sdcNameDict)    
        return response
    

    def get_sdc_by_name(self, name):
        """
        Get ScaleIO SDC object by its name
        :param name: Name of SDC
        :return: ScaleIO SDC object
        :raise KeyError: No SDC with specified name found
        :rtype: SDC object
        """
        for sdc in self.sdc:
            if sdc.name == name:
                return sdc
        raise KeyError("SDC of that name not found")

    def get_sdc_by_id(self, id):
        """
        Get ScaleIO SDC object by its id
        :param name: id of SDC
        :return: ScaleIO SDC object
        :raise KeyError: No SDC with specified id found
        :rtype: SDC object
        """
        for sdc in self.sdc:
            if sdc.id == id:
                return sdc
        raise KeyError("SDC with that ID not found")

    def get_sdc_by_guid(self, guid):
        """
        Get ScaleIO SDC object by its id
        :param name: guid of SDC
        :return: ScaleIO SDC object
        :raise KeyError: No SDC with specified id found
        :rtype: SDC object
        """
        for sdc in self.sdc:
            if sdc.guid == guid:
                return sdc
        raise KeyError("SDC with that GUID not found")

    def get_sdc_by_ip(self, ip):
        """
        Get ScaleIO SDC object by its ip
        :param name: IP address of SDC
        :return: ScaleIO SDC object
        :raise KeyError: No SDC with specified IP found
        :rtype: SDC object
        """
        if self.conn.is_ip_addr(ip):
            for sdc in self.sdc:
                if sdc.sdcIp == ip:
                    return sdc
            raise KeyError("SDS of that name not found")
        else:
            raise ValueError("Malformed IP address - get_sdc_by_ip()")
        
    def unregisterSdc(self, sdcObj):
        """
        Unregister SDC from MDM/SIO Cluster
        :param sdcObj: ScaleIO SDC object
        :return: POST request response
        :rtype: Requests POST response object
        """
        # TODO:
        # Add code that unmap volume if mapped
        self.conn.connection._check_login()
        response = self.conn.connection._do_post("{}/{}{}/{}".format(self.conn.connection._api_url, "instances/Sdc::", sdcObj.id, 'action/removeSdc'))    
        return response

    def registerSdc(self, sdcObj, **kwargs):
        # Register existing SDS running SDS binary (need to be installed manually but not added to MDM)
        # 
        self.conn.connection._check_login()    

        response = self.conn.connection._do_post("{}/{}".format(self.conn.connection._api_url, "types/Sdc/instances"), json=sdcObj.__to_dict__())
        return response
    
    
    