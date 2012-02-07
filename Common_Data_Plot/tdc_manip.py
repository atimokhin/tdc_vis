import matplotlib
from   tdc_figure_geometry import tdc_Single_FigureGeometry

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

    def __init__(self, fig_param=None):
        # figure geometry
        self.fig_geom = tdc_Single_FigureGeometry(fig_param) 
        # PLOTTER <<<<
        self.plotter = None
        # FIGURE <<<<<
        self.fig = None
        # AXES <<<<<<<
        self.ax  = None
        # i_ts
        self.i_ts = None
        # by default set into interactive mode
        self.interactive=True
        # if True data are restored from dump file
        # and are not connected to the data file
        self.restored_from_dump=False

    def set_plotter(self,plotter):
        # PLOTTER <<<<
        self.plotter = plotter        

    def read(self, i_ts,**kwargs):
        """
        Reads DATA through plotter class interface at timeshot# i_ts
        """
        if not self.restored_from_dump:
            self.i_ts = i_ts
            self.plotter.read(i_ts,**kwargs)
        else:
            print '\nData are restored from dump file and cannot be read for another i_ts!\n'

    def plot(self,
             ylim=None,
             xlim=None,
             print_id=False,
             **kwargs):
        """
        Plot DATA  for already set i_ts.
        All plotting is done via plotter
        ----------
        ylim --    axes limits
        xlim |
        print_id  -- print label on the plot? <False>
        """
        # Create figure and axes -----------
        self.create_figure_and_axes()
        # set window title -----------------
        # id label
        id_label = ('i_ts=%i:' % self.i_ts if self.i_ts else '') + self.plotter.plot_idlabel          
        # if asked put widnow title label  into figure too
        if print_id:
            self.fig.suptitle(id_label, size='x-small')
        id_label = 'Fig %i|' % self.fig.number + id_label
        self.fig.canvas.set_window_title(id_label) 
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
        if matplotlib.rcParams['text.usetex']:
            self.set_ylabel(self.plotter.plot_ylabel_latex)
        else:
            self.set_ylabel(self.plotter.plot_ylabel)
        self.set_xlabel(self.plotter.plot_xlabel)
        # change fontsize
        self._change_ticklabel_fonsize()

    def print_info(self):
        print self

    def create_figure_and_axes(self):
        """
        Create figure and axes
        """
        # FIGURE ---------------------------
        self.fig = matplotlib.pyplot.figure(facecolor='white',
                                            figsize=self.fig_geom.figsize_inch,
                                            dpi=self.fig_geom.dpi)
        # AXES -----------------------------
        self.ax = self.fig.add_axes([self.fig_geom.left_margin,
                                     self.fig_geom.bottom_margin,
                                     self.fig_geom.dx_ax,
                                     self.fig_geom.dy_ax])
        self.ax.yaxis.set_major_formatter(self.fig_geom.formatter)

    def _change_ticklabel_fonsize(self):
        "function for changing fontsize for axes"
        for label in self.ax.xaxis.get_ticklabels():
            label.set_size(self.fig_geom.ticklabel_fontsize)
        for label in self.ax.yaxis.get_ticklabels():
            label.set_size(self.fig_geom.ticklabel_fontsize)

    def set_xlabel(self,xlabel):
        coord = self.fig_geom.xlabel_pos()
        self.x_label=self.fig.text( *coord, s=xlabel,
                                    va='bottom',ha='center',
                                    size=self.fig_geom.label_fontsize)

    def set_ylabel(self,ylabel):
        coord = self.fig_geom.ylabel_pos()
        self.y_label=self.fig.text( *coord, s=ylabel,
                                    va='center',ha='left',
                                    size=self.fig_geom.label_fontsize)

    def set_xlim(self, *args, **kwargs):
        "call set_xlim command for axes"
        self.ax.set_xlim(*args, **kwargs)
        if self.interactive: self.fig.canvas.draw()

    def set_xticks(self, *args, **kwargs):
        "call set_ticks for xaxis"
        self.ax.xaxis.set_ticks(*args, **kwargs)
        if self.interactive: self.fig.canvas.draw()

    def set_xticklabels(self, labels, tex=False, *args, **kwargs):
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

    def set_yticklabels(self, labels, tex=False, *args, **kwargs):
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

    def dump_data(self,filename,dump_id):
        """
        get pure data from plotter and dump it into the pickle file
           'tdc_Filenames.__VisResultsDir/dump_id/filename.pickle' 
        """
        import pickle
        from   Auxiliary import tdc_Filenames
        # get pure data copy
        data = [ d.get_pure_data_copy() for d in self.plotter.data ]
        # full file name of the file with manipulator dump
        filename=tdc_Filenames().get_full_vis_filename(dump_id, filename+'.pickle')
        pickle.dump( data, open(filename,'w') )
        print '\nContent dumped in "%s" \n' % filename

    def _manip_name(self,name):
        """
        Return properly formatted name on the Manip class
        taking restored_from_dump flag into account
        """
        s = ' ==> RESTORED <== ' if self.restored_from_dump else ''
        return name + ':' + s + '\n\n'


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
