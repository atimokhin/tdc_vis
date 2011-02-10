from movie_frames__gui import *

class Double_Panel_Movie_Frames(MovieFrames__GUI):
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
        MovieFrames__GUI.__init__(self, seq_plotter)
        # set plot_idlabel -----------------------
        self.plot_idlabel = seq_plotter[0].plot_idlabel
        # setup graphic elements =====
        # plot window ----------------------------
        self.figure = Figure(facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.set_size_request(1100,500)
        # axes -----------------------------------
        self.ax.append( self.figure.add_axes([0.08,.1,.4,.85]) )        
        self.ax.append( self.figure.add_axes([0.58,.1,.4,.85]) )        
        self.setup_axes(xlim, ylim) 
        self.setup_timelabels() 