from Common import tdc_Data_vs_X_Plotter

class tdc_XPs_Plotter(tdc_Data_vs_X_Plotter):
    """
    This class is simple phase space portrait plotter
    Members:
    xp         -- field
    plot_label -- TeX string label used for plot annotations
    line       -- Line artists with plotted field
    """

    __plotstyle = { 'Electrons' : ['.b'] ,
                    'Positrons' : ['.r'] ,
                    'Pairs'     : ['.k']   }

    __plotlabel = { 'Electrons' : r'$p_{-}$' ,
                    'Positrons' : r'$p_{+}$' ,
                    'Pairs'     : r'$p_\gamma$'   }


    def __init__(self, xps):
        """
        sets internal variables 
        xps
           XP data to be plotted
        """
        # base class initialization is enough
        tdc_Data_vs_X_Plotter.__init__(self,xps)
        # set y-label:
        # if only one particle kind is plotted -- set specific label
        # if more than one -- set it to 'p'
        if len(self.data)>1:
            self.plot_ylabel=r'$p$'
        else:
            self.plot_ylabel=self.__plotlabel[xps[0].name]
        # id label
        self.plot_idlabel='XP : ' + self.data[0].calc_id


    def plot(self,ax,**kwargs):
        """
        Plot particles into axes ax
        **kwargs goes to ax.plot(..)
        """
        for i,xp in enumerate(self.data):
            self.lines[i], = ax.plot(xp.x, xp.p,
                                     *self.__plotstyle[xp.name],
                                     markersize=.5,
                                     **kwargs)
            #ax.set_yscale('symlog',linthreshy=1e2)


    def animation_update(self,ax,i_ts):
        "Read and plot particles for animation at timestep# i_ts"
        self.read(i_ts)
        for i,line in enumerate(self.lines):
            line.set_xdata(self.data[i].x)
            line.set_ydata(self.data[i].p)
        for line in self.lines:    
            ax.draw_artist(line)

