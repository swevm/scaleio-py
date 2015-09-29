# Standard lib imports
# None

# Third party imports
# None

# Project level imports
# None


class ProtectionDomain(object):

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

    def get_pd_by_name(self, name):
        """
        Get ScaleIO ProtectionDomain object by its name
        :param name: Name of ProtectionDomain
        :return: ScaleIO ProtectionDomain object
        :raise KeyError: No ProtetionDomain with specified name found
        :rtype: ProtectionDomain object
        """
        for pd in self.conn.protection_domains:
            if pd.name == name:
                return pd
        raise KeyError("Protection Domain NAME " + name + " not found")

    def get_pd_by_id(self, id):
        """
        Get ScaleIO ProtectionDomain object by its id
        :param name: ID of ProtectionDomain
        :return: ScaleIO ProctectionDomain object
        :raise KeyError: No ProtectionDomain with specified name found
        :rtype: ProtectionDomain object
        """
        for pd in self.conn.protection_domains:
            if pd.id == id:
                return pd
        raise KeyError("Protection Domain with ID " + id + " not found")
    
    def create_protection_domain(self, pdObj, **kwargs):
        # TODO:
        # Check if object parameters are the correct ones
        self.conn.connection._check_login()    
        response = self.conn.connection._do_post("{}/{}".format(self.conn.connection._api_url, "types/Volume/instances"), json=pdObj.__to_dict__()())
        return response
    
    def delete_potection_domain(self, pdObj):
        """
        :param pdObj: ID of ProtectionDomain
        
        type: POST
        Required:
            Protection Domain Object
        Return:
        """
        self.conn.connection._check_login()
        response = self.conn.connection._do_post("{}/{}{}/{}".format(self.conn.connection._api_url, "instances/ProtectionDomain::", pdObj.id, 'action/removeProtectionDomain'))
        return response