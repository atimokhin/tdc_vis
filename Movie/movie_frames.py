import matplotlib

# LaTeX rendering will be very slow - disable
# sets this for all movie plots
# matplotlib.rcParams['text.usetex'] = False


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
        self.MFS = None
        self.figure = None
        self.ax = []
        self.xlim = []
        self.ylim = []
        self.p_time_label = []
        self.x_label = None
        self.y_label = None
        self.formatter= []
        self.axes_commands_executed_flag = False

    def set_axes_commands_executed_flag(self, val):
        self.axes_commands_executed_flag = val
        
    def set_movie_frames_sizes(self, mfs):
        """
        sets self.MFS
        -------
        Params:
        -------
        mfs
          MovieFrames_Sizes class instance, contains figure sizes and axes boxes
        """
        self.MFS = mfs


    def setup_axes(self,xlim,ylim,axes_commands):
        """
        xlim:
           [[axes1 xlim], [axes2 xlim], ... ]
        ylim:
           [[axes1 ylim], [axes2 ylim], ... ]
        axes_commands:
           [[axes1 commands], [axes2 commands], ... ]
        ------
        - save axes_commands in class variable
        - applies formatter to each axes
        - sets axes ticklabel fontsize
        - sets axes limits
        """
        # store axes command as a class variable
        self.axes_commands = axes_commands
        # setup formatter, ticklabelsize, and axes limits
        for i,A in enumerate(self.ax):
            # axes formatter -------------------------
            self.formatter.append( matplotlib.ticker.ScalarFormatter() )
            self.formatter[i].set_powerlimits((-3, 4))
            A.yaxis.set_major_formatter(self.formatter[i])
            # set ticklabel size ------------------
            A.tick_params(labelsize=self.MFS.ticklabel_fontsize)
            # axes limits ------------------------
            # xlim -- if not set, use the whole x range 
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
        for P,A in zip(self.seq_plotter,self.ax):
            P.plot(A,**kwargs)
        # set axes labels ---------------------
        if not self.x_label:
            # set axes labels ---------------------
            for i,P in enumerate(self.seq_plotter):
                coord_x = self.MFS.xlabel_pos(i)
                self.x_label=self.figure.text( *coord_x, s=P.plot_xlabel,
                                               va='bottom',ha='center',
                                               size=self.MFS.label_fontsize)
                coord_y = self.MFS.ylabel_pos(i)
                self.y_label=self.figure.text( *coord_y, s=P.plot_ylabel,
                                               va='center',ha='left',
                                               size=self.MFS.label_fontsize)
        # execute axes commands ---------------
        if not self.axes_commands_executed_flag:
            for A, commands in zip(self.ax,self.axes_commands):
                if commands:
                    for command in commands:
                        try:
                            eval ('A.' + command )
                        except:
                            print 'Wrong axis command \"', axes_commands[i], '\"!\n'
            # set flag
            self.set_axes_commands_executed_flag(True)
        
    def get__i_timeshot(self):
        return self.seq_plotter[0].get__i_timeshot()

    def get__i_id(self):
        return self.seq_plotter[0].get__i_id()

    def set_main_window(self,window):
        self.main_Window=window

