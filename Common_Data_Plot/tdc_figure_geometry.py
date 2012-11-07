import matplotlib
from matplotlib.ticker import ScalarFormatter

from figure_params     import paramSingleFig_Work

class tdc_Single_FigureGeometry:
    """
    Class for single plot figures, sets:
        figure size,
        axes positions,
        label positions,
        formatter
        label and ticklabel fontsizes
    """

    def __init__(self,fig_param=None):
        """
        Initialize figure and axes parameters
        ------------
        params
        ------------
        fig_param
            <None>  - configurable parameters of the Figure
                      Example:
                      dict(figsize_points     = [720,480],
                           axes_boxes         = [[0.12,.1375,.86,.8]],
                           ylabel_left_x      = 0.01,
                           xlabel_bottom_y    = 0.01,
                           label_fontsize     = 20,
                           ticklabel_fontsize = 11)
                    - if None fig_param=paramSingleFig_Work,
                      defined in figure_params.py
        """
        # -----------------------------
        # Customizable parameters
        # -----------------------------
        # assume  paramSingleFig_Work as default
        if not fig_param:
            fig_param = paramSingleFig_Work
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  
        # if parameter is not specified,
        # its value in paramSingleFig_Work is used
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # figure size and axes position
        self.figsize_points = fig_param.get('figsize_points',
                                            paramSingleFig_Work['figsize_points'])
        self.axes_boxes     = fig_param.get('axes_boxes',
                                            paramSingleFig_Work['axes_boxes'])
        # label sizes
        self.label_fontsize = fig_param.get('label_fontsize',
                                            paramSingleFig_Work['label_fontsize'])
        self.ticklabel_fontsize = fig_param.get('ticklabel_fontsize',
                                                paramSingleFig_Work['ticklabel_fontsize'])
        # label positions
        self.xlabel_bottom_y = fig_param.get('xlabel_bottom_y',
                                             paramSingleFig_Work['xlabel_bottom_y'])
        self.xlabel_bottom_x = fig_param.get('xlabel_bottom_x',
                                             paramSingleFig_Work['xlabel_bottom_x'])
        self.ylabel_left_x   = fig_param.get('ylabel_left_x',
                                             paramSingleFig_Work['ylabel_left_x'])
        self.ylabel_left_y   = fig_param.get('ylabel_left_y',
                                             paramSingleFig_Work['ylabel_left_y'])
        # -------------------------------------
        # figure size in inches
        self.dpi = matplotlib.rcParams['figure.dpi']
        print 'dpi=',self.dpi

        self.figsize_inch = fig_param.get('figsize_inch',
                                          [self.figsize_points[0]/self.dpi,
                                           self.figsize_points[1]/self.dpi])
        print 'figsize_inch=',self.figsize_inch
        
        # axes related parameters
        self.dx_ax = self.axes_boxes[0][2]
        self.dy_ax = self.axes_boxes[0][3]
        self.left_margin   = self.axes_boxes[0][0]
        self.bottom_margin = self.axes_boxes[0][1]
        # formatter
        self.formatter=ScalarFormatter()
        self.formatter.set_powerlimits((-3, 4))


    def xlabel_pos(self,i=0):
        """
        x label position in figure coordinates
        """
        if self.xlabel_bottom_x is None:
            xlabel_bottom_x = self.left_margin+.5*self.dx_ax
        else: 
            xlabel_bottom_x = self.xlabel_bottom_x
        return ( xlabel_bottom_x, self.xlabel_bottom_y)

    def ylabel_pos(self,i=0):
        """
        y label position in figure coordinates
        """
        if self.ylabel_left_y is None:
            ylabel_left_y = self.bottom_margin+.5*self.dy_ax
        else:
            ylabel_left_y = self.ylabel_left_y
        return ( self.ylabel_left_x, ylabel_left_y)



class tdc_Double_FigureGeometry(tdc_Single_FigureGeometry):
    """
    Size of figure and axes boxes for single pane movie frame
    """

    def __init__(self,fig_param=None):
        tdc_Single_FigureGeometry.__init__(self,fig_param)
        self.figsize_points=[720,600]
        self.axes_boxes=[[0.12,.55,.86,.43], [0.12,.11,.86,.43]]
        # axes related parameters
        self.y_BOT_ax_center = self.bottom_margin    + 0.5*self.axes_boxes[1][3]
        self.y_TOP_ax_center = self.axes_boxes[0][1] + 0.5*self.axes_boxes[0][3]

    def ylabel_pos(self,i):
        """
        y label position in figure coordinates
        """
        if self.ylabel_left_y is None:
            ylabel_left_y = self.y_TOP_ax_center if i==0 else self.y_BOT_ax_center
        else:
            ylabel_left_y = self.ylabel_left_y
        return ( self.ylabel_left_x, ylabel_left_y)
