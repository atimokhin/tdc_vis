from Common  import tdc_Manip_Plot_vs_X
from Fields  import tdc_Field_Data, tdc_EP_Density_Plotter


def tdc_plot_ep_density(calc_id, i_ts,
                        e_density_negative=True,
                        ylim=None, xlim=None,
                        print_id=False,
                        no_plot=False,
                        **kwargs):
    """
    calc_id
       calculation id name
    field_name
       name of the field to be plotted
    i_ts
       timeshot#
    Options:
    --------
    xlim 
    ylim
       <None>  axis limits
    e_density_negative
       <True> if True plots n_e and n_p
       as having different signs
    print_id
       <False> whether to put id label on the figure
    no_plot
       <False> if True do not call plot in Manipulator
       useful if additional plot modifications are required
    Returns:
    --------
    ()=> tdc_EP_Density_Manip
    """
    manip = tdc_EP_Density_Manip(calc_id, e_density_negative,**kwargs)
    manip.read(i_ts)
    if not no_plot:
        manip.plot(ylim, xlim, print_id)
    return manip


class tdc_EP_Density_Manip(tdc_Manip_Plot_vs_X):
    """
    Manipulator class for Field
    """

    def __init__(self, calc_id,
                 e_density_negative=True,
                 **kwargs):
        # fields 
        self.fe = tdc_Field_Data(calc_id, field_name='N',
                                 filename='prop_Electrons.h5')
        self.fp = tdc_Field_Data(calc_id, field_name='N',
                                 filename='prop_Positrons.h5')
        # set PLOTTER by calling base class constructor
        # with tdc_XPs_Plotter instanse
        tdc_Manip_Plot_vs_X.__init__(self, tdc_EP_Density_Plotter(self.fe, self.fp,
                                                                  e_density_negative),
                                     **kwargs)


    def __repr__(self):
        s =  'tdc_EP_Density_Manip:\n\n'
        s += '   calc_id = \"%s\"\n' % self.fe.calc_id
        s += '      i_ts = %d\n'     % self.i_ts
        return s
