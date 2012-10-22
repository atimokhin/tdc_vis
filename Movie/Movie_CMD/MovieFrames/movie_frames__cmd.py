from Auxiliary        import *
from Common_Data_Plot import *
from Movie            import *

import matplotlib

class MovieFrames__CMD(MovieFrames__Axes):
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
        MovieFrames__Axes.__init__(self, seq_plotter)

    def _setup_figure_and_axes(self, mfs, xlim, ylim, axes_commands):
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
        self.MFS = mfs
        # plot window ----------------------------
        self.figure = matplotlib.pyplot.figure(facecolor='white',
                                               figsize=self.MFS.figsize_inch,
                                               dpi=self.MFS.dpi)
        # axes -----------------------------------
        # add as many axes as there are entries in mfs.axes_boxes
        self.ax = [ self.figure.add_axes(box)  for box in self.MFS.axes_boxes ]       
        # setup axes limits
        self._setup_axes(xlim, ylim, axes_commands) 

    def _plot_axes_labels(self):
        for i,P in enumerate(self.seq_plotter):
            coord_x = self.MFS.xlabel_pos(i)
            self.figure.text( *coord_x, 
                              s=P.plot_xlabel,
                              va='bottom',ha='center',
                              size=self.MFS.label_fontsize)
            coord_y = self.MFS.ylabel_pos(i)
            self.figure.text( *coord_y, 
                              s=P.plot_ylabel,
                              va='center',ha='left',
                              size=self.MFS.label_fontsize)

    def _plot_time_labels(self):
        for P,A in zip(self.seq_plotter,self.ax):
             A.text(0.02, 0.925,
                    't=%.3f' % self.get_time(),
                    transform = A.transAxes,
                    fontsize = self.MFS.ticklabel_fontsize )
        

    def plot(self,**kwargs):
        """
        Plots movie frame:
        (is called each time a new plot is needed)
        - calls MovieFrames.plot
        - plots time label
        - sets 
        """
        # set axes limits and formatter (again)
        self._setup_axes_from_stored_values()
        # main plot
        MovieFrames__Axes.plot(self,**kwargs)
        # plot axes labels and execute axes commands
        self._plot_axes_labels()
        self._execute_axes_commands()
        # plot time label on top of the plot
        self._plot_time_labels()

    def animation_update(self,i_frame,**kwargs):
        """
        - reads data for i_frame's frame
        - clear figure
        - setup axes anew
        - calls self.plot
        """
        for P,A in zip(self.seq_plotter,self.ax):
            P.read(i_frame)
        # clear figure
        self.figure.clf()
        # add as many axes as there are entries in mfs.axes_boxes
        self.ax = [ self.figure.add_axes(box)  for box in self.MFS.axes_boxes ]       
        # make plot
        self.plot(**kwargs)

