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
    self.main_Window  -- root window on teh player: needed by Axes_Setup_Window

    self.time_label
    self.xaxis_label -- all labels are updated, so keep them after initialization
    self.yaxis_label
    
    self.redraw_flag -- nedeed by MovieEngine
    """

    def __init__(self, seq_plotter):
        # initialize base class 
        MovieFrames.__init__(self, seq_plotter)
        # GUI specific members -------
        # main window
        self.main_Window = None
        # set redraw_flag 
        self.redraw_flag=False
        # label lists
        self.time_label=[]
        self.xaxis_label=[]
        self.yaxis_label=[]

    def _setup_figure_and_axes(self, mfs, xlim, ylim, axes_commands):
        """
        Creates figure and axes accordinng to sized in class mfs
        -------
        Params:
        -------
        mfs
          MovieFrames_Sizes class instance, contains figure sizes and axes boxes
        xlim
        ylim
          axes limits
        axes_commands
          commnads to be executed by axes
        """
        # set MFS
        self.MFS = mfs
        # plot window ----------------------------
        self.figure = Figure(facecolor='white',dpi=self.MFS.dpi)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.set_size_request( *self.MFS.figsize_points )
        # axes -----------------------------------
        # add as many axes as there are entries in mfs.axes_boxes
        for box in self.MFS.axes_boxes:
            self.ax.append( self.figure.add_axes(box) )
        # setup axes limits
        self._setup_axes(xlim, ylim, axes_commands) 
        # setup label artists
        self.__setup_axes_labels() 
        self.__setup_time_labels() 

    def _setup_axes(self,xlim,ylim, axes_commands):
        """
        - calls MovieFrames.setup_axes(self,xlim,ylim)
        - sets callback function for setting redraw_flag if axes limits change
        """
        MovieFrames._setup_axes(self,xlim,ylim, axes_commands)
        # set redraw_flag if axes limits change
        for i,A in enumerate(self.ax):
            A.callbacks.connect('ylim_changed', self.__axes_lims_changed_callback)
            A.callbacks.connect('xlim_changed', self.__axes_lims_changed_callback)

    def __axes_lims_changed_callback(self,ax):
        self.redraw_flag=True

    def __setup_time_labels(self):
        "initialize an empty timelabel artist"
        self.p_time_labels = [ A.text(0.02, 0.925, None,
                                      transform = A.transAxes,
                                      fontsize=self.MFS.ticklabel_fontsize,
                                      animated=True)  for A in self.ax ]

    def __setup_axes_labels(self):
        "initialize empty axeslabel artists"
        self.xaxis_labels = [ self.figure.text( *self.MFS.xlabel_pos(i),
                                                s=P.plot_xlabel,
                                                va='bottom',ha='center',
                                                size=self.MFS.label_fontsize ) \
                                                for i,P in enumerate(self.seq_plotter) ]
        self.yaxis_labels = [ self.figure.text( *self.MFS.ylabel_pos(i),
                                                s=P.plot_ylabel,
                                                va='center',ha='left',
                                                size=self.MFS.label_fontsize) \
                                                for i,P in enumerate(self.seq_plotter) ]


    def _plot_time_labels(self):
        for P,T in zip(self.seq_plotter,self.p_time_labels):
            T.set_text( 't=%.3f' % self.get_time() )

    def _plot_axes_labels(self):
        for P,Xlabel,Ylabel in zip(self.seq_plotter,self.xaxis_labels,self.yaxis_labels):
            Xlabel.set_text( P.plot_xlabel )
            Ylabel.set_text( P.plot_ylabel )
            
    def plot(self,**kwargs):
        """
        Makes initial plot and set text for the timelabel
        """
        MovieFrames.plot(self,**kwargs)
        self._plot_axes_labels()
        self._execute_axes_commands()
        # time label
        self._plot_time_labels()

    def replot(self,**kwargs):
        """
        - plotters' plot
        - put axes labels
        - executes axes commands
        time does not change, so no change in time label
        """
        # do plot
        MovieFrames.plot(self,animated=True,**kwargs)
        self._plot_axes_labels()
        self._execute_axes_commands()

    def animation_update(self,i_frame):
        """
        Updates plot and timelabel
        """
        for P,A,T in zip(self.seq_plotter,self.ax,self.p_time_labels):
            P.animation_update( A, i_frame )
            T.set_text( 't=%.3f' % self.get_time() )
            A.draw_artist(T)

    def set_animated(self,val):
        """
        changes *animated* attribute for all changing entries
        """
        for P,T in zip(self.seq_plotter,self.p_time_labels):
            P.set_animated(val)
            T.set_animated(val)

            
    def set_main_window(self,window):
        "Sets the main window for matplotlib widget"
        self.main_Window=window

    def axes_setup_panel(self, parent_widget):
        """
        Pops up parameter window and passes control to it
        """
        from Plot_GUI.GUI.axes_setup import Axes_Setup_Window
        self.axes_setup_window=Axes_Setup_Window(self,
                                                 self.seq_plotter,
                                                 self.ax,
                                                 parent_widget)



