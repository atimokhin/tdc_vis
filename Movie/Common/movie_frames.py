import matplotlib

class MovieFrames:
    """
    Base class for movie frames
    - contains information about number of frames
    - initialize all variables
    - sets size of labels and ticklabels
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
        self.i_frame_max = seq_plotter[0].data[0].get_sequence_length()
        # label of the frame
        self.plot_idlabel = None
        # initialize base class variables ---------------------
        # MovieFrames_Sizes class instance, contains figure sizes and axes boxes
        self.MFS = None
        self.figure = None
        self.ax = []
        
    def plot(self,**kwargs):
        """
        run plotters' plot

        Makes initial plot, but does not plot time label
        it must be plotted in a child class
        """
        for P,A in zip(self.seq_plotter,self.ax):
            P.plot(A,**kwargs)
        
    def get__i_ts(self):
        return self.seq_plotter[0].data[0].get__i_ts()

    def get__id(self):
        return self.seq_plotter[0].data[0].get__id()

    def get_time(self):
        return self.seq_plotter[0].data[0].get_time()



class MovieFrames__Axes(MovieFrames):
    """
    Base class for Movie Frames with visible axes

    self.xlim 
    self.ylim 
    self.formatter
    """
    
    def __init__(self, seq_plotter):
        """
        """
        MovieFrames.__init__(self,seq_plotter)
        self.xlim = []
        self.ylim = []
        self.formatter= []

    def _setup_axes(self,xlim,ylim,axes_commands):
        """
        xlim:
           [[axes1 xlim], [axes2 xlim], ... ]
        ylim:
           [[axes1 ylim], [axes2 ylim], ... ]
        axes_commands:
           [[axes1 commands], [axes2 commands], ... ]
        ------
        - save axes parameters in class variable
        - sets axes formatter, ticklabel, fontsize, limits
        """
        self.__store_axes_setup(xlim,ylim,axes_commands)
        self._setup_axes_from_stored_values()

    def __store_axes_setup(self, xlim, ylim, axes_commands):
        """
        xlim:
           [[axes1 xlim], [axes2 xlim], ... ]
        ylim:
           [[axes1 ylim], [axes2 ylim], ... ]
        axes_commands:
           [[axes1 commands], [axes2 commands], ... ]
        ------
        - save axes parameters in class variable
        """
        # store axes command as a class variable
        self.axes_commands = axes_commands
        # setup formatter, ticklabelsize, and axes limits
        for i in range(len(self.ax)):
            # axes formatter -------------------------
            self.formatter.append( matplotlib.ticker.ScalarFormatter() )
            self.formatter[i].set_powerlimits((-3, 4))
            # axes limits ------------------------
            # xlim: if not set, use the whole x range 
            # will work only for plotters which inherit tdc_Data_vs_X_Plotter 
            if xlim[i] is None:
                xlim[i]=[ self.seq_plotter[i].xmin, self.seq_plotter[i].xmax ]
            self.xlim.append(xlim[i])
            self.ylim.append(ylim[i])

    def _setup_axes_from_stored_values(self):
        """
        Setup axes using parameters values already stored in class
        variables
        
        Sets axes formatter, ticklabel, fontsize, limits
        """
        # setup formatter, ticklabelsize, and axes limits
        for i,A in enumerate(self.ax):
            # axes formatter -------------------------
            A.yaxis.set_major_formatter(self.formatter[i])
            # set ticklabel size ------------------
            A.tick_params(labelsize=self.MFS.ticklabel_fontsize)
            # axes limits ------------------------
            A.set_xlim(self.xlim[i])
            A.set_ylim(self.ylim[i])
            
    def _execute_axes_commands(self):
        "calls A.command "
        for A, commands in zip(self.ax,self.axes_commands):
            if commands:
                for command in commands:
                    try:
                        eval ('A.' + command )
                    except:
                        print 'MovieFrames: Wrong axis command \"%s\"!\n' % str(command)
        
        
