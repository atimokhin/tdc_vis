from Common_Data_Plot import tdc_Data_Plotter

class tdc_SEDs_Plotter(tdc_Data_Plotter):
    """
    This class is SED plotter
    """
    __plotstyle_separated = { 'Electrons' : ['b'] ,
                              'Positrons' : ['r--'] ,
                              'Pairs'     : ['k:']   }
    
    __plotstyle_u_combined = { 'Electrons' : ['b'] ,
                               'Positrons' : ['r'] ,
                               'Pairs'     : ['k']   }

    __plotstyle_d_combined = { 'Electrons' : ['b:'] ,
                               'Positrons' : ['r:'] ,
                               'Pairs'     : ['k:']   }

    
    def __init__(self, seds, xlabel=None,ylabel=None,idlabel=None):
        """
        sets internal variables 
        seds -- xp data to be plotted
        """
        # base class initialization is enough
        tdc_Data_Plotter.__init__(self,seds, xlabel,ylabel,idlabel)
        # plot labels ---------------------
        if not ylabel:
            self.plot_ylabel = r'$p\frac{\partial{}n}{\partial{}p}$'
            self.plot_ylabel_latex = r'$\displaystyle{}p\:\frac{\partial\!n}{\partial{}\!p}$'
        if not idlabel:
            self.plot_idlabel='SED:'+self.data[0].calc_id
        # these will be used to choose the right xlabel
        self.plot_xlabel_default = r'$p$'
        self.plot_xlabel_total   = r'$|p|$'
        # ---------------------------------
        # initialize lines
        self.lines = len(self.data)*[None]
        # additional lines for downward moving particle spectra
        self.lines_d=len(self.data)*[None]
        # xmin/xmax
        self.xmin = self.data[0].P_bins[0]
        self.xmax = self.data[0].P_bins[-1]
            

    def plot(self,ax,prefix=None,**kwargs):
        """
        Plot SEDs into axes ax
        Arguments:
        ----------
        ax
          axes
        prefix: < 'ns' | 'lc' | None >
          depending on prefix plot:
           - None    : plot SED for both ns and lc moving particles
                       on  the same plot, use color lines
           - 'ns'    : plot SED for particles moving to the NS
                       use solid/dashe/dotted b/w lines
           - 'lc'    : plot SED for particles moving to the LC
                       use solid/dashe/dotted b/w lines
           - 'total' : plot SED for particles all particles as a function
                       of |p|, summing dN_dlogPdX_u+dN_dlogPdX_u
        **kwargs goes to ax.plot(..)
        """
        # prefix and plotstyles
        if prefix is None or prefix=='total':
            plotstyle_u = self.__plotstyle_u_combined
            plotstyle_d = self.__plotstyle_d_combined
        else:
            plotstyle_u = self.__plotstyle_separated
            plotstyle_d = self.__plotstyle_separated
        
        for i,sed in enumerate(self.data):
            # SED for UPWARD moving particles
            if prefix is None or prefix == 'lc':
                self.lines[i],   = ax.loglog(sed.P_bins, sed.dN_dlogPdX_u,
                                             *plotstyle_u[sed.name],
                                             drawstyle='steps-pre',
                                             nonposx='clip',nonposy='clip',
                                             **kwargs)
            # SED for DOWNWARD moving particles 
            if prefix is None or prefix == 'ns':
                self.lines_d[i], = ax.loglog(sed.P_bins, sed.dN_dlogPdX_d,
                                             *plotstyle_d[sed.name],
                                             drawstyle='steps-pre',
                                             nonposx='clip',nonposy='clip',
                                             **kwargs)
            # total SED
            if prefix == 'total':
                self.lines[i],   = ax.loglog(sed.P_bins, sed.dN_dlogPdX_u+sed.dN_dlogPdX_d,
                                             *plotstyle_u[sed.name],
                                             drawstyle='steps-pre',
                                             nonposx='clip',nonposy='clip',
                                             **kwargs)
                self.plot_xlabel = self.plot_xlabel_total
            else:
                self.plot_xlabel = self.plot_xlabel_default


    def animation_update(self,ax,i_ts):
        "Read and plot particles for animation at timestep# i_ts"
        pass



