from tdc_xps_plotter  import tdc_XPs_Plotter

import TrackParticles
from TrackParticles  import tdc_TP_Plotter

class tdc_XPs_TP_Plotter(tdc_XPs_Plotter):
    """
    Plotter for particle phase space portrait with trajectories of
    tracked particles on it

    It combines functionality of
    tdc_XPs_Plotter and tdc_TP_Plotter
    """

    def __init__(self, xps, tp=None, trail_dict=None, xlabel=None,ylabel=None,idlabel=None, trace_particles = None):
        """
        xps
           XP data to be plotted
        tp
           TP (Tracked Particles) data to be plotted
           if None <default> no tracked particles will be plotted
        trail
           Length of the particle trail
           If None <default> -- default length will be used
        """
        # base class initialization
        tdc_XPs_Plotter.__init__(self,xps, xlabel,ylabel,idlabel)
        # if tp is not None, initialize tpp
        if tp:
            self.tpp=tdc_TP_Plotter(tp,trail_dict)
        else:
            self.tpp=None

    def read(self,i_ts,**kwargs):
        "Read data at i_ts timeshot"
        tdc_XPs_Plotter.read(self,i_ts,**kwargs)
        if self.tpp:
            self.tpp.read(i_ts,**kwargs)

    def plot(self,ax,**kwargs):
        "Plot particles into axes ax"
        tdc_XPs_Plotter.plot(self,ax,**kwargs)
        if self.tpp:
            self.tpp.plot(ax,**kwargs)

    def replot(self,ax):
        """
        Replot particles
        """
        tdc_XPs_Plotter.replot(self,ax)
        if self.tpp:
            self.tpp.replot(ax)

    def update_plot(self,ax):
        """
        Plot particles for animation at timestep# i_ts
        """
        self.replot(ax)

    def set_animated(self,val):
        "Set animated property of the each plot"
        tdc_XPs_Plotter.set_animated(self,val)
        if self.tpp:
            self.tpp.set_animated(val)

    def animation_update(self,ax,i_ts):
        "Read and plot particles for animation at timestep# i_ts"
        tdc_XPs_Plotter.animation_update(self,ax,i_ts)
        if self.tpp:
            self.tpp.animation_update(ax,i_ts)

