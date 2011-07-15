from Common import tdc_Data_vs_X_Plotter

class tdc_XPs_Plotter(tdc_Data_vs_X_Plotter):
    """
    This class is simple phase space portrait plotter
    Members:
    xp         -- field
    plot_label -- TeX string label used for plot annotations
    line       -- Line artists with plotted field
    """

    __plotstyle = { 'Electrons' : {'linestyle':'None','color':'b','marker':'.','markersize':1},
                    'Positrons' : {'linestyle':'None','color':'r','marker':'.','markersize':1},
                    'Protons'   : {'linestyle':'None','color':'m','marker':'.','markersize':4},  
                    'Pairs'     : {'linestyle':'None','color':'k','marker':'.','markersize':1}   }

    __plotlabel = { 'Electrons' : r'$p_{-}$' ,
                    'Positrons' : r'$p_{+}$' ,
                    'Protons'   : r'$p_{p}$',
                    'Pairs'     : r'$p_\gamma$'   }


    def __init__(self, xps):
        """
        sets internal variables 
        xps
           XP data to be plotted
        """
        # base class initialization is enough
        tdc_Data_vs_X_Plotter.__init__(self,xps)
        # X coordinates are read at every timestep and must be
        # renormalized
        self.new_x_at_every_read_flag = True
        # set y-label:
        # if only one particle kind is plotted -- set specific label
        # if more than one -- set it to 'p'
        if len(self.data)>1:
            self.plot_ylabel=r'$p$'
        else:
            self.plot_ylabel=self.__plotlabel[xps[0].name]
        # id label
        self.plot_idlabel='XP : ' + self.data[0].calc_id
        # initialize lines
        self.lines = len(self.data)*[None]

    def change_default_plotstyle(self,particle_name, **kwargs):
        self.__plotstyle[particle_name].update(kwargs) 

    def plot(self,
             ax,
             symlog=False,
             linthreshy=5,
             **kwargs):
        """
        Plot particles into axes ax
        **kwargs goes to ax.plot(..)
        ----------
        Options:
        ----------
        symlog
           <False>/True --  whether to plot in semi-logarithmic scale
        linthreshy   
           <1>     The range (-x, x) within which the plot is linear
        """
        plot_kwargs={}
        for i,xp in enumerate(self.data):
            plot_kwargs.update(self.__plotstyle[xp.name])
            plot_kwargs.update(kwargs)            
            self.lines[i], = ax.plot(xp.x, xp.p,
                                     **plot_kwargs)
            # make scaling semi-logatithmic if asked
            if symlog:
                ax.set_yscale('symlog',linthreshy=linthreshy)
        tdc_Data_vs_X_Plotter.plot(self,ax,**kwargs)


    def replot(self,ax):
        """
        Plot particles for animation at timestep# i_ts
        """
        for i,line in enumerate(self.lines):
            line.set_xdata(self.data[i].x)
            line.set_ydata(self.data[i].p)
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
