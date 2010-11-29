from Common  import tdc_Manip_Plot_vs_X

from Particles.TrackParticles.tdc_tp_plotter  import tdc_TP_Plotter


def tdc_plot_tp(tp, i_ts,
                trail_dict=None,
                ylim=None, xlim=None,
                print_id=False,
                no_plot=False,
                **kwargs):
    """
    tp
       TP_Data instance
    i_ts
       timeshot#
    Options:
    --------
    trail_dict
       <None> trail_dict
    xlim 
    ylim
       <None>  axis limits
    print_id
       <False> whether to put id label on the figure
    no_plot
       <False> if True do not call plot in Manipulator
       useful if additional plot modifications are required
    Returns:
    --------
    ()=> tdc_TP_Manip
    """

    manip = tdc_TP_Manip(tp, trail_dict=trail_dict, **kwargs)
    manip.read(i_ts)
    if not no_plot:
        manip.plot(ylim, xlim, print_id=print_id)
    return manip




class tdc_TP_Manip(tdc_Manip_Plot_vs_X):
    """
    Manipulator class for TP
    """

    def __init__(self, tp,
                 trail_dict=None,
                 **kwargs):
        self.tp=tp
        # set PLOTTER by calling base class constructor
        # with tdc_TP_Plotter instanse
        tdc_Manip_Plot_vs_X.__init__(self,
                                     tdc_TP_Plotter(tp=self.tp, trail_dict=trail_dict),
                                     **kwargs )


    def __repr__(self):
        return self.tp.__repr__()
