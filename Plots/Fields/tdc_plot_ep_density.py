from Common  import tdc_Manip_Plot_vs_X
from Fields  import tdc_Field_Data, tdc_EP_Density_Plotter


def tdc_plot_ep_density(calc_id,
                        i_ts,
                        e_density_negative=True,
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
    manip = tdc_EP_Density_Manip(**kwargs)
    manip.setup_from_data(calc_id, e_density_negative,**kwargs)
    manip.read(i_ts)
    if not no_plot:
        manip.plot(ylim, xlim, print_id)
    return manip


def tdc_plot_ep_density_restored(filename,
                                 e_density_negative=True,
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
    # create Manip
    manip = tdc_EP_Density_Manip(**kwargs)
    manip.restore(filename,e_density_negative)
    if not no_plot:
        manip.plot(ylim, xlim, print_id)
    return manip



class tdc_EP_Density_Manip(tdc_Manip_Plot_vs_X):
    """
    Manipulator class for Field
    """
    def __init__(self,**kwargs):
        tdc_Manip_Plot_vs_X.__init__(self,**kwargs)
        # Field DATA <<<<<<<
        self.fe=None
        self.fp=None
        
    def setup_from_data(self,
                        calc_id,
                        e_density_negative=True,
                        **kwargs):
        # fields 
        self.fe = tdc_Field_Data(calc_id,
                                 field_name='N',
                                 filename='prop_Electrons.h5')
        self.fp = tdc_Field_Data(calc_id,
                                 field_name='N',
                                 filename='prop_Positrons.h5')
        # set PLOTTER by calling base class method
        self.set_plotter( tdc_EP_Density_Plotter(self.fe,
                                                 self.fp,
                                                 e_density_negative)
                          )

    def restore(self,
                filename,
                e_density_negative=True):
        """
        setup Manip by reading the pickle'd data dumped
        by Manip called before
        """
        import pickle
        # set restored_from_dump flag so the data cannot be read again
        self.restored_from_dump=True
        # Fields <<<<<<<
        fields = pickle.load( open(filename+'.pickle','r') )
        self.fe = fields['fe']
        self.fp = fields['fp']
        # i_ts
        self.i_ts = self.fe.i_ts
        # set PLOTTER by calling base class method
        self.set_plotter( tdc_EP_Density_Plotter(self.fe,
                                                 self.fp,
                                                 e_density_negative)
                          )
        
    def dump_data(self,filename):
        """
        get pure data from plotter and dump it into the pickle file filename.pickle 
        """
        import pickle
        dump_dict={}
        dump_dict['fe'] = self.fe.get_pure_data_copy()
        dump_dict['fp'] = self.fp.get_pure_data_copy()
        pickle.dump( dump_dict, open(filename+'.pickle','w') )

    def __repr__(self):
        s = self._manip_name('tdc_EP_Density_Manip')
        s += '   calc_id = \"%s\"\n' % self.fe.calc_id
        s += '      i_ts = %d\n'     % self.i_ts
        return s
