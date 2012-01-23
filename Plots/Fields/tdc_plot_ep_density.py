from Common_Data_Plot  import tdc_Manip_Plot_vs_X
from Fields   import tdc_Field_Data, tdc_EP_Density_Plotter, tdc_EPG_Density_Plotter, tdc_EPGP_Density_Plotter


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
                                 dump_id,
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
    manip.restore(filename,dump_id,e_density_negative)
    if not no_plot:
        manip.plot(ylim, xlim, print_id)
    return manip



def tdc_plot_epg_density(calc_id,
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
    ()=> tdc_EPG_Density_Manip
    """
    manip = tdc_EPG_Density_Manip(**kwargs)
    manip.setup_from_data(calc_id, e_density_negative,**kwargs)
    manip.read(i_ts)
    if not no_plot:
        manip.plot(ylim, xlim, print_id)
    return manip


def tdc_plot_epg_density_restored(filename,
                                  dump_id,
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
    ()=> tdc_EPG_Density_Manip
    """
    # create Manip
    manip = tdc_EPG_Density_Manip(**kwargs)
    manip.restore(filename,dump_id,e_density_negative)
    if not no_plot:
        manip.plot(ylim, xlim, print_id)
    return manip



def tdc_plot_epgp_density(calc_id,
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
    ()=> tdc_EPGP_Density_Manip
    """
    manip = tdc_EPGP_Density_Manip(**kwargs)
    manip.setup_from_data(calc_id, e_density_negative,**kwargs)
    manip.read(i_ts)
    if not no_plot:
        manip.plot(ylim, xlim, print_id)
    return manip


def tdc_plot_epgp_density_restored(filename,
                                   dump_id,
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
    ()=> tdc_EPGP_Density_Manip
    """
    # create Manip
    manip = tdc_EPGP_Density_Manip(**kwargs)
    manip.restore(filename,dump_id,e_density_negative)
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
                dump_id,
                e_density_negative=True):
        """
        setup Manip by reading the pickle'd data dumped
        by Manip called before
        """
        import pickle
        from   Auxiliary import tdc_Filenames
        # set restored_from_dump flag so the data cannot be read again
        self.restored_from_dump=True
        # Fields <<<<<<<
        # full file name of the file with manipulator dump
        filename=tdc_Filenames().get_full_vis_filename(dump_id, filename+'.pickle')
        fields = pickle.load( open(filename,'r') )
        self.fe = fields['fe']
        self.fp = fields['fp']
        # i_ts
        self.i_ts = self.fe.i_ts
        # set PLOTTER by calling base class method
        self.set_plotter( tdc_EP_Density_Plotter(self.fe,
                                                 self.fp,
                                                 e_density_negative)
                          )
        
    def dump_data(self,filename,dump_id):
        """
        get pure data from plotter and dump it into the pickle file filename.pickle 
        """
        import pickle
        from   Auxiliary import tdc_Filenames
        dump_dict={}
        dump_dict['fe'] = self.fe.get_pure_data_copy()
        dump_dict['fp'] = self.fp.get_pure_data_copy()
        # full file name of the file with manipulator dump
        filename=tdc_Filenames().get_full_vis_filename(dump_id, filename+'.pickle')
        pickle.dump( dump_dict, open(filename,'w') )
        print '\nContent dumped in "%s" \n' % filename

    def __repr__(self):
        s = self._manip_name('tdc_EP_Density_Manip')
        s += '   calc_id = \"%s\"\n' % self.fe.calc_id
        s += '      i_ts = %d\n'     % self.i_ts
        return s



class tdc_EPG_Density_Manip(tdc_Manip_Plot_vs_X):
    """
    Manipulator class for Field
    """
    def __init__(self,**kwargs):
        tdc_Manip_Plot_vs_X.__init__(self,**kwargs)
        # Field DATA <<<<<<<
        self.fe=None
        self.fp=None
        self.fg=None
        
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
        self.fg = tdc_Field_Data(calc_id,
                                 field_name='N',
                                 filename='prop_Pairs.h5')
        # set PLOTTER by calling base class method
        self.set_plotter( tdc_EPG_Density_Plotter(self.fe,
                                                  self.fp,
                                                  self.fg,
                                                  e_density_negative)
                          )

    def restore(self,
                filename,
                dump_id,
                e_density_negative=True):
        """
        setup Manip by reading the pickle'd data dumped
        by Manip called before
        """
        import pickle
        from   Auxiliary import tdc_Filenames
        # set restored_from_dump flag so the data cannot be read again
        self.restored_from_dump=True
        # Fields <<<<<<<
        # full file name of the file with manipulator dump
        filename=tdc_Filenames().get_full_vis_filename(dump_id, filename+'.pickle')
        fields = pickle.load( open(filename,'r') )
        self.fe = fields['fe']
        self.fp = fields['fp']
        self.fg = fields['fg']
        # i_ts
        self.i_ts = self.fe.i_ts
        # set PLOTTER by calling base class method
        self.set_plotter( tdc_EPG_Density_Plotter(self.fe,
                                                  self.fp,
                                                  self.fg,
                                                  e_density_negative)
                          )
        
    def dump_data(self,filename,dump_id):
        """
        get pure data from plotter and dump it into the pickle file filename.pickle 
        """
        import pickle
        from   Auxiliary import tdc_Filenames
        dump_dict={}
        dump_dict['fe'] = self.fe.get_pure_data_copy()
        dump_dict['fp'] = self.fp.get_pure_data_copy()
        dump_dict['fg'] = self.fg.get_pure_data_copy()
        # full file name of the file with manipulator dump
        filename=tdc_Filenames().get_full_vis_filename(dump_id, filename+'.pickle')
        pickle.dump( dump_dict, open(filename,'w') )
        print '\nContent dumped in "%s" \n' % filename

    def __repr__(self):
        s = self._manip_name('tdc_EPG_Density_Manip')
        s += '   calc_id = \"%s\"\n' % self.fe.calc_id
        s += '      i_ts = %d\n'     % self.i_ts
        return s



class tdc_EPGP_Density_Manip(tdc_Manip_Plot_vs_X):
    """
    Manipulator class for Field
    """
    def __init__(self,**kwargs):
        tdc_Manip_Plot_vs_X.__init__(self,**kwargs)
        # Field DATA <<<<<<<
        self.fe=None
        self.fp=None
        self.fg=None
        self.fpr=None
        
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
        self.fg = tdc_Field_Data(calc_id,
                                 field_name='N',
                                 filename='prop_Pairs.h5')
        self.fpr= tdc_Field_Data(calc_id,
                                 field_name='N',
                                 filename='prop_Protons.h5')
        # set PLOTTER by calling base class method
        self.set_plotter( tdc_EPGP_Density_Plotter(self.fe,
                                                   self.fp,
                                                   self.fg,
                                                   self.fpr,
                                                   e_density_negative)
                          )

    def restore(self,
                filename,
                dump_id,
                e_density_negative=True):
        """
        setup Manip by reading the pickle'd data dumped
        by Manip called before
        """
        import pickle
        from   Auxiliary import tdc_Filenames
        # set restored_from_dump flag so the data cannot be read again
        self.restored_from_dump=True
        # Fields <<<<<<<
        # full file name of the file with manipulator dump
        filename=tdc_Filenames().get_full_vis_filename(dump_id, filename+'.pickle')
        fields = pickle.load( open(filename,'r') )
        self.fe = fields['fe']
        self.fp = fields['fp']
        self.fg = fields['fg']
        self.fpr = fields['fpr']
        # i_ts
        self.i_ts = self.fe.i_ts
        # set PLOTTER by calling base class method
        self.set_plotter( tdc_EPGP_Density_Plotter(self.fe,
                                                   self.fp,
                                                   self.fg,
                                                   self.fpr,
                                                   e_density_negative)
                          )
        
    def dump_data(self,filename,dump_id):
        """
        get pure data from plotter and dump it into the pickle file filename.pickle 
        """
        import pickle
        from   Auxiliary import tdc_Filenames
        dump_dict={}
        dump_dict['fe'] = self.fe.get_pure_data_copy()
        dump_dict['fp'] = self.fp.get_pure_data_copy()
        dump_dict['fg'] = self.fg.get_pure_data_copy()
        dump_dict['fpr'] = self.fpr.get_pure_data_copy()
        # full file name of the file with manipulator dump
        filename=tdc_Filenames().get_full_vis_filename(dump_id, filename+'.pickle')
        pickle.dump( dump_dict, open(filename,'w') )
        print '\nContent dumped in "%s" \n' % filename

    def __repr__(self):
        s = self._manip_name('tdc_EPGP_Density_Manip')
        s += '   calc_id = \"%s\"\n' % self.fe.calc_id
        s += '      i_ts = %d\n'     % self.i_ts
        return s


