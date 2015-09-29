# Standard lib imports
#import logging

# Third party imports
# None

# Project level imports
# None

#log = logging.getLogger(__name__)

class Statistics(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get(self):
        self.conn.connection._check_login()
        response = self.conn.connection._do_get("{}/{}{}/{}".format(self.conn.connection._api_url, "instances/System::", str(self.conn.get_system_id()), "relationships/Statistics")).json()
        return response
