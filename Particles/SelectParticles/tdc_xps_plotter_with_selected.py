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
        self.marker_size = 20
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
        #sets up empty line_select lines
        for i in range(0,len(self.data)):
            select_x = []
            select_y = []
            self.line_select[i], = ax.plot(select_x, select_y, 'o', ms = self.marker_size, color = 'green', alpha = .7
            )
        tdc_XPs_TP_Plotter.plot(self,
                                ax=ax,
                                symlog=symlog,
                                linthreshy=linthreshy,
                                **kwargs)

    def replot(self, ax):
        """
        Plot particles for animation at timestep# i_ts
        """
        for i, xp in enumerate(self.data):            
            select_x = []
            select_y = []
            for key in xp.select:
                select_x.append(xp.select[key].x)
                select_y.append(xp.select[key].p)
            self.line_select[i].set_xdata(select_x)
            self.line_select[i].set_ydata(select_y)
            ax.draw_artist(self.line_select[i])
        tdc_XPs_TP_Plotter.replot(self,ax=ax)

    def resize_marker(self, ax, marker_size):
        self.marker_size = marker_size
        print "Resize marker to %i at next frame" %(marker_size)
        for i in range(0,len(self.line_select)):
            self.line_select[i].set_markersize(marker_size)
            ax.draw_artist(self.line_select[i])
    def set_animated(self,val):
        """
        Set animated property in all lines
        """
        tdc_XPs_TP_Plotter.set_animated(self,val=val)
