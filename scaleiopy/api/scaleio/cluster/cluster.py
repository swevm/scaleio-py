# Standard lib imports
# None

# Third party imports
# None

# Project level imports
from scaleiopy.api.scaleio.system import SIO_System
# None


class Cluster(object):

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
            all_system_objects.append(SIO_System.from_dict(system_object))
        return all_system_objects
    