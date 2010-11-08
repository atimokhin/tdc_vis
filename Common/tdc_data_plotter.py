import numpy  as  np

from tdc_mesh import tdc_Mesh

class tdc_Data_Plotter:
    """
    Base class for data plotting on both single frame and in animation
    it contains all required methods

    plot()
    animation_update()
       must be implemented in children classes

    Members:
    --------
    data
       data to be plotted
    plot_label
       TeX string label used for plot annotations
    line
       Line artists with plotted field

    Redirects all non-implemented methods to data[0] instance
    """

    def __init__(self, data):
        """
        Sets internal variables 
        data
           data to be plotted
        """
        # be sure data is a sequnce
        if not isinstance( data, (list,tuple) ):
            data = (data,)
        self.data=data
        # plot labels
        self.plot_ylabel  = None
        self.plot_xlabel  = None
        self.plot_idlabel = None
        # initialize lines
        self.lines = len(self.data)*[None]


    def __getattr__(self,attrname):
        "Redirects all non-implemented methods to data[0] instance"
        return getattr(self.data[0], attrname)


    def read(self,i_ts,**kwargs):
        "Read data at i_ts timeshot"
        for d in self.data:
            d.read(i_ts,**kwargs)

    def plot(self,ax,**kwargs):
        "Do plotting on axes ax - EMPTY"
        pass

    def get_time(self):
        "Get time of the current timeshot"
        return self.data[0].timetable.get_time()

    def set_animated(self,val):
        "Set animated property in all lines"
        for line in self.lines:
            line.set_animated(val)

    def animation_update(self,ax,i_ts):
        "Update animation frame - EMPTY"
        pass



class tdc_Data_vs_X_Plotter(tdc_Data_Plotter):
    """
    Base class for plotters of physical quantities
    being functions of space positions
    Adds functionality for:
    1) transformation between positions and cell number coordinates
    2) showing cell boundaries
    Members:
    --------
    xmin --|
    xmax --|<-mesh boundaries
       
    _Mesh
       tdc_Mesh instnace (tied to data[0].calc_id)
    _use_cell_coordinates_flag
       default False
    cells
       cell boundaries class instance
    """
    
    def __init__(self, data):
        # setup base class
        tdc_Data_Plotter.__init__(self,data)
        # read mesh
        self._Mesh = tdc_Mesh(self.data[0].calc_id)
        # set flag, xmin/max, x-label
        self.use_x_coordinates()
        # initialize cells
        self.new_cell_boundary_class()

    def read(self,i_ts,**kwargs):
        """
        Read data at i_ts timeshot
        Transform positions into cell
            coordinates if _use_cell_coordinates_flag is True
        """
        for d in self.data:
            d.read(i_ts, re_read_x=self._use_cell_coordinates_flag,**kwargs)
            if self._use_cell_coordinates_flag:
                d.x = self._Mesh.x2cell(d.x)

    def new_cell_boundary_class(self):
        """
        Create new instance of cells
        this function must be called when new plot is created
        """
        self.cells = _CellBoundaries(self._Mesh)

    def to_cell_cordinates(self,ax):
        """
        Replot currend plot in cell coordinates
        ()=>
          True  if replotted
          False if not replotted
        """
        if self._use_cell_coordinates_flag:
            return False
        else:
            # set flag, xmin/max, x-label
            self.use_cell_coordinates()
            # ------------------------------
            # get current axes limits
            # ------------------------------
            ylims = ax.get_ylim()
            xlims = ax.get_xlim()
            # ------------------------------
            # transform data
            # ------------------------------
            # renormalize coordinates
            for d in self.data:
                d.x = self._Mesh.x2cell(d.x)
            # ------------------------------
            # replot 
            # ------------------------------
            self.plot(ax)
            # draw cell boundaries
            self.cells.to_cell_cordinates(ax,ylims)
            # ------------------------------
            # set axes limits
            # ------------------------------
            # transform x limits
            xlims = self._Mesh.x2cell(xlims)
            # set correct limits
            ax.set_ylim(ylims)
            ax.set_xlim(xlims)
            return True

    def to_x_cordinates(self,ax):
        """
        Replot currend plot in position coordinates
        ()=>
          True  if replotted
          False if not replotted
        """
        if self._use_cell_coordinates_flag:
            # set flag, xmin/max, x-label
            self.use_x_coordinates()
            # ------------------------------
            # get current axes limits
            # ------------------------------
            ylims = ax.get_ylim()
            xlims = ax.get_xlim()
            # ------------------------------
            # transform data
            # ------------------------------
            # renormalize coordinates
            for d in self.data:
                d.x = self._Mesh.cell2x(d.x)
            # ------------------------------
            # replot 
            # ------------------------------
            self.plot(ax)
            # cell boundaries
            self.cells.to_x_cordinates(ax,ylims)
            # ------------------------------
            # set axes limits
            # ------------------------------
            # transform x limits
            xlims = self._Mesh.cell2x(xlims)
            # set correct limits
            ax.set_ylim(ylims)
            ax.set_xlim(xlims)
            return True
        else:
            return False

    def cells_on(self,ax):
        "Shows boundaries of all cells on the current plot"
        self.cells.on(ax,self._use_cell_coordinates_flag)
        
    def cells_off(self,ax):
        "Remove cell boundaries from axes"
        self.cells.off(ax)        
        
    def use_cell_coordinates(self):
        """
        Sets: _use_cell_coordinates_flag, xmin/xmax, plot_xlabel
        """
        self._use_cell_coordinates_flag = True
        # set xmin,xmax
        self.xmin = 0
        self.xmax = len(self._Mesh.x_b)
        # set xlabel
        self.plot_xlabel  = r'cell #'

    def use_x_coordinates(self):
        """
        Sets: _use_cell_coordinates_flag, xmin/xmax, plot_xlabel
        """
        self._use_cell_coordinates_flag = False
        # set xmin,xmax
        self.xmin = self._Mesh.xmin
        self.xmax = self._Mesh.xmax
        # set xlabel
        self.plot_xlabel  = r'$x$'


        

