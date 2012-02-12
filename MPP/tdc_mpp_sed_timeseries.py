from Auxiliary import tdc_Exception

from tdc_mpp import tdc_MPP_H
                       
class tdc_MPP_SED_Timeseries_H ( tdc_MPP_H ):
    """
    Plots multiple plots of SED  for different moments of time.
    NB: time flows in *horizontal* direction

    Members:
    top_xlabels
    """

    def __init__(self, plotter, timeshots, xxs, fig_param=None):
        """
        gets list of plotters and timeshots, plots
        len(plotters)*len(timeshots) grid marks time of each
        timeshot at the top and labels each plot row at the left
        """
        # check length of parameter arrays
        if len(timeshots)!=len(xxs):
            print '\n len(timeshots)!=len(xxs) : %g != %g\n\n' % (len(timeshots),len(xxs))
            raise tdc_Exception()
        # grid size
        nx = len(timeshots)
        ny = 2
        # make figure and grid
        tdc_MPP_H.__init__(self,nx,ny, fig_param)
        # do actual plotting
        self.top_xlabels=[]
        for j in range(nx):
            # read and plot field
            plotter.read( timeshots[j], xx=xxs[j] )
            plotter.plot( self.grid[0][j], prefix = 'lc' )
            plotter.plot( self.grid[1][j], prefix = 'ns' )
            # top x labels <-- times
            t_str = self.fg.timelabel_format % plotter.get_time()
            self.top_xlabels.append( self.set_top_xlabel(j, '$t='+t_str+'$') )
        # bottom x labels
        #for j in range(nx): set_bottom_xlabel(j,'$x$')
        self._delete_xlabels_for_middle_plots()
        self._delete_ylabels_for_middle_plots()
        # show plots
        self.fig.canvas.draw()


