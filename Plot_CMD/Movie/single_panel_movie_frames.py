#from movie_frames import MovieFrames

from Common   import *
from Movie    import *

# LaTeX rendering would be very slow!
import matplotlib
matplotlib.rcParams['text.usetex'] = False

import matplotlib.pyplot as plt


class Single_Panel_Movie_Frames(MovieFrames):
    """
    plot function(s) and time label

    seq_plotter must provide get_time() method!
    """

    def __init__(self, seq_plotter, ylim, xlim=None, **kwargs):
        """
        field_sequence -- Data Sequence with field
        ylim -- Y axis limits
        xlim -- <None> X axis limits
        """
        
        # plot window ----------------------------
        self.figure = plt.figure(facecolor='white', figsize=(6,5))
        # ----------------------------------------
        # ----------------------------------------
        # axes
        self.ax     = self.figure.add_axes([0.1135,.125,.8582,.8125])
        # axes formatter
        self.formatter=matplotlib.ticker.ScalarFormatter()
        self.formatter.set_powerlimits((-3, 4))
        self.ax.yaxis.set_major_formatter(self.formatter)
        # ----------------------------------------
        # ----------------------------------------
        # Animation elements: plotters and Artists
        # field plotter --------------
        self.seq_plotter = seq_plotter
        # initialize field plotter
        self.seq_plotter.read(1)
        # initialize base class ======
        MovieFrames.__init__(self, self.seq_plotter)

        # axes limits ----------------------------
        # xlim -- if not set use the whole x range 
        if xlim==None:
            xlim=[ self.seq_plotter.xmin, self.seq_plotter.xmax ]
        self.xlim=xlim
        self.ylim=ylim
        self.ax.set_xlim(self.xlim)
        self.ax.set_ylim(self.ylim)
        # ----------------------------------------

    def get_xlims(self):
        return self.ax.get_xlim()

    def get_ylims(self):
        return self.ax.get_ylim()


    def plot(self,**kwargs):
        "Makes initial plot"
        # main plot
        self.ax.set_xlim(self.xlim)
        self.ax.set_ylim(self.ylim)
        self.seq_plotter.plot(self.ax,**kwargs)
        # time label
        self.ax.text(0.02, 0.925,
                     't=%.3f' % self.seq_plotter.get_time(),
                     transform = self.ax.transAxes)
        # set axes labels
        self.ax.set_ylabel(self.seq_plotter.plot_ylabel,size='x-large')
        self.ax.set_xlabel(self.seq_plotter.plot_xlabel,size='x-large')
        

    def animation_update(self,i_frame):
        "Plot Field into axes ax"
        self.ax.cla()
        self.seq_plotter.read(i_frame)
        self.plot()

