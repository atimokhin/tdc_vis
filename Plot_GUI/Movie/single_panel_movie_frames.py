from movie_frames__gui import *

class Single_Panel_Movie_Frames(MovieFrames__GUI):
    """
    Setup figure and axes for single panel plots
    in other opartions relies on MovieFrames__GUI
    """

    def __init__(self, seq_plotter, ylim, xlim=None):
        # makes sequences from scalar parameters
        xlim=[xlim]
        ylim=[ylim]
        seq_plotter = (seq_plotter,)
        # initialize base class ======
        MovieFrames__GUI.__init__(self, seq_plotter)
        # set plot_idlabel -----------------------
        self.plot_idlabel = seq_plotter[0].plot_idlabel
        # setup graphic elements =====
        # plot window ----------------------------
        self.figure = Figure(facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.set_size_request(705,480)
        # axes -----------------------------------
        self.ax.append( self.figure.add_axes([0.1135,.125,.8582,.8125]) )        
        self.setup_axes(xlim, ylim) 
        self.setup_timelabels() 
