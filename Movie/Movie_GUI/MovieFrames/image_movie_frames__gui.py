import gtk, gobject

from Auxiliary        import *
from Common_Data_Plot import *
from Movie            import *

from matplotlib.figure                  import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas


class Image_MovieFrames__GUI(MovieFrames):
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
        # initialize base class 
        MovieFrames.__init__(self, seq_plotter)
        # GUI specific members -------
        self.main_Window = None
        # set redraw_flag 
        self.redraw_flag=False

    def _setup_figure_and_axes(self, mfs):
        """
        Creates figure and axes accordinng to sized in class mfs
        -------
        Params:
        -------
        mfs
          quasi MovieFrames_Sizes class instance, contains figure sizes and axes boxes
        """
        # set MFS
        self.MFS = mfs
        # plot window ----------------------------
        # self.figure = Figure(facecolor='white',dpi=self.MFS.dpi)
        self.figure = Figure(facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.set_size_request( *self.MFS.figsize_points )
        # axes -----------------------------------
        # add as many axes as there are entries in mfs.axes_boxes
        for box in self.MFS.axes_boxes:
            self.ax.append( self.figure.add_axes(box) )

    def __erase_axes(self):
        for A in self.ax:
            A.set_frame_on(False)
            A.xaxis.set_visible(False)
            A.yaxis.set_visible(False)
            
    def plot(self,**kwargs):
        """
        Makes initial plot and set text for the timelabel
        """
        MovieFrames.plot(self,**kwargs)
        self.__erase_axes()

    def replot(self,**kwargs):
        """
        - plotters' plot
        - erase axes
        """
        # do plot
        MovieFrames.plot(self,animated=True,**kwargs)
        self.__erase_axes()

    def animation_update(self,i_frame):
        """
        Updates plot and timelabel
        """
        for P,A in zip(self.seq_plotter,self.ax):
            P.animation_update( A, i_frame )

    def set_animated(self,val):
        """
        changes *animated* attribute for all changing entries
        """
        for P in self.seq_plotter:
            P.set_animated(val)

    def set_main_window(self,window):
        "Sets the main window for matplotlib widget"
        self.main_Window=window
        


