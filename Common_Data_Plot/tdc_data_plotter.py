import numpy  as  np

from Auxiliary import tdc_Mesh

from tdc_data_sequence import tdc_Data_Sequence


class tdc_Plotter:
    """
    Base class for Plotting on both single frame and in animation
    it contains required methods
    which must be implemented in children classes
    -------
    Members:
    --------
    data
       data to be plotted
    plot_label
       TeX string label used for plot annotations
    line
       Line artists with plotted field
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

    def plot(self,ax,**kwargs):
        """
        Do plotting on axes ax - EMPTY
        Must be implemented in a children class
        """
        pass

    def replot(self,ax,**kwargs):
        """
        Do replotting on axes ax - EMPTY
        Must be implemented in a children class
        """
        pass

    def update_plot(self,ax,**kwargs):
        """
        Update plot for animation - EMPTY
        Must be implemented in a children class
        """
        pass

    def set_animated(self,val):
        """
        Set animated property in all lines
        Must be implemented in a children class
        """
        pass
    
    def animation_update(self,ax,i_ts):
        """
        Update animation frame - EMPTY
        Must be implemented in a children class
        """
        pass
    

class tdc_Data_Plotter(tdc_Plotter):
    """
    Base class for *Data* plotting on both single frame and in animation
    it contains all required methods

    plot()
    animation_update()
       must be implemented in children classes
    Adds: ---
    read()
    get_time()

    Redirects all non-implemented methods to data[0] instance
    """

    def __init__(self, data):
        """
        Sets internal variables 
        data
           data to be plotted
        """
        tdc_Plotter.__init__(self,data)

    def __getattr__(self,attrname):
        """
        Redirects all non-implemented methods to data[0] instance
        """
        return getattr(self.data[0], attrname)

    def read(self,i_ts,**kwargs):
        "Read data at i_ts timeshot"
        for d in self.data:
            d.read(i_ts,**kwargs)
    
    def animation_update(self,ax,i_ts):
        """
        Update animation frame:
        - read data for timestep i_ts
        - replot existing lines for the new data
        """
        self.read(i_ts)
        self.update_plot(ax)

    def get_time(self):
        """
        Get time of the current timeshot
        """
        return self.data[0].timetable.get_time()



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
    use_cell_coordinates_flag
       default False
    cells
       cell boundaries class instance

    TODO: describe problems with x coordinate
    it is implicitely defined as a member of tdc_Data_Sequence and
    redirection to data class does not work!
    """
    
    def __init__(self, data):
        # setup base class
        tdc_Data_Plotter.__init__(self,data)
        # set alias for mesh
        self._Mesh = self.data[0]._Mesh
        # set flag, xmin/max, x-label
        self.use_x_coordinates()
        # initialize cells
        self.cells = _CellBoundaries(self._Mesh)
        # by default cell boundaries will be not plotted
        self.show_cells_flag = False
        # by default normalization of X coordinates at every read is not performed
        self.new_x_at_every_read_flag = False

    def read(self,i_ts,**kwargs):
        """
        Read data at i_ts timeshot
        Transform positions into cell
        coordinates if use_cell_coordinates_flag is True
        """
        for d in self.data:
            d.read(i_ts, re_read_x=self._coordinates_chaged_flag,**kwargs)
            # -----------------------------
            # this must be done because x is reassigned and is a member of
            # tdc_Data_Sequence class !
            if isinstance(d, tdc_Data_Sequence):
                d.x = d.current_data.x
            # -----------------------------
            if self.use_cell_coordinates_flag and ( self._coordinates_chaged_flag or
                                                    self.new_x_at_every_read_flag ):
                d.x /= self._Mesh.dx
        # unset _coordinates_chaged_flag
        self._coordinates_chaged_flag = False 

    def plot(self,ax,**kwargs):
        """
        Plot cell boundaries if requested
        """
        if self.show_cells_flag:
            self.cells_on(ax)
        else:
            self.cells.off(ax)
            

    def to_cell_coordinates(self,ax):
        """
        Transforms data of the current plot to cell coordinates
        ()=>
          True  if transformed
          False if not transformed
        """
        if self.use_cell_coordinates_flag:
            return False
        else:
            # set flag, xmin/max, x-label
            self.use_cell_coordinates()
            # ------------------------------
            # get current axes limits
            # ------------------------------
            xlims = ax.get_xlim()
            # transform x limits
            xlims = self._Mesh.x2cell(xlims)
            # change xlim
            ax.set_xlim( xlims )
            # ------------------------------
            # transform data
            # ------------------------------
            # renormalize coordinates
            for d in self.data:
                d.x /= self._Mesh.dx
            # renormalize cell boundaries
            self.cells.to_cell_coordinates(ax)
            # ------------------------------
            return True

    def to_x_coordinates(self,ax):
        """
        Transforms data of the current plot to position coordinates
        ()=>
          True  if transformed
          False if not transformed
        """
        if self.use_cell_coordinates_flag:
            # set flag, xmin/max, x-label
            self.use_x_coordinates()
            # ------------------------------
            # get current axes limits
            # ------------------------------
            xlims = ax.get_xlim()
            # transform x limits
            xlims = self._Mesh.cell2x(xlims)
            # change xlim
            ax.set_xlim( xlims )
            # ------------------------------
            # transform data
            # ------------------------------
            # renormalize coordinates
            for d in self.data:
                d.x *= self._Mesh.dx
            # renormalize cell boundaries
            self.cells.to_x_coordinates(ax)
            # ------------------------------
            return True
        else:
            return False

    def cells_on(self,ax):
        """
        Shows boundaries of all cells on the current plot
        """
        self.cells.on(ax,self.use_cell_coordinates_flag)
        
    def cells_off(self,ax):
        """
        Remove cell boundaries from axes
        """
        self.cells.off(ax)        

        
    def use_cell_coordinates(self):
        """
        Sets: use_cell_coordinates_flag, xmin/xmax, plot_xlabel
        useful for initial settings
        """
        self.use_cell_coordinates_flag = True
        # set xmin,xmax
        self.xmin = 0
        self.xmax = len(self._Mesh.x_b)
        # set xlabel
        self.plot_xlabel  = r'cell #'
        # set coordinates_chaged_flag
        self._coordinates_chaged_flag = True

    def use_x_coordinates(self):
        """
        Sets: use_cell_coordinates_flag, xmin/xmax, plot_xlabel
        useful for initial settings
        """
        self.use_cell_coordinates_flag = False
        # set xmin,xmax
        self.xmin = self._Mesh.xmin
        self.xmax = self._Mesh.xmax
        # set xlabel
        self.plot_xlabel  = r'$x$'
        # set coordinates_chaged_flag
        self._coordinates_chaged_flag = True

    def show_cells_on(self):
        """
        Sets: show_cells_flag = True
        useful for initial settings
        """
        self.show_cells_flag = True

    def show_cells_off(self):
        """
        Sets: show_cells_flag = False
        useful for initial settings
        """
        self.show_cells_flag = False

        

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
        Shows boundaries of all cells on the current plot,
        i.e. only on the visible part of the screen
        - calculate cell line coordinates
        - calls draw fucntion to remove previously plotted cells and plot new ones
        """
        # get current axes limits
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
        # clear existing cell boundaries (if any) and draw new ones
        self.draw(ax)
        
    def off(self,ax):
        """
        Remove cell boundaries from the plot
        """
        # remove cell lines if thery are on the plot
        # (if new axes are created the cell lines will be not there)
        for line in self.cell_lines:
            try:
                ax.lines.remove(line)
            except ValueError:
                pass
        # set lines and coordinates to empty lists 
        self.cell_lines = []
        self.xx_cells   = []


    def to_x_coordinates(self,ax):
        """
        Transforms cell x positions to x coordinates 
        """
        self.xx_cells = self._Mesh.cell2x(self.xx_cells)

    def to_cell_coordinates(self,ax):
        """
        Transforms cell x positions to cell coordinates 
        """
        self.xx_cells = self._Mesh.x2cell(self.xx_cells)
        

    def draw(self,ax):
        """
        Plot cell boundaries using already calculated positions
        """
        # remove cell lines if thery are on the plot
        # (if new axes are created the cell lines will be not there)
        for line in self.cell_lines:
            try:
                ax.lines.remove(line)
            except ValueError:
                pass
        # create new list with cell boundaries
        ylims = ax.get_ylim()
        self.cell_lines = [ ax.plot(xx,ylims,'k:')[0] 
                            for xx in zip(self.xx_cells,self.xx_cells) ]

        
