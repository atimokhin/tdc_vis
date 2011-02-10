from Common  import tdc_Manip_Plot_vs_X
from Fields  import tdc_Field_Data, tdc_Fields_Plotter


def tdc_plot_field(calc_id,
                   i_ts,
                   field_name,
                   ylim=None,
                   xlim=None,
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
    print_id
       <False> whether to put id label on the figure
    no_plot
       <False> if True do not call plot in Manipulator
       useful if additional plot modifications are required
    Returns:
    --------
    ()=> tdc_Field_Manip
    """
    manip = tdc_Field_Manip(calc_id, field_name,**kwargs)
    manip.read(i_ts)
    if not no_plot:
        manip.plot(ylim, xlim, print_id)
    return manip


class tdc_Field_Manip(tdc_Manip_Plot_vs_X):
    """
    Manipulator class for Field
    """

    def __init__(self, calc_id, field_name,**kwargs):
        # field 
        self.field   = tdc_Field_Data(calc_id, field_name,**kwargs)
        # set PLOTTER by calling base class constructor
        # with tdc_XPs_Plotter instanse
        tdc_Manip_Plot_vs_X.__init__(self, tdc_Fields_Plotter(self.field),**kwargs )


    def __repr__(self):
        s =  'tdc_Field_Manip:\n\n'
        s += '   calc_id = \"%s\"\n' % self.field.calc_id
        s += 'field name = \"%s\"\n' % self.field.name
        s += '      i_ts = %d\n'     % self.i_ts
        s += '      time = %s\n'     % self.field.timetable
        return s
