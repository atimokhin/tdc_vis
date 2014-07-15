from  Particles.tdc_xps_tp_plotter import tdc_XPs_TP_Plotter
from pprint import *

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
        self.line_select=[None]*len(self.data)
        
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
#        for i, line in enumerate(self.line_select):
#            line.set_xdata(self.data[i].select_x)
#            line.set_ydata(self.data[i].select_y)
#            line.set_color('green')
#            ax.draw_artist(line)
        for i, xp in enumerate(self.data):
            select_x = []
            select_y = []
            for key in xp.select:
                select_x.append(xp.select[key][1])
                select_y.append(xp.select[key][2])
            self.line_select[i], = ax.plot(select_x, select_y, 'o', ms = 20, color = 'yellow', alpha = .7)
            ax.draw_artist(self.line_select[i])

    def set_animated(self,val):
        """
        Set animated property in all lines
        """
        tdc_XPs_TP_Plotter.set_animated(self,val=val)
