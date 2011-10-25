import gtk, gobject

from Auxiliary        import *
from Common_Data_Plot import *
from Movie            import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas


class MovieFrames__GUI(MovieFrames):
    """
    Base class for GUI version of Movie Frames
    ---> needs matplotlib.backends.backend_gtkagg!
         do not clear axes each time for the next animation frame
    -------------
    Contains:
    -------------
    self.redraw_flag -- nedeed by MovieEngine
    """

    def __init__(self, seq_plotter):
        # initialize base class ======
        MovieFrames.__init__(self, seq_plotter)
        # set redraw_flag 
        self.redraw_flag=False

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
        # set MFS
        self.set_movie_frames_sizes(mfs)
        # plot window ----------------------------
        self.figure = Figure(facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.set_size_request( *self.MFS.figsize_points )
        # axes -----------------------------------
        # add as many axes as there are entries in mfs.axes_boxes
        for box in self.MFS.axes_boxes:
            self.ax.append( self.figure.add_axes(box) )
        # setup axes limits
        self.setup_axes(xlim, ylim) 
        # setup timelabel artists
        self.setup_timelabels() 

    def setup_axes(self,xlim,ylim):
        """
        - calls MovieFrames.setup_axes(self,xlim,ylim)
        - sets callback function for setting redraw_flag if axes limits change
        """
        MovieFrames.setup_axes(self,xlim,ylim)
        # set redraw_flag if axes limits change
        for i,A in enumerate(self.ax):
            A.callbacks.connect('ylim_changed', self.axes_lims_changed_callback)
            A.callbacks.connect('xlim_changed', self.axes_lims_changed_callback)

    def setup_timelabels(self):
        """
        initialize an empty timelabel artist 
        """
        # time label artist 
        self.p_time_label = [ A.text(0.02, 0.925, None,
                                     transform = A.transAxes,
                                     animated=True)
                              for A in self.ax ]

    def axes_lims_changed_callback(self,ax):
        self.redraw_flag=True
        
    def plot(self,**kwargs):
        """
        Makes initial plot and set text for the timelabel
        """
        MovieFrames.plot(self,**kwargs)
        # time label
        for P,T in zip(self.seq_plotter,self.p_time_label):
            T.set_text( 't=%.3f' % P.get_time() )

    def replot(self,**kwargs):
        """
        - Clears axes
        - plots
        - restores axes settings
        """
        xlim=[]
        ylim=[]
        # store current axes limits
        for A in self.ax:
            xlim.append( A.get_xlim() )
            ylim.append( A.get_ylim() )
        # do plot
        self.plot(animated=True,**kwargs)
        # restore axes limits
        for A,xl,yl in zip(self.ax,xlim,ylim):
            A.set_xlim( xl )
            A.set_ylim( yl )
        
    def animation_update(self,i_frame):
        """
        Updates plot and timelabel
        """
        for P,A,T in zip(self.seq_plotter,self.ax,self.p_time_label):
            P.animation_update( A, i_frame )
            T.set_text( 't=%.3f' % P.get_time() )
            A.draw_artist(T)

    def set_animated(self,val):
        """
        changes *animated* attribute for all changing entries
        """
        for P,T in zip(self.seq_plotter,self.p_time_label):
            P.set_animated(val)
            T.set_animated(val)

    def axes_setup_panel(self, parent_widget):
        """
        Pops up parameter window and passes control to it
        """
        from Plot_GUI.GUI.axes_setup import Axes_Setup_Window
        self.axes_setup_window=Axes_Setup_Window(self,
                                                 self.seq_plotter,
                                                 self.ax,
                                                 parent_widget)



