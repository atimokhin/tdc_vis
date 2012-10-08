from numpy import *
from matplotlib.colors import LogNorm

from Common_Data_Plot import tdc_Data_Plotter

class tdc_FMCI_XP_Plotter(tdc_Data_Plotter):
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
        tdc_Data_Plotter.__init__(self,fmci_XPs, xlabel,ylabel,idlabel)
        # limits on particle weights
        self.wlims=wlims
        # labels -----------------------
        # xlabel
        if not xlabel:
            self.plot_xlabel = r'$x$'
        # ylabel
        if not ylabel:
            self.plot_ylabel = self.__default_plot_ylabel[self.data[0].name]
        # idlabel
        if not idlabel:
            self.plot_idlabel='FMCI_XP:' + self.data[0].name + ':' + self.data[0].calc_id
        # ---------------------------------
        # initialize lines
        self.lines = None
        self.cbar  = None
        
    def plot(self,
             ax,            
             wlims=None,
             symlog=True,
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
        if wlims is None:
            wlims = self.wlims
        xp = self.data[0]
        self.lines = ax.pcolor(xp.x, xp.p, 
                               transpose(xp.fmci_XP),
                               norm=LogNorm(vmin=0.95*wlims[0], vmax=1.05*wlims[1]))
        # make scaling semi-logatithmic if asked
        if symlog:
            ax.set_yscale('symlog',linthreshy=linthreshy,subsy=[1,10])
        # plot colorbar
        self.cbar = ax.get_figure().colorbar(self.lines)

    def replot(self,ax):
        """
        Plot particles for animation at timestep# i_ts
        """
        self.plot(ax)
        ax.draw_artist(self.lines)

    def update_plot(self,ax):
        """
        Plot particles for animation at timestep# i_ts
        """
        self.replot(ax)


    def set_animated(self,val):
        """
        Set animated property in all lines
        """
        pass
        ## for line in self.lines:
        ##     line.set_animated(val)

            

