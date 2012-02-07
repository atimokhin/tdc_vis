from Common_Data_Plot  import tdc_Single_FigureGeometry

from Movie import *
from movie_frames__cmd import *

class Single_Panel_Movie_Frames(MovieFrames__CMD):
    """
    Setup figure and axes for single panel plots
    in other opartions relies on MovieFrames__GUI
    """

    def __init__(self, seq_plotter, ylim, xlim=None, axes_commands=None):
        # initialize base class ======
        # seq_plotter must be a sequence
        MovieFrames__CMD.__init__(self, (seq_plotter,) )
        # setup graphic elements =====
        mfs = tdc_Single_FigureGeometry()
        # xlim, ylim must be sequences
        self.setup_figure_and_axes(mfs, [xlim],[ylim], [axes_commands])



class Double_Panel_Movie_Frames(MovieFrames__CMD):
    """
    Setup figure and axes for single panel plots
    in other opartions relies on MovieFrames__GUI
    """

    def __init__(self, seq_plotter, ylim, xlim=None, axes_commands=None, **kwargs):
        """
        All arguments must be sequences of the same length!
        -----------
        seq_plotter
        ylim       
        xlim       
        """
        # initialize base class ======
        MovieFrames__CMD.__init__(self, seq_plotter )
        # setup graphic elements =====
        mfs = tdc_Double_FigureGeometry()
        # xlim, ylim must be sequences
        if not xlim:
            xlim = [None,None]
        if not axes_commands:
            axes_commands = [None,None]
        self.setup_figure_and_axes(mfs, xlim,ylim, axes_commands)
        # set plot_idlabel -----------------------
        self.plot_idlabel = seq_plotter[0].plot_idlabel
