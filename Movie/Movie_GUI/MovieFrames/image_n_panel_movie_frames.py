from ImageFiles              import Image_Single_FigureGeometry
from Movie                   import *

from image_movie_frames__gui import *


class Image_Single_Panel_Movie_Frames(Image_MovieFrames__GUI):
    """
    Setup figure and axes for SINGLE panel plots with image
    in other operations it relies on Image_MovieFrames__GUI
    """
    def __init__(self, seq_plotter):
        # initialize base class ======
        # seq_plotter must be a sequence
        Image_MovieFrames__GUI.__init__(self, (seq_plotter,) )
        # setup graphic elements =====
        mfs = Image_Single_FigureGeometry(seq_plotter)
        # xlim, ylim must be sequences
        self._setup_figure_and_axes(mfs)
        # set plot_idlabel -----------------------
        self.plot_idlabel = seq_plotter.plot_idlabel



# class Image_Double_Panel_Movie_Frames(Image_MovieFrames__GUI):
#     """
#     Setup figure and axes for DOUBLE panel plots
#     in other opertions it relies on MovieFrames__GUI
#     """

#     def __init__(self, seq_plotter):
#         """
#         All arguments must be sequences of the same length!
#         -----------
#         seq_plotter
#         ylim       
#         xlim       
#         """
#         # initialize base class ======
#         MovieFrames__GUI.__init__(self, seq_plotter )
#         # setup graphic elements =====
#         mfs = Image_Double_FigureGeometry(fig_param)
#         self._setup_figure_and_axes(mfs)
#         # set plot_idlabel -----------------------
#         self.plot_idlabel = seq_plotter[0].plot_idlabel
