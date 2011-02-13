from Common   import *
from Movie    import *

import matplotlib

class MovieFrames__CMD(MovieFrames):
    """
    Base class for CMD version of Movie Frames
    ---> clears axes each time for the next animation frame!
    -------------
    Defines
    plot()
    animation_update()
    """

    def __init__(self, seq_plotter):
        # initialize base class ======
        MovieFrames.__init__(self, seq_plotter)

    def setup_figure_and_axes(self, mfs, xlim, ylim):
        """
        Creates figure and axes accordinng to sized in class mds
        -------
        Params:
        -------
        mfs
          MovieFrames_Sizes class instance, contains figure sizes and axes boxes
        xlim
        ylim
          axes limits
        """
        # get dpi and calculate figure size in inches 
        dpi = matplotlib.rcParams['figure.dpi']
        figsize_inch = [ x/dpi for x in  mfs.figsize_points ]
        # plot window ----------------------------
        self.figure = matplotlib.pyplot.figure(facecolor='white', figsize=figsize_inch)
        # axes -----------------------------------
        # add as many axes as there are entries in mfs.axes_boxes
        for box in mfs.axes_boxes:
            self.ax.append( self.figure.add_axes(box) )        
        # setup axes limits
        self.setup_axes(xlim, ylim) 


    def plot(self,**kwargs):
        """
        Plots movie frame:
        (is called each time a new plot is needed)
        - calls MovieFrames.plot
        - plots time label
        - sets 
        """
        MovieFrames.plot(self,**kwargs)
        self.p_time_label=[]
        # main plot
        for P,A,F in zip(self.seq_plotter,self.ax,self.formatter):
            A.yaxis.set_major_formatter(F)
            self.p_time_label.append( A.text(0.02, 0.925,
                                             't=%.3f' % P.get_time(),
                                             transform = A.transAxes) )

    def animation_update(self,i_frame):
        """
        - reads data for i_frame's frame
        - clear axes
        - calls self.plot
        """
        for P,A in zip(self.seq_plotter,self.ax):
            P.read(i_frame)
            A.cla()
        self.plot()

