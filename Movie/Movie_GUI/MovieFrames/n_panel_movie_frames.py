import re

from ATvis.Common_Data_Plot import AT_Single_FigureGeometry, AT_Double_FigureGeometry

from Movie             import *
from movie_frames__gui import *


class Single_Panel_Movie_Frames(MovieFrames__GUI):
    """
    Setup figure and axes for SINGLE panel plots
    in other opertions it relies on MovieFrames__GUI
    """

    def __init__(self, seq_plotter, ylim, xlim=None, axes_commands=None, fig_param=None):
        # initialize base class ======
        # seq_plotter must be a sequence
        MovieFrames__GUI.__init__(self, (seq_plotter,) )
        # setup graphic elements =====
        mfs = AT_Single_FigureGeometry(fig_param)
        # xlim, ylim must be sequences
        self._setup_figure_and_axes(mfs, [xlim],[ylim], [axes_commands])
        # set plot_idlabel -----------------------
        self.plot_idlabel = seq_plotter.plot_idlabel



class Double_Panel_Movie_Frames(MovieFrames__GUI):
    """
    Setup figure and axes for DOUBLE panel plots
    in other opertions it relies on MovieFrames__GUI
    """

    def __init__(self, seq_plotters, ylims, xlims=None, axes_commands=None, fig_param=None):
        """
        All arguments must be sequences of the same length!
        -----------
        seq_plotter
        ylim       
        xlim       
        """
        # initialize base class ======
        MovieFrames__GUI.__init__(self, seq_plotters )
        # setup graphic elements =====
        mfs = AT_Double_FigureGeometry(fig_param)
        # xlim, ylim must be sequences
        if not xlims:
            xlims = [None,None]
        if not axes_commands:
            axes_commands = [None,None]
        self._setup_figure_and_axes(mfs, xlims,ylims, axes_commands)
        # set plot_idlabel -----------------------
        self.plot_idlabel = '%s + %s' % (re.split(':',seq_plotters[0].plot_idlabel)[0], seq_plotters[1].plot_idlabel)
