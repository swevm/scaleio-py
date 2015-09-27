# Imports


class Link(object):
    def __init__(self, href, rel):
        self.href = href
        self.rel = rel

    def __str__(self):
        """
        A convenience method to pretty print the contents of the class instance
        """
        # to show include all variables in sorted order
        return "{} : Target: '{}' Relative: '{}'".format("Link", self.href, self.rel)

    def __repr__(self):
        return self.__str__()


