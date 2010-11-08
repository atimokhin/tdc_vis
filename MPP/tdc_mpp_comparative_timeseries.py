import matplotlib.pyplot as     plt
from   matplotlib.cbook  import flatten

from tdc_mpp import tdc_MPP_H, tdc_MPP_V
                       
class tdc_MPP_Comparative_Timeseries_H ( tdc_MPP_H ):
    """
    Plots multiple plots of physical quantities aligned vertically for
    different moments of time.
    NB: time flows in *horizontal* direction

    Members:
    top_xlabels
    """
    __timelabel_format = '%.3f'
    __timelabel_size   = 8

    def __init__(self, plotters, timeshots, **kwargs):
        """
        gets list of plotters and timeshots, plots
        len(plotters)*len(timeshots) grid marks time of each
        timeshot at the top and labels each plot row at the left
        """
        timelabel_format = kwargs.get('timelabel_format',
                                      tdc_MPP_Comparative_Timeseries_H.__timelabel_format)

        # grid size
        nx = len(timeshots)
        ny = len(plotters)
        # make figure and grid
        tdc_MPP_H.__init__(self,nx,ny, **kwargs)
        # do actual plotting
        self.top_xlabels=[]
        for i in range(ny):
            self.set_ylabel(i,plotters[i].plot_ylabel)
            for j in range(nx):
                # read and plot field
                plotters[i].read( timeshots[j] )
                plotters[i].plot( self.grid[i][j] )
                # top x labels <-- times
                if ( i==0 ):
                    t_str = timelabel_format % plotters[i].get_time()
                    self.top_xlabels.append( self.set_top_xlabel(j, '$t='+t_str+'$') )
        # change fontsize fot timelabel
        for tl in self.top_xlabels:
            tl.set_size(self.__timelabel_size)
        # bottom x labels
        #for j in range(nx): set_bottom_xlabel(j,'$x$')
        # show plots
        self.fig.canvas.draw()


class tdc_MPP_Comparative_Timeseries_V ( tdc_MPP_V ):
    """
    Plots multiple plots of physical quantities aligned horizontally for
    different moments of time.
    NB: time flows in *vertival* direction

    Members:
    top_xlabels
    """
    __timelabel_format = '%.3f'
    __timelabel_size   = 8

    def __init__(self, plotters, timeshots, **kwargs):
        """
        gets list of plotters and timeshots, plots
        len(timeshots)*len(plotters) grid marks time of each
        timeshot at the top and labels each plot row at the left
        """
        timelabel_format = kwargs.get('timelabel_format',
                                      tdc_MPP_Comparative_Timeseries_V.__timelabel_format)

        # grid size
        nx = len(plotters)
        ny = len(timeshots)
        # make figure and grid
        tdc_MPP_V.__init__(self,nx,ny, **kwargs)
        # do actual plotting
        self.top_xlabels=[]
        for i in range(ny):
            for j in range(nx):
                # read and plot field
                plotters[j].read( timeshots[i] )
                plotters[j].plot( self.grid[i][j] )
                # top x labels <-- physical parameter names
                if ( i==0 ):
                    self.top_xlabels.append( self.set_top_xlabel(j, plotters[j].plot_ylabel) )
            # plot ylabels <--- time
            t_str = timelabel_format % plotters[0].get_time()
            timelabel=self.set_ylabel(i,'$t='+t_str+'$')
            timelabel.set_size(self.__timelabel_size)
        # bottom x labels
        #for j in range(nx): set_bottom_xlabel(j,'$x$')
        # show plots
        self.fig.canvas.draw()
