from numpy import *

from Common_Data_Plot import tdc_Data_Plotter

class tdc_FMCI_MP_Plotter(tdc_Data_Plotter):
    """
    Plots FMCI_XP as particles with sizes proportional to their weights
    """
    __default_plot_ylabel = { 'Electrons' : r'$p_{-}$' ,
                              'Positrons' : r'$p_{+}$' ,
                              'Protons'   : r'$p_{p}$',
                              'Pairs'     : r'$p_\gamma$'   }
    
    def __init__(self, fmci_MPs, xlabel=None,ylabel=None,idlabel=None):
        """
        """
        # base class initialization is enough
        tdc_Data_Plotter.__init__(self,fmci_MPs, xlabel,ylabel,idlabel)
        # labels -----------------------
        # xlabel
        if not xlabel:
            self.plot_xlabel = r'$x$'
        else:
            self.plot_xlabel = xlabel
        # ylabel: if only one particle kind is plotted -- set
        #         specific label if more than one -- set to 'p'
        if not ylabel:
            if len(self.data)>1:
                self.plot_ylabel=r'$p$'
            else:
                self.plot_ylabel=self.__default_plot_ylabel[self.data[0].name]
        # idlabel
        if not idlabel:
            self.plot_idlabel='FMCI_MPs:' + self.data[0].calc_id
        # ---------------------------------
        # initialize lines
        self.lines = len(self.data)*[None]
        

    def plot(self,
             ax,            
             symlog=True,
             linthreshy=5,
             **kwargs):
        """
        Plot particles with sizes representing their statistical weight
        """
        for i,mp in enumerate(self.data):
            self.lines[i] =  ax.scatter(mp.x,mp.p, 
                                        s=mp.markersize, 
                                        c='b', marker='o', cmap=None, norm=None,
                                        vmin=None, vmax=None, alpha=None, linewidths=None,
                                        verts=None, edgecolors ='none',
                                        **kwargs)
        # make scaling semi-logatithmic if asked
        if symlog:
            ax.set_yscale('symlog',linthreshy=linthreshy,subsy=[1,10])

                
