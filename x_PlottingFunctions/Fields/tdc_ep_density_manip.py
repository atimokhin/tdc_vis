from Common_Data_Plot  import tdc_Manip_Plot_vs_X
from Fields            import tdc_Field_Data, tdc_EP_Density_Plotter, tdc_EPG_Density_Plotter, tdc_EPGP_Density_Plotter


class tdc_EP_Density_Manip(tdc_Manip_Plot_vs_X):
    """
    Manipulator class for Density plots of E[lectrons] P[ositrons]
    """
    
    def __init__(self,fig_param=None):
        tdc_Manip_Plot_vs_X.__init__(self,fig_param)
        # Field DATA <<<<<<<
        self.fe=None
        self.fp=None

        
    @staticmethod
    def init_from_data(calc_id,
                        i_ts,
                        e_density_negative=True,
                        fig_param=None):
        """
        Setup Manip by reading original data

        calc_id
           calculation id name
        i_ts
           timeshot#
        --------
        Options:
        --------
        e_density_negative
        fig_param
        --------
        """
        manip=tdc_EP_Density_Manip(fig_param)
        manip.read_from_data(calc_id, i_ts, e_density_negative=e_density_negative)
        return manip


    @staticmethod
    def init_from_dump(filename,
                        dump_id,
                        e_density_negative=True,
                        fig_param=None):
        """
        Setup Manip from dumped data
        filename
           pickle file name is 'filename.pickle'
        """
        manip=tdc_EP_Density_Manip(fig_param)
        manip.read_from_dump(filename, dump_id, e_density_negative=e_density_negative)
        return manip

    
    def read_from_data(self,
                       calc_id,
                       i_ts,
                       e_density_negative=True):
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
        #read data
        self.read(i_ts)

        
    def read_from_dump(self,
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
        filename=tdc_Filenames.get_full_vis_filename(dump_id, filename+'.pickle')
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
        filename=tdc_Filenames.get_full_vis_filename(dump_id, filename+'.pickle')
        pickle.dump( dump_dict, open(filename,'w') )
        print '\nContent dumped in "%s" \n' % filename

    def __repr__(self):
        s = self._manip_name('tdc_EP_Density_Manip')
        s += '   calc_id = \"%s\"\n' % self.fe.calc_id
        s += '      i_ts = %d\n'     % self.i_ts
        return s



class tdc_EPG_Density_Manip(tdc_Manip_Plot_vs_X):
    """
    Manipulator class for Density plots of E[lectrons] P[ositrons] G[amma rays]
    """

    def __init__(self,fig_param=None):
        tdc_Manip_Plot_vs_X.__init__(self,fig_param)
        # Field DATA <<<<<<<
        self.fe=None
        self.fp=None
        self.fg=None

        
    @staticmethod
    def init_from_data(calc_id,
                        i_ts,
                        e_density_negative=True,
                        fig_param=None):
        """
        Setup Manip by reading original data

        calc_id
           calculation id name
        i_ts
           timeshot#
        --------
        Options:
        --------
        e_density_negative
        fig_param
        --------
        """
        manip=tdc_EPG_Density_Manip(fig_param)
        manip.read_from_data(calc_id, i_ts, e_density_negative=e_density_negative)
        return manip

    
    @staticmethod
    def init_from_dump(filename,
                        dump_id,
                        e_density_negative=True,
                        fig_param=None):
        """
        Setup Manip from dumped data
        filename
           pickle file name is 'filename.pickle'
        """
        manip=tdc_EPG_Density_Manip(fig_param)
        manip.read_from_dump(filename, dump_id, e_density_negative=e_density_negative)
        return manip

    
    def read_from_data(self,
                       calc_id,
                       i_ts,
                       e_density_negative=True):
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
        #read data
        self.read(i_ts)

        
    def read_from_dump(self,
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
        filename=tdc_Filenames.get_full_vis_filename(dump_id, filename+'.pickle')
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
        filename=tdc_Filenames.get_full_vis_filename(dump_id, filename+'.pickle')
        pickle.dump( dump_dict, open(filename,'w') )
        print '\nContent dumped in "%s" \n' % filename

    def __repr__(self):
        s = self._manip_name('tdc_EPG_Density_Manip')
        s += '   calc_id = \"%s\"\n' % self.fe.calc_id
        s += '      i_ts = %d\n'     % self.i_ts
        return s



class tdc_EPGP_Density_Manip(tdc_Manip_Plot_vs_X):
    """
    Manipulator class for Density plots of E[lectrons] P[ositrons] G[amma rays] P[rotons]
    """

    def __init__(self,fig_param=None):
        tdc_Manip_Plot_vs_X.__init__(self,fig_param)
        # Field DATA <<<<<<<
        self.fe=None
        self.fp=None
        self.fg=None
        self.fpr=None


    @staticmethod
    def init_from_data(calc_id,
                       i_ts,
                       e_density_negative=True,
                       fig_param=None):
        """
        Setup Manip by reading original data

        calc_id
           calculation id name
        i_ts
           timeshot#
        --------
        Options:
        --------
        e_density_negative
        fig_param
        --------
        """
        manip=tdc_EPGP_Density_Manip(fig_param)
        manip.read_from_data(calc_id, i_ts, e_density_negative=e_density_negative)
        return manip

    
    @staticmethod
    def init_from_dump(filename,
                       dump_id,
                       e_density_negative=True,
                       fig_param=None):
        """
        Setup Manip from dumped data
        filename
           pickle file name is 'filename.pickle'
        """
        manip=tdc_EPGP_Density_Manip(fig_param)
        manip.read_from_dump(filename, dump_id, e_density_negative=e_density_negative)
        return manip


    def read_from_data(self,
                       calc_id,
                       i_ts,
                       e_density_negative=True):
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
        #read data
        self.read(i_ts)


    def read_from_dump(self,
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
        filename=tdc_Filenames.get_full_vis_filename(dump_id, filename+'.pickle')
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
        filename=tdc_Filenames.get_full_vis_filename(dump_id, filename+'.pickle')
        pickle.dump( dump_dict, open(filename,'w') )
        print '\nContent dumped in "%s" \n' % filename

    def __repr__(self):
        s = self._manip_name('tdc_EPGP_Density_Manip')
        s += '   calc_id = \"%s\"\n' % self.fe.calc_id
        s += '      i_ts = %d\n'     % self.i_ts
        return s

