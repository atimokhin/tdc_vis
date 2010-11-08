import matplotlib.pyplot as plt
from   matplotlib.ticker import ScalarFormatter

class tdc_Single_FigureGeometry:
    """
    Class for single plot figures
    sets fifure size, axes positions
    """
    fig_width_abs     = 7;
    aspect_ratio      = 1.618
    left_margin_abs   = 0.8
    right_margin_abs  = 0.1
    top_margin_abs    = 0.3
    bottom_margin_abs = 0.5
    f_ylabel_left     = 0.2
    f_xlabel_bottom   = 0.2

    def __init__(self,**kwargs):
        """
        """
        # ----------------------------------------
        # setup figure parameters
        self.fig_width_abs   = kwargs.get('fig_width_abs',
                                          tdc_Single_FigureGeometry.fig_width_abs)
        self.f_ylabel_left   = kwargs.get('f_ylabel_left',
                                          tdc_Single_FigureGeometry.f_ylabel_left)
        self.f_xlabel_bottom = kwargs.get('f_xlabel_bottom',
                                          tdc_Single_FigureGeometry.f_xlabel_bottom)
        left_margin_abs  = kwargs.get('left_margin_abs',
                                      tdc_Single_FigureGeometry.left_margin_abs)
        right_margin_abs = kwargs.get('right_margin_abs',
                                      tdc_Single_FigureGeometry.right_margin_abs)
        top_margin_abs    = kwargs.get('top_margin_abs',
                                       tdc_Single_FigureGeometry.top_margin_abs)
        bottom_margin_abs = kwargs.get('bottom_margin_abs',
                                       tdc_Single_FigureGeometry.bottom_margin_abs)
        aspect_ratio     = kwargs.get('aspect_ratio',
                                      tdc_Single_FigureGeometry.aspect_ratio)
        # ----------------------------------------
        self.left_margin = left_margin_abs/self.fig_width_abs
        right_margin     = right_margin_abs/self.fig_width_abs
        self.dx_ax = 1-self.left_margin-right_margin
        dy_ax_abs  = self.dx_ax/aspect_ratio*self.fig_width_abs
        self.fig_height_abs = dy_ax_abs + top_margin_abs + bottom_margin_abs
        self.dy_ax          = dy_ax_abs/self.fig_height_abs
        self.bottom_margin  = bottom_margin_abs/self.fig_height_abs
        # formatter ------------------------------
        self.formatter=ScalarFormatter()
        self.formatter.set_powerlimits((-3, 4))


    def xlabel_pos(self):
        "x label position in figure coordinates"
        return ( self.left_margin+.5*self.dx_ax,
                 self.f_xlabel_bottom*self.bottom_margin)

    def ylabel_pos(self):
        "y label position in figure coordinates"
        return ( self.f_ylabel_left*self.left_margin,
                 self.bottom_margin+.5*self.dy_ax)

    def create_figure(self,**kwargs):
        "Create figure and axes"
        # figure object
        fig = plt.figure(figsize=(self.fig_width_abs, self.fig_height_abs),**kwargs )
        # axes
        ax = fig.add_axes([self.left_margin,
                           self.bottom_margin,
                           self.dx_ax,
                           self.dy_ax])
        ax.yaxis.set_major_formatter(self.formatter)
        return fig
