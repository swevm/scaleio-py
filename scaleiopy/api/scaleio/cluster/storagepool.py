# Standard lib imports
# None

# Third party imports
# None

# Project level imports
# None


class StoragePool(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection        

    @property
    def get(self):
        pass

    def get_storage_pool_by_name(self, name):
        """
        Get ScaleIO StoragePool object by its name
        :param name: Name of StoragePool
        :return: ScaleIO StoragePool object
        :raise KeyError: No StoragePool with specified name found
        :rtype: StoragePool object
        """
        for storage_pool in self.conn.storage_pools:
            if storage_pool.name == name:
                return storage_pool
        raise KeyError("Storage pool of that name not found")

    def get_storage_pool_by_id(self, id):
        """
        Get ScaleIO SDS ofbject by its id
        :param name: Name of StoragePool
        :return: ScaleIO StoraegPool object
        :raise KeyError: No StoragePool with specified id found
        :rtype: StoragePool object
        """
        for storage_pool in self.conn.storage_pools:
            if storage_pool.id == id:
                return storage_pool
        raise KeyError("Storage Pool with that ID not found")