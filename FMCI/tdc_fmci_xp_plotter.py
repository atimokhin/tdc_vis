from numpy import *
from matplotlib.colors import LogNorm

from ATvis.Common_Data_Plot import AT_Data_Plotter


class tdc_FMCI_XP_Plotter(AT_Data_Plotter):
    """
    Plot Color map of array fmci_XP
    """
    
    __default_plot_ylabel = { 'Electrons' : r'$p_{-}$' ,
                              'Positrons' : r'$p_{+}$' ,
                              'Protons'   : r'$p_{p}$',
                              'Pairs'     : r'$p_\gamma$'   }

    def __init__(self, fmci_XPs, wlims, xlabel=None,ylabel=None,idlabel=None):
        """
        Sets internal variables 
        fmci_xp -- xp data to be plotted
        wlims   -- limits on colormap showing particle weights
        """
        # base class initialization is enough
        AT_Data_Plotter.__init__(self,fmci_XPs, xlabel,ylabel,idlabel)
        # limits on particle weights
        self.wlims=wlims
        # labels -----------------------
        # xlabel
        if not xlabel:
            self.plot_xlabel = r'$x$'
        # ylabel
        if not ylabel:
            self.plot_ylabel = self.__default_plot_ylabel[self.data[0].name]
            self.plot_ylabel_latex=self.plot_ylabel
        # idlabel
        if not idlabel:
            self.plot_idlabel='FMCI_XP:' + self.data[0].name + ':' + self.data[0].calc_id
        # ---------------------------------
        # initialize lines
        self.lines = [ None ]
        self.colorbar  = None
        self.pcolor_args = {}
        
    def plot(self,
             ax,            
             wlims=None,
             symlog=True,
             colorbar=True,
             linthreshy=5,
             **kwargs):
        """
        Plot Color map of array fmci_XP into axes ax
        ----------
        Arguments:
        ----------
        ax
        **kwargs goes to ax.plot(..)
        ----------
        Options:
        ----------
        wlims
           <None> interval for particle weights [wmin,wmax] to be plotted 
                  as distinct colors according the current color map
                  if None, use the default value stored at class initialization
        symlog
           <False>/True --  whether to plot in semi-logarithmic scale
        linthreshy   
           <5>     The range (-x, x) within which the plot is linear
        """
        self.__plot_colormap(ax, wlims, symlog=symlog, linthreshy=linthreshy, **kwargs)
        if colorbar:
            self.__plot_colorbar()
        
    def __plot_colormap(self, 
                        ax,
                        wlims=None,
                        symlog=True,
                        linthreshy=5,
                        **kwargs):
        "Do main plot: colormap of fmci_XP values"
        if wlims is None:
            wlims = self.wlims
        xp = self.data[0]
        self.lines[0] = ax.pcolormesh( xp.x, xp.p,
                                       transpose(xp.fmci_XP),
                                       norm=LogNorm(vmin=0.95*wlims[0],
                                                    vmax=1.05*wlims[1]),
                                       **kwargs)
        # make scaling semi-logatithmic if asked
        if symlog:
            ax.set_yscale('symlog',linthreshy=linthreshy,subsy=[1,10])

    def data_point(self, x, y):
        """
        Returns (z, xx, yy) for the data point x,y
        Used for data inspection
        """
        xp = self.data[0]
        i=xp.x.searchsorted(x)-1
        j=xp.p.searchsorted(y)-1
        # are we within data range?
        if i is None or j is None:
            return None
        xx = [ xp.x[i],  xp.x[i+1] ]
        yy = [ xp.p[j],  xp.p[j+1] ]
        z = xp.fmci_XP[i][j]
        return (z, xx, yy)
    
    def __plot_colorbar(self):
        "Plot colorbar for already plotted color map"
        fig = self.lines[0].get_figure()
        ax  = self.lines[0].get_axes()
        self.colorbar = fig.colorbar(self.lines[0],ax=ax,fraction=0.12,pad=0.03)
        
    def replot(self,ax):
        """
        Plot new colormap, *does not change colorbar* 
        """
        self.__plot_colormap(ax)
        ax.draw_artist(self.lines[0])

    def update_plot(self,ax):
        """
        Plot call replot
        """
        self.replot(ax)

    def set_animated(self,val):
        """
        Set animated property in all lines
        """
        for line in self.lines:
            line.set_animated(val)

