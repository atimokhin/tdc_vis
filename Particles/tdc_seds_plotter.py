from Common import tdc_Data_Plotter

class tdc_SEDs_Plotter(tdc_Data_Plotter):
    """
    This class is SED plotter


    """
    __plotstyle_separated = { 'Electrons' : ['k--'] ,
                              'Positrons' : ['k'] ,
                              'Pairs'     : ['k:']   }
    
    __plotstyle_u_combined = { 'Electrons' : ['b'] ,
                               'Positrons' : ['r'] ,
                               'Pairs'     : ['k']   }

    __plotstyle_d_combined = { 'Electrons' : ['b:'] ,
                               'Positrons' : ['r:'] ,
                               'Pairs'     : ['k:']   }


    def __init__(self, seds):
        """
        sets internal variables 
        seds -- xp data to be plotted
        """
        # base class initialization is enough
        tdc_Data_Plotter.__init__(self,seds)
        # plot label
        self.plot_ylabel = r'$p\frac{\partial{}n}{\partial{}p}$'
        self.plot_xlabel = r'$p$'
        self.plot_idlabel='SED : '+self.data[0].calc_id
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
           - None : plot SED for both ns and lc moving particles
                    on  the same plot, use color lines
           - 'ns' : plot SED for particles moving to the NS
                    use solid/dashe/dotted b/w lines
           - 'lc' : plot SED for particles moving to the LC
                    use solid/dashe/dotted b/w lines
        **kwargs goes to ax.plot(..)
        """
        # prefix and plotstyles
        if not prefix:
            plotstyle_u = self.__plotstyle_u_combined
            plotstyle_d = self.__plotstyle_d_combined
        else:
            plotstyle_u = self.__plotstyle_separated
            plotstyle_d = self.__plotstyle_separated
        
        for i,sed in enumerate(self.data):
            # SED for UPWARD moving particles
            if not prefix or prefix == 'lc':
                self.lines[i],   = ax.loglog(sed.P_bins, sed.dN_dlogPdX_u,
                                             *plotstyle_u[sed.name],
                                             drawstyle='steps-pre',
                                             nonposx='clip',nonposy='clip',
                                             **kwargs)
            # SED for DOWNWARD moving particles 
            if not prefix or prefix == 'ns':
                self.lines_d[i], = ax.loglog(sed.P_bins, sed.dN_dlogPdX_d,
                                             *plotstyle_d[sed.name],
                                             drawstyle='steps-pre',
                                             nonposx='clip',nonposy='clip',
                                             **kwargs)


    def animation_update(self,ax,i_ts):
        "Read and plot particles for animation at timestep# i_ts"
        pass



