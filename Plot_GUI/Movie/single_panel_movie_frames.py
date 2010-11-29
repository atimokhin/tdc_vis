from Common   import *
from Movie    import *

# LaTeX rendering would be very slow!
import matplotlib
matplotlib.rcParams['text.usetex'] = False

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas


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
        self.figure = Figure(facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.set_size_request(705,480)
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
        #
        # time label artist ----------
        self.p_time_label = self.ax.text(0.02, 0.925, None,
                                         transform = self.ax.transAxes,
                                         animated=True)
        # ----------------------------------------        
        # axes limits ----------------------------
        # xlim -- if not set use the whole x range 
        if xlim==None:
            xlim=[ self.seq_plotter.xmin, self.seq_plotter.xmax ]
        self.xlim=xlim
        self.ylim=ylim
        self.ax.set_xlim(self.xlim)
        self.ax.set_ylim(self.ylim)
        # ----------------------------------------
        # Axes change attrributes
        self.axes_lims_changed_flag=False
        self.ax.callbacks.connect('ylim_changed', self.axes_lims_changed_callback)
        self.ax.callbacks.connect('xlim_changed', self.axes_lims_changed_callback)
        # ----------------------------------------


    def axes_lims_changed_callback(self,ax):
        self.axes_lims_changed_flag=True


    def get_xlims(self):
        return self.ax.get_xlim()

    def get_ylims(self):
        return self.ax.get_ylim()


    def plot(self,**kwargs):
        "Makes initial plot"
        # main plot
        self.seq_plotter.plot(self.ax,**kwargs)
        self.ax.set_xlim(self.xlim)
        self.ax.set_ylim(self.ylim)
        # time label
        self.p_time_label.set_text( 't=%.3f' % self.seq_plotter.get_time() )
        # set axes labels
        self.ax.set_ylabel(self.seq_plotter.plot_ylabel,size='x-large')
        self.ax.set_xlabel(self.seq_plotter.plot_xlabel,size='x-large')
        

    def replot(self,**kwargs):
        "Clears axes, plots, and restores axes settings"
        # store current axes limits
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        # do plot
        self.plot(animated=True)
        # restore axes limits
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)

        
    def animation_update(self,i_frame):
        "Plot Field into axes ax"
        self.seq_plotter.animation_update( self.ax, i_frame )
        self.p_time_label.set_text( 't=%.3f' % self.seq_plotter.get_time() )
        self.ax.draw_artist(self.p_time_label)


    def set_animated(self,val):
        "changes *animated* attribute for all changing entries"
        self.seq_plotter.set_animated(val)
        self.p_time_label.set_animated(val)
