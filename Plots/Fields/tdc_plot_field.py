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
    manip = tdc_Field_Manip(**kwargs)
    manip.setup_from_data(calc_id, field_name,**kwargs)
    manip.read(i_ts)
    if not no_plot:
        manip.plot(ylim, xlim, print_id)
    return manip


def tdc_plot_field_restored(filename,
                            ylim=None,
                            xlim=None,
                            print_id=False,
                            no_plot=False,
                            **kwargs):
    """
    filename
       pickle file name is 'filename.pickle'
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
    # create Manip
    manip = tdc_Field_Manip(**kwargs)
    manip.restore(filename)
    if not no_plot:
        manip.plot(ylim, xlim, print_id)
    return manip



class tdc_Field_Manip(tdc_Manip_Plot_vs_X):
    """
    Manipulator class for Field
    """
    
    def __init__(self,**kwargs):
        tdc_Manip_Plot_vs_X.__init__(self,**kwargs)
        # Field DATA <<<<<<<
        self.field=None

    def setup_from_data(self,
                        calc_id,
                        field_name,
                        **kwargs):
        """
        setup Manip by reading the original data file
        """
        # Field <<<<<<<
        self.field = tdc_Field_Data(calc_id, field_name,**kwargs)
        # set PLOTTER by calling base class method
        self.set_plotter( tdc_Fields_Plotter(self.field) )
        
    def restore(self,
                filename):
        """
        setup Manip by reading the pickle'd data dumped
        by Manip called before
        """
        import pickle
        # set restored_from_dump flag so the data cannot be read again
        self.restored_from_dump=True
        # Field <<<<<<<
        fields = pickle.load( open(filename+'.pickle','r') )
        self.field = fields[0]
        # i_ts
        self.i_ts = self.field.i_ts
        # set PLOTTER by calling base class method
        self.set_plotter( tdc_Fields_Plotter( self.field ) )

    def __repr__(self):
        s = self._manip_name('tdc_Field_Manip')
        s += '   calc_id = \"%s\"\n' % self.field.calc_id
        s += 'field name = \"%s\"\n' % self.field.name
        s += '      i_ts = %d\n'     % self.i_ts
        s += '      time = %s\n'     % self.field.timetable
        return s
