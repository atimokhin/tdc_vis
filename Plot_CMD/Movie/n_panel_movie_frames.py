from Movie import *
from movie_frames__cmd import *

class Single_Panel_Movie_Frames(MovieFrames__CMD):
    """
    Setup figure and axes for single panel plots
    in other opartions relies on MovieFrames__GUI
    """

    def __init__(self, seq_plotter, ylim, xlim=None):
        # initialize base class ======
        # seq_plotter must be a sequence
        MovieFrames__CMD.__init__(self, (seq_plotter,) )
        # setup graphic elements =====
        mfs = Single_Panel_Movie_Frames_Sizes()
        # xlim, ylim must be sequences
        self.setup_figure_and_axes(mfs, [xlim],[ylim])



class Double_Panel_Movie_Frames(MovieFrames__CMD):
    """
    Setup figure and axes for single panel plots
    in other opartions relies on MovieFrames__GUI
    """

    def __init__(self, seq_plotter, ylim, xlim=None, **kwargs):
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
        mfs = Double_Panel_Movie_Frames_Sizes()
        # xlim, ylim must be sequences
        self.setup_figure_and_axes(mfs, xlim,ylim)
        # set plot_idlabel -----------------------
        self.plot_idlabel = seq_plotter[0].plot_idlabel