class _CellBoundaries:
    """
    Auxiliary class responsible for cell boundary lines
    """

    def __init__(self, mesh):
        self._Mesh = mesh
        # initialize cell_lines to an empty list
        self.cell_lines = []
        self.xx_cells   = []
    
    def on(self,ax,use_cell_coordinates):
        """
        Shows boundaries of all cells on the current plot
        """
        # clear existing cell lines
        self.off(ax)
        # get current axes limits
        ylims = ax.get_ylim()
        xlims = ax.get_xlim()
        # transform x limits
        if use_cell_coordinates:
            xlims_cell = xlims
        else:
            xlims_cell = self._Mesh.x2cell(xlims)
        # calculate cell boundaries (ndarray -easy to change values)
        self.xx_cells = np.arange(int(xlims_cell[0]),int(xlims_cell[1]))
        if not use_cell_coordinates:
           self.xx_cells = self._Mesh.cell2x(self.xx_cells)
        # draw cell boundaries
        self.draw(ax,ylims)
        # set correct limits
        ax.set_ylim(ylims)
        ax.set_xlim(xlims)
        
    def off(self,ax):
        """
        Remove cell boundaries from plot
        """
        for line in self.cell_lines:
            ax.lines.remove(line)
        self.cell_lines = []
        self.xx_cells   = []

    def to_x_cordinates(self,ax,ylims):
        self.xx_cells = self._Mesh.cell2x(self.xx_cells)
        self.draw(ax,ylims)

    def to_cell_cordinates(self,ax,ylims):
        self.xx_cells = self._Mesh.x2cell(self.xx_cells)
        self.draw(ax,ylims)
        
    def draw(self,ax,ylims):
        # delete already existing cell lines
        for line in self.cell_lines:
            ax.lines.remove(line)
        # create new list with cell boundaries
        self.cell_lines = [ ax.plot(xx,ylims,'k:')[0] 
                             for xx in zip(self.xx_cells,self.xx_cells) ]
        # draw cell boundaries
        for line in self.cell_lines:
            ax.draw_artist(line)
        
