import os
import optparse

class Movie_Interface_Selector(object):
    """
    Selects interface: either CMD or GUI

    Uses command line options and environment variables
    """
    def __init__(self):
        """
        """
        # parse command line
        p = optparse.OptionParser()
        p.add_option("--cmd",action="store_true",dest="interface_cmd")
        p.set_defaults(interface_cmd=False)
        opts, args = p.parse_args()
        # use environment variable to make the final decision what module to import
        interface_cmd = os.environ.get('MPL_INTERFACE')=='GUI' or opts.interface_cmd
        # import module
        if interface_cmd:
            from .. import Movie_CMD as movie_module
        else:
            from .. import Movie_GUI as movie_module
        self.__movie_module = movie_module

    @property
    def movie_module(self):
        return self.__movie_module
