class ForceIndentation(object):
    """
    For plotting Force vs. Indentation
    """
    def __init__(self,):
        """
        Initialization goes here.
        """
        print "Force-Indentation Class created."

    def print_class(self):
        """
        Print whole class.
        """
        keys = dir(self)
        for key in keys:
            print key,':\t',getattr(self,key)

    def next_class(self):
        """
        Establish properties.
        """
        print "Hello World!!!!"
