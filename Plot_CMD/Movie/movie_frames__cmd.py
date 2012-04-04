from Auxiliary        import *
from Common_Data_Plot import *
from Movie            import *

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

    def setup_figure_and_axes(self, mfs, xlim, ylim, axes_commands):
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
        # set MFS
        self.set_movie_frames_sizes(mfs)
        # plot window ----------------------------
        self.figure = matplotlib.pyplot.figure(facecolor='white',
                                               figsize=self.MFS.figsize_inch,
                                               dpi=self.MFS.dpi)
        # axes -----------------------------------
        # add as many axes as there are entries in mfs.axes_boxes
        for box in self.MFS.axes_boxes:
            self.ax.append( self.figure.add_axes(box) )        
        # setup axes limits
        self.setup_axes(xlim, ylim, axes_commands) 


    def plot(self,**kwargs):
        """
        Plots movie frame:
        (is called each time a new plot is needed)
        - calls MovieFrames.plot
        - plots time label
        - sets 
        """
        # set axes limits and formatter (again)
        for A,F,xl,yl in zip(self.ax,self.formatter,self.xlim,self.ylim):
            A.yaxis.set_major_formatter(F)
            A.set_xlim(xl)
            A.set_ylim(yl)
        # force to call axes commands
        self.set_axes_commands_executed_flag(False)
        # main plot
        MovieFrames.plot(self,**kwargs)
        # plot time label on top of the plot
        self.p_time_label=[]
        for P,A in zip(self.seq_plotter,self.ax):
            self.p_time_label.append( A.text(0.02, 0.925,
                                             't=%.3f' % P.get_time(),
                                             transform = A.transAxes,
                                             fontsize=self.MFS.ticklabel_fontsize) )

    def animation_update(self,i_frame,**kwargs):
        """
        - reads data for i_frame's frame
        - clear axes
        - calls self.plot
        """
        for P,A in zip(self.seq_plotter,self.ax):
            P.read(i_frame)
            A.cla()
        self.plot(**kwargs)

