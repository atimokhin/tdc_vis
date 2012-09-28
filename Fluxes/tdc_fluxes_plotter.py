## import Common
from Common_Data_Plot import tdc_Data_Plotter


class tdc_Fluxes_Plotter(tdc_Data_Plotter):
    """
    Flux plotter
    """

    __plotstyle = { 'ns' : 'k:',
                    'lc' : 'k-' }

    __labels = { 'N'      : r'$\frac{dn}{dt}$',
                 'Energy' : r'$W$',
                 'J'      : r'$j$'  }

    def __init__(self, fluxes, xlabel=None,ylabel=None,idlabel=None):
        """
        fluxes -- list with fluxes to be plotted
        """
        # base class initialization is enough
        tdc_Data_Plotter.__init__(self,fluxes, xlabel,ylabel,idlabel)
        # labels -----------------------------
        if not xlabel:
            self.plot_xlabel  = r'$t$'
        if not ylabel:
            self.plot_ylabel  = self.__labels[fluxes[0].name]
        if not idlabel:
            self.plot_idlabel = self.data[0].name+' : '+self.data[0].calc_ids[0]
        # ------------------------------------
        # initialize lines
        self.lines = len(self.data)*[None]

    def plot(self,
             ax,
             semilog=True,
             **kwargs):
        """
        semilog
           <True> if True make semilog plot: t-linear, f-log scale,
                  if False  make linear plot: t,f-linear
        """
        for i,flux in enumerate(self.data):
            self.lines[i], = ax.semilogy( flux.t, flux.f,
                                          self.__plotstyle[flux.prefix],
                                          **kwargs)
        if semilog is True:
            ax.set_yscale('log')
