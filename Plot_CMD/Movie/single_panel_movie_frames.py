from movie_frames__cmd import *

class Single_Panel_Movie_Frames(MovieFrames__CMD):
    """
    Setup figure and axes for single panel plots
    in other opartions relies on MovieFrames__GUI
    """

    def __init__(self, seq_plotter, ylim, xlim=None, **kwargs):
        # makes sequences from scalar parameters
        xlim=[xlim]
        ylim=[ylim]
        seq_plotter = (seq_plotter,)
        # initialize base class ======
        MovieFrames__CMD.__init__(self, seq_plotter)
        # plot window ----------------------------
        self.figure = plt.figure(facecolor='white', figsize=(7.05,4.8))
        # axes -----------------------------------
        self.ax.append( self.figure.add_axes([0.1135,.125,.8582,.8125]) )        
        self.setup_axes(xlim, ylim) 


