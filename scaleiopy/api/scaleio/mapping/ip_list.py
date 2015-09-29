# Imports

class SIO_IP_List(object):
    def __init__(self, ip, role):
        self.ip = ip
        self.role = role

    def __str__(self):
        """
        A convenience method to pretty print the contents of the class instance
        """
        # to show include all variables in sorted order
        return "{} : IP: {} Role: {}".format("IP",self.ip,self.role)

    def __repr__(self):
        return self.__str__()
