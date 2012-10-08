import matplotlib        as     mpl
import matplotlib.pyplot as     plt
from   matplotlib.cbook  import flatten

from tdc_mpp import tdc_MPP_H

from Common_Data_Plot import paramMPP_Timeseries_MNRAS

                       
class tdc_MPP_Timeseries ( tdc_MPP_H ):
    """
    plots time series of a physical quantity in a grid with shape=(nx,ny)
    """

    def __init__(self, shape, plotter, timeshots, selected=(), fig_param=None):
        """
        shape       -- figure has shape=(nx,ny), nx columns and ny rows
        plotter     -- it plots using plotter
        timeshots   -- (list) timeshots to be plotted
        selected    -- frames# (consecutively numbered) listed here will be highlighted
        """
        # set top_margin_abs if it was not set by calling subroutine
        fig_param_current = paramMPP_Timeseries_MNRAS.copy()
        if fig_param:
            fig_param_current.update(fig_param)
        # make figure and grid
        tdc_MPP_H.__init__(self, *shape, fig_param=fig_param_current)
        # flatten grid into a list of axes
        axs = [ g for g in flatten(self.grid)]
        # compare axis grid and timeshots dimensions
        n_axes       = len(axs)
        n_timeshosts = len(timeshots)
        if ( n_axes != n_timeshosts ):
            print 'Warning: number of timeshots is not equal to the number of plot panles!'
        # number of plots
        n_plots = min( n_axes, n_timeshosts )
        # do actual plotting
        self.timelabels=[]
        for i in range(0,n_plots):
            plotter.read( timeshots[i] )
            plotter.plot( axs[i] )
            t_str= self.fg.timelabel_format % plotter.data[0].get_time()
            # mark selected timeshots with bold line timebox
            if  ( selected.count(i) > 0 ):
                box_linewidth = 1.5*mpl.rcParams['axes.linewidth']
                box_facecolor = 'yellow'
            else:
                box_linewidth = mpl.rcParams['axes.linewidth']
                box_facecolor = 'white'
            # plot timelabels in boxes
            self.timelabels.append(
                axs[i].text( 0.1,1.01, 
                             '$t='+t_str+'$',
                             size = self.fg.timelabel_fontsize,
                             va='center', ha='left', transform=axs[i].transAxes,
                             bbox=dict( facecolor = box_facecolor,
                                        linewidth = box_linewidth )
                             )
                )
        # label y-axes
        for j in range(0,shape[1]):
            self.set_ylabel(j,plotter.plot_ylabel)
        # draw figure
        self.fig.canvas.draw()



    def set_ylim_all(self, *args, **kwargs):
        "call set_ylim command for each axes in grid"
        from  matplotlib.cbook  import flatten
        for ax in flatten(self.grid):
            ax.set_ylim(*args, **kwargs)
        if self.interactive: self.fig.canvas.draw()

    def set_yticks_all(self, *args, **kwargs):
        "call set_ticks for each yaxis in the grid"
        from  matplotlib.cbook  import flatten
        for ax in flatten(self.grid):
            ax.yaxis.set_ticks(*args, **kwargs)
        if self.interactive: self.fig.canvas.draw()

    def set_yticklabels_all(self,labels,tex=False, *args, **kwargs):
        """
        call set_ticklabels for each yaxis in the grid,
        if tex is True, format each label L as "$L$"
        """
        # format in TeX mathmode if necessary
        if tex:
            labels = ["$"+l+"$" for l in labels]
        # set labels for y labelled axes
        for ax in self.y_labelled_axes:
            ax.yaxis.set_ticklabels(labels,*args, **kwargs)
        if self.interactive: self.fig.canvas.draw()


