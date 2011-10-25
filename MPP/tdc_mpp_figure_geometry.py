
class tdc_MPP_FigureGeometry:
    """
    class for defining geometry of multiple plot grid
    at setup calculates all geometry parameters of the plots
    requires following parameters:
    ----------------
    Members:
    ----------------
    self.left_margin  
    self.right_margin 
    self.top_margin   
    self.bottom_margin
    # figure size
    self.fig_height_abs 
    self.fig_width_abs  
    # can use for figure aspect ratio adjustment
    self.dx_ax_abs  
    self.dy_ax_abs  
    self.dx_pad_abs 
    self.dy_pad_abs 
    # label positions
    self.xlabel_bottom_y 
    self.xlabel_top_y    
    self.ylabel_left_x   
    self.ylabel_right_x  
    """
    # Default values:
    fig_width_abs = 7;
    aspect_ratio  = 1.618
    dx_pad_abs = 0.1
    dy_pad_abs = 0.1
    left_margin_abs   = 0.45
    right_margin_abs  = 0.05
    top_margin_abs    = 0.2
    bottom_margin_abs = 0.35
    xlabel_bottom_y_abs = 0.01
    xlabel_top_y_abs    = 0.01
    ylabel_left_x_abs   = 0.01
    ylabel_right_x_abs  = 0.10


    def __init__(self,nx,ny,**kwargs):
        """
        for gives number of column nx and rows ny calculates all
        geometry parameters of mupltiple plots

        all ..._abs quantities are measured in inches
        all other quantities  -- in figure coordinates
        """
        # ========================================
        # setup figure parameters in absolute units [inches]
        # ========================================
        # figure width
        self.fig_width_abs = kwargs.get('self.fig_width_abs',
                                        tdc_MPP_FigureGeometry.fig_width_abs)
        # margins --------------------------------
        left_margin_abs   = kwargs.get('left_margin_abs',
                                       tdc_MPP_FigureGeometry.left_margin_abs)
        right_margin_abs  = kwargs.get('right_margin_abs',
                                       tdc_MPP_FigureGeometry.right_margin_abs)
        top_margin_abs    = kwargs.get('top_margin_abs',
                                       tdc_MPP_FigureGeometry.top_margin_abs)
        bottom_margin_abs = kwargs.get('bottom_margin_abs',
                                       tdc_MPP_FigureGeometry.bottom_margin_abs)
        # axis alabe positions -------------------
        xlabel_bottom_y_abs = kwargs.get('xlabel_bottom_y_abs',
                                         tdc_MPP_FigureGeometry.xlabel_bottom_y_abs)
        xlabel_top_y_abs    = kwargs.get('xlabel_top_y_abs',
                                         tdc_MPP_FigureGeometry.xlabel_top_y_abs)
        ylabel_left_x_abs   = kwargs.get('ylabel_left_x_abs',
                                         tdc_MPP_FigureGeometry.ylabel_left_x_abs)
        ylabel_right_x_abs  = kwargs.get('ylabel_right_x_abs',
                                         tdc_MPP_FigureGeometry.ylabel_right_x_abs)
        # padding between individual plots ------
        dx_pad_abs = kwargs.get('dx_pad_abs',tdc_MPP_FigureGeometry.dx_pad_abs)
        dy_pad_abs = kwargs.get('dy_pad_abs',tdc_MPP_FigureGeometry.dy_pad_abs)
        # aspect ratio
        aspect_ratio = kwargs.get('aspect_ratio',tdc_MPP_FigureGeometry.aspect_ratio)
        # ========================================
        # figure parameters in relative units
        # ========================================
        # margins: left/right
        self.left_margin  = float(left_margin_abs)/self.fig_width_abs
        self.right_margin = float(right_margin_abs)/self.fig_width_abs
        # axes sizes: x direction
        dx_pad = float(dx_pad_abs)/self.fig_width_abs    
        dx_ax_abs = ( self.fig_width_abs - \
                      left_margin_abs - right_margin_abs - \
                      dx_pad_abs*(nx-1) )/float(nx)
        dx_ax = dx_ax_abs/self.fig_width_abs
        # axes sizes: y direction
        dy_ax_abs = dx_ax_abs/aspect_ratio
        # figure height
        self.fig_height_abs = dy_ax_abs*ny + dy_pad_abs*(ny-1) + \
                              bottom_margin_abs + top_margin_abs
        # margins: top/bottom
        self.top_margin    = float(top_margin_abs)/self.fig_height_abs
        self.bottom_margin = float(bottom_margin_abs)/self.fig_height_abs
        # axes sizes: y direction
        dy_pad = float(dy_pad_abs)/self.fig_height_abs
        dy_ax  = float(dy_ax_abs)/self.fig_height_abs
        # lambda function for axis positions
        self.rect = lambda i, j: \
                    [self.left_margin   + (dx_ax + dx_pad)*j, \
                     self.bottom_margin + (ny-i-1)*(dy_ax + dy_pad),\
                     dx_ax, dy_ax]
        # can use for figure aspect ratio adjustment
        self.dx_ax_abs  = dx_ax_abs
        self.dy_ax_abs  = dy_ax_abs
        self.dx_pad_abs = dx_pad_abs
        self.dy_pad_abs = dy_pad_abs
        # label positions
        self.xlabel_bottom_y = float(xlabel_bottom_y_abs)/self.fig_height_abs
        self.xlabel_top_y    = float(xlabel_top_y_abs)/self.fig_height_abs
        self.ylabel_left_x   = float(ylabel_left_x_abs)/self.fig_width_abs
        self.ylabel_right_x  = float(ylabel_right_x_abs)/self.fig_width_abs


    def get_figsize_abs(self):
        "returns tuple of figure size in inches (width, height)"
        return (self.fig_width_abs, self.fig_height_abs)

    def axes_rectangle(self, i, j):
        """
        for row i and column j returns rectangle (x,y,dx,dy)
        defining (i,j)'th axes position in figure coordinates
        """
        return self.rect(i,j)

    def top_xlabel_pos(self, j):
        "top x label position for j'th column in figure coordinates"
        return ( self.rect(0,j)[0]+self.rect(0,j)[2]/2.,
                 1-self.xlabel_top_y)

    def bottom_xlabel_pos(self, j):
        "bottom x label position for j'th column in figure coordinates"
        return ( self.rect(0,j)[0]+self.rect(0,j)[2]/2.,
                 self.xlabel_bottom_y)

    def left_ylabel_pos(self, i):
        "left y label position for i'th row in figure coordinates"
        return ( self.ylabel_left_x,
                 self.rect(i,0)[1]+self.rect(i,0)[3]/2.)

    def right_ylabel_pos(self, i):
        "right y label position for i'th row in figure coordinates"
        return ( 1-self.ylabel_right_x,
                 self.rect(i,0)[1]+self.rect(i,0)[3]/2.)


                       
