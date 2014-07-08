from ATvis.MPP import AT_MPP_V, AT_MPP_Colorbar_Right


class tdc_MPP__XP_XPDensity(AT_MPP_V,AT_MPP_Colorbar_Right):
    """
    Plots vertical rows cascade phase potraits
    - the first row must be an XP potrait showing numerical particles
    - the rest rows are densities of plasma compoments in pahase space
    - plots colorbar for density plots on the right of the plot
    """
    
    def __init__(self, plotters, timeshots, fig_param=None):
        """
        """
        self.plotters=plotters
        nx = len(timeshots)
        ny = len(plotters)        
        AT_MPP_V.__init__(self,nx,ny, fig_param=fig_param)
        # do actual plotting
        self.top_xlabels=[]
        for i in range(ny):
            self.set_ylabel(i, plotters[i].plot_ylabel)
            for j in range(nx):
                # read and plot field
                plotters[i].read( timeshots[j] )
                if i == 0:
                    plotters[i].plot(self.grid[i][j] )
                else: 
                    plotters[i].plot( self.grid[i][j], colorbar=False)
        # wrap MPP instance in an MPP_Colorbar_Right instance
        AT_MPP_Colorbar_Right.__init__(self,self, plotters[1], fig_param=fig_param)
        self.fig.canvas.draw()
        
        
