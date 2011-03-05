import matplotlib

# LaTeX rendering will be very slow - disable
# sets this for all movie plots
matplotlib.rcParams['text.usetex'] = False


class MovieFrames:
    """
    Base class for movie frames
    - contains information about number of frames
    - initialize all variables
    -------------
    Contains:
    -------------
    --- initialize --
    self.seq_plotter
    self.i_frame_min
    self.i_frame_max
    --- empty -------
    self.main_Window
    self.plot_idlabel
    self.figure 
    self.ax 
    self.xlim 
    self.ylim 
    self.p_time_label
    self.formatter
    """

    def __init__(self, seq_plotter):
        # sequence plotter
        if not isinstance( seq_plotter, (tuple,list)):
            raise Exception, 'seq_plotter is not a sequence of seq_plotter\'s!'
        self.seq_plotter = seq_plotter
        # read the first timeshot for all plotters
        for P in self.seq_plotter:
            P.read(1)
        # frame number limits
        self.i_frame_min = 1
        self.i_frame_max = seq_plotter[0].get_sequence_length()
        # label of the frame
        self.plot_idlabel = None
        # initialize base class variables
        self.main_Window = None
        self.figure = None
        self.ax = []
        self.xlim = []
        self.ylim = []
        self.p_time_label = []
        self.formatter= []
        
    def setup_axes(self,xlim,ylim):
        """
        - applies formatter to each axes
        - sets axes limits
        """
        for i,A in enumerate(self.ax):
            # axes formatter -------------------------
            self.formatter.append( matplotlib.ticker.ScalarFormatter() )
            self.formatter[i].set_powerlimits((-3, 4))
            A.yaxis.set_major_formatter(self.formatter[i])
            # axes limits ------------------------
            # xlim -- if not set use the whole x range 
            if xlim[i]==None:
                xlim[i]=[ self.seq_plotter[i].xmin, self.seq_plotter[i].xmax ]
            self.xlim.append(xlim[i])
            self.ylim.append(ylim[i])
            A.set_xlim(self.xlim[i])
            A.set_ylim(self.ylim[i])

    def plot(self,**kwargs):
        """
        Makes initial plot, but does not plot time label
        it must be plotted in a child class
        """
        # main plot
        for P,A,xl,yl in zip(self.seq_plotter,self.ax,self.xlim,self.ylim):
            P.plot(A,**kwargs)
            # set axes labels
            A.set_ylabel(P.plot_ylabel,size='x-large')
            A.set_xlabel(P.plot_xlabel,size='x-large')
        
    def get__i_timeshot(self):
        return self.seq_plotter[0].get__i_timeshot()

    def get__i_id(self):
        return self.seq_plotter[0].get__i_id()

    def set_main_window(self,window):
        self.main_Window=window
