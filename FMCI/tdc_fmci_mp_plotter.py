from numpy import *

from ATvis.Common_Data_Plot import AT_Data_Plotter

class tdc_FMCI_MP_Plotter(AT_Data_Plotter):
    """
    Plots FMCI_XP as particles with sizes proportional to their weights
    """
    __plotstyle = { 'Electrons' : {'color':'b','marker':'o'},
                    'Positrons' : {'color':'r','marker':'o'},
                    'Protons'   : {'color':'m','marker':'o'},  
                    'Pairs'     : {'color':'k','marker':'o'}  }

    __default_plot_ylabel = { 'Electrons' : r'$p_{-}$' ,
                              'Positrons' : r'$p_{+}$' ,
                              'Protons'   : r'$p_{p}$',
                              'Pairs'     : r'$p_\gamma$'   }
    
    def __init__(self, fmci_MPs, xlabel=None,ylabel=None,idlabel=None):
        """
        """
        # base class initialization is enough
        AT_Data_Plotter.__init__(self,fmci_MPs, xlabel,ylabel,idlabel)
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
        plot_kwargs={}
        for i,mp in enumerate(self.data):
            plot_kwargs.update(self.__plotstyle[mp.name])
            plot_kwargs.update(kwargs)            
            self.lines[i] = ax.scatter(mp.x,mp.p, 
                                       s=mp.markersize, 
                                       cmap=None, norm=None,
                                       vmin=None, vmax=None, alpha=None, linewidths=None,
                                       verts=None, edgecolors ='none',
                                       **plot_kwargs)
        # make scaling semi-logatithmic if asked
        if symlog:
            ax.set_yscale('symlog',linthreshy=linthreshy,subsy=[1,10])

    def replot(self,ax):
        """
        Plot particles for animation at timestep# i_ts
        """
        self.plot(ax)
        for line in self.lines:    
            ax.draw_artist(line)

    def update_plot(self,ax):
        """
        Plot particles for animation at timestep# i_ts
        """
        self.replot(ax)

    def set_animated(self,val):
        """
        Set animated property in all lines
        """
        for line in self.lines:
            line.set_animated(val)
                
