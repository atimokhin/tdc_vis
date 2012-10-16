import os
import optparse

class tdc_Select_Interface(object):
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
            import Plot_CMD as plot_module
        else:
            import Plot_GUI as plot_module
        self.__plot_module = plot_module

    @property
    def plot_module(self):
        return self.__plot_module
