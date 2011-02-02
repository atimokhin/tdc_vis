from tdc_single_figure_geometry import tdc_Single_FigureGeometry

class tdc_Manip:
    """
    Base class for Manipulators

    Members:
    --------
    fig
       figure
    ax
       axes
    plotter
       plotter
    i_ts
       current timeshot for data
    """
    __label_size         = 15
    __ticklabel_fontsize = 10

    def __init__(self, plotter, **kwargs):
        # ----------------------------------------
        # setup figure parameters
        self._label_size         = kwargs.get('label_size',
                                              tdc_Manip.__label_size)
        self._ticklabel_fontsize = kwargs.get('ticklabel_fontsize',
                                              tdc_Manip.__ticklabel_fontsize)
        # ----------------------------------------
        #figure geometry
        self.fg = tdc_Single_FigureGeometry(**kwargs) 
        # by default set into interactive mode
        self.interactive=True
        # PLOTTER <<<<
        self.plotter = plotter
        # i_ts
        self.i_ts = None
        # FIGURE <<<<<
        self.fig = None
        # AXES <<<<<<<
        self.ax  = None


    def read(self, i_ts,**kwargs):
        """
        Reads DATA through plotter class interface at timeshot# i_ts
        """
        self.i_ts=i_ts
        self.plotter.read(i_ts,**kwargs)


    def plot(self, ylim=None, xlim=None,
             print_id=False,**kwargs):
        """
        Plot DATA  for already set i_ts.
        All plotting is done via plotter
        ----------
        ylim --    axes limits
        xlim |
        print_id  -- print label on the plot? <False>
        """
        # FIGURE ---------------------------------
        self.fig = self.fg.create_figure(facecolor='w')
        # set window title
        # id_label
        id_label = self.plotter.plot_idlabel   +\
                   '   i_ts=' +  str(self.i_ts)
        self.fig.canvas.set_window_title(id_label) 
        # if asked put widnow title label  into figure too
        if print_id:
            self.fig.suptitle(id_label,size='x-small' )
        # AXES ------------------------------------ 
        self.ax  = self.fig.axes[0]
        # PLOT
        self.plotter.plot(self.ax,**kwargs)
        # set axes limits:
        # xlim -- if not set use the whole x range 
        if xlim==None:
            xlim=[ self.plotter.xmin, self.plotter.xmax ]
        self.ax.set_xlim(xlim)
        # ylim -- if not set use automatic setting 
        if ylim!=None:
            self.ax.set_ylim(ylim)
        # labels
        self.set_ylabel(self.plotter.plot_ylabel)
        self.set_xlabel(self.plotter.plot_xlabel)
        # change fontsize
        self._change_ticklabel_fonsize()


    def print_info(self):
        print self

    def _change_ticklabel_fonsize(self):
        "function for changing fontsize for axes"
        for label in self.ax.xaxis.get_ticklabels():
            label.set_size(self._ticklabel_fontsize)
        for label in self.ax.yaxis.get_ticklabels():
            label.set_size(self._ticklabel_fontsize)

    def set_xlabel(self,xlabel):
        coord = self.fg.xlabel_pos()
        self.x_label=self.fig.text( *coord, s=xlabel, va='center',ha='center', size=self._label_size)

    def set_ylabel(self,ylabel):
        coord = self.fg.ylabel_pos()
        self.y_label=self.fig.text( *coord, s=ylabel, va='center',ha='left', size=self._label_size)

    def set_xlim(self, *args, **kwargs):
        "call set_xlim command for axes"
        self.ax.set_xlim(*args, **kwargs)
        if self.interactive: self.fig.canvas.draw()

    def set_xticks(self, *args, **kwargs):
        "call set_ticks for xaxis"
        self.ax.xaxis.set_ticks(*args, **kwargs)
        if self.interactive: self.fig.canvas.draw()

    def set_xticklabels(self, labels, tex=True, *args, **kwargs):
        """
        call set_ticklabels for xaxis 
        if tex is True, format each label L as "$L$"
        """
        # format in TeX mathmode if necessary
        if tex:
            labels = ['$'+l+'$' for l in labels]
        # set labels for x labelled axes
        self.ax.xaxis.set_ticklabels(labels,*args, **kwargs)
        if self.interactive: self.fig.canvas.draw()

    def set_ylim(self, *args, **kwargs):
        "call set_ylim command for axes"
        self.ax.set_ylim(*args, **kwargs)
        if self.interactive: self.fig.canvas.draw()

    def set_yticks(self, *args, **kwargs):
        "call set_ticks for yaxis"
        self.ax.yaxis.set_ticks(*args, **kwargs)
        if self.interactive: self.fig.canvas.draw()

    def set_yticklabels(self, labels, tex=True, *args, **kwargs):
        """
        call set_ticklabels for yaxis 
        if tex is True, format each label L as "$L$"
        """
        # format in TeX mathmode if necessary
        if tex:
            labels = ['$'+l+'$' for l in labels]
        # set labels for x labelled axes
        self.ax.yaxis.set_ticklabels(labels,*args, **kwargs)
        if self.interactive: self.fig.canvas.draw()

    def interactive_on(self):
        """
        set into interactive mode: changes to figure are plotted
        immediately
        """
        self.interactive=True

    def interactive_off(self):
        """
        switch off interactive mode: changes to figure delayed till
        draw is called
        """
        self.interactive=False



class tdc_Manip_Plot_vs_X(tdc_Manip):
    """
    Manipulators for plots vs x-coordinate
    Adds:
    - switching between X and CELL coordinates
    - switching between CELL boundaries ON/OFF
    """
        
    def to_cell_coordinates(self):
        """
        Convert CURRENT plot to cell cordinates
        """
        self.plotter.to_cell_coordinates(self.ax)
        self.plotter.replot(self.ax)
        self.plotter.cells.draw(self.ax)
        self.x_label.set_text(self.plotter.plot_xlabel)
        self.fig.canvas.draw()

    def to_x_coordinates(self):
        """
        Convert CURRENT plot to x cordinates
        """
        self.plotter.to_x_coordinates(self.ax)
        self.plotter.replot(self.ax)
        self.plotter.cells.draw(self.ax)
        self.x_label.set_text(self.plotter.plot_xlabel)
        self.fig.canvas.draw()
        
    def cells_on(self):
        """
        Shows cell boundaries on the CURRENT plot
        """
        self.plotter.cells_on(self.ax)
        self.fig.canvas.draw()

    def cells_off(self):
        """
        Deletes cell boundaries from the CURRENT plot
        """
        self.plotter.cells_off(self.ax)
        self.fig.canvas.draw()
