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
        self.line_select=[None]*2*len(self.data)
        self.marker_size = 20
        #keeps track of sensitivity of pick events
        self.lines_epsilon = 0
        self.line_select_epsilon = 20
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
        tdc_XPs_TP_Plotter.plot(self,
                                ax=ax,
                                symlog=symlog,
                                linthreshy=linthreshy,
                                **kwargs)
        for i in range(0,len(self.data)):
            select_x = []
            select_y = []
            self.line_select[i], = ax.plot( select_x, select_y,'o', 
                                            picker = self.line_select_epsilon, 
                                            ms = self.marker_size, 
                                            color = 'green',
                                            alpha = .6)
#        for i in range(len(self.data),2*len(self.data)):
#            select_x = []
#            select_y = []
#            self.line_select[i], = ax.plot( select_x, select_y,'-',
#                                            ms = self.marker_size, 
#                                            color = 'black', linewidth = 5,
#                                            alpha = .9)
        

    def replot(self, ax):
        """
        Plot particles for animation at timestep# i_ts
        """
        tdc_XPs_TP_Plotter.replot(self,ax=ax)
            
        for i, xp in enumerate(self.data):            
            select_x = []
            select_y = []
#            old_x = self.line_select[i].get_xdata()
#            old_y = self.line_select[i].get_ydata()
            for key in xp.select:
                select_x.append(xp.select[key].x)
                select_y.append(xp.select[key].p)
            self.line_select[i].set_xdata(select_x)
            self.line_select[i].set_ydata(select_y)
            ax.draw_artist(self.line_select[i])
#            select_x.extend(old_x)
#            select_y.extend(old_y)
#            self.line_select[i+4].set_xdata(select_x)
#            self.line_select[i+4].set_ydata(select_y)
#            ax.draw_artist(self.line_select[i+4])
        

    def resize_marker(self, ax, marker_size):
        self.marker_size = marker_size
        print "Resize marker to %i at next frame" %(marker_size)
        for i in range(0,len(self.line_select)):
            self.line_select[i].set_markersize(marker_size)
            ax.draw_artist(self.line_select[i])
    def change_sensitivity(self,selecting):
        if selecting:
            self.lines_epsilon=self.lines[0].get_pickradius()
            self.line_select_epsilon = 0
        else:
            self.lines_epsilon = 0
            self.line_select_epsilon = self.marker_size
        for i in range(0,len(self.lines)):
            self.lines[i].set_picker(self.lines_epsilon)
        for i in range(0,len(self.line_select)):
                self.line_select[i].set_picker(self.line_select_epsilon)
    def set_animated(self,val):
        """
        Set animated property in all lines
        """
        tdc_XPs_TP_Plotter.set_animated(self,val=val)
