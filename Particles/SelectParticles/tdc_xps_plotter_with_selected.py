from  Particles.tdc_xps_tp_plotter import tdc_XPs_TP_Plotter

class tdc_XPs_TP_Plotter_with_Selected(tdc_XPs_TP_Plotter):
    """
    """
    
    def __init__(self, xps, tp=None, trail_dict=None, xlabel=None,ylabel=None,idlabel=None ):
        """
        """
        tdc_XPs_TP_Plotter.__init__(self,
                                    xps=xps,
                                    tp=tp,
                                    trail_dict=trail_dict,
                                    xlabel=xlabel,
                                    ylabel=ylabel,
                                    idlabel=idlabel)
        
    def plot(self,
             ax,
             symlog=True,
             linthreshy=5,
             **kwargs):
        """
        Plot particles into axes ax
        **kwargs goes to ax.plot(..)
        ----------
        Options:
        ----------
        symlog
           <True>/False --  whether to plot in semi-logarithmic scale
        linthreshy   
           <5>     The range (-x, x) within which the plot is linear
        """
        tdc_XPs_TP_Plotter.plot(self,
                                ax=ax,
                                symlog=symlog,
                                linthreshy=linthreshy,
                                **kwargs)


    def replot(self,ax):
        """
        Plot particles for animation at timestep# i_ts
        """
        tdc_XPs_TP_Plotter.replot(self,ax=ax)


    def set_animated(self,val):
        """
        Set animated property in all lines
        """
        tdc_XPs_TP_Plotter.set_animated(self,val=val)
