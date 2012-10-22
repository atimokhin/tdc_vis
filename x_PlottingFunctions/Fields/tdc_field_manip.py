from Common_Data_Plot  import tdc_Manip_Plot_vs_X
from Fields            import tdc_Field_Data, tdc_Fields_Plotter



class tdc_Field_Manip(tdc_Manip_Plot_vs_X):
    """
    Manipulator class for Field
    """
    
    def __init__(self,fig_param=None):
        tdc_Manip_Plot_vs_X.__init__(self,fig_param)
        # Field DATA <<<<<<<
        self.field=None
        
        
    @staticmethod
    def init_from_data(calc_id,
                       i_ts,
                       field_name,
                       fig_param=None):
        """
        Setup Manip by reading original data

        calc_id
           calculation id name
        field_name
           name of the field to be plotted
        i_ts
           timeshot#
        --------
        Options:
        --------
        fig_param
        --------
        """
        manip=tdc_Field_Manip(fig_param)
        manip.read_from_data(calc_id, i_ts, field_name)
        return manip

    
    @staticmethod
    def init_from_dump(filename,
                       dump_id,
                       fig_param=None):
        """
        Setup Manip from dumped data
        filename
           pickle file name is 'filename.pickle'
        """
        manip=tdc_Field_Manip(fig_param)
        manip.read_from_dump(filename, dump_id)
        return manip

    
    
    def read_from_data(self,
                       calc_id,
                       i_ts,
                       field_name):
        """
        setup Manip by reading the original data file
        """
        # Field <<<<<<<
        self.field = tdc_Field_Data(calc_id, field_name)
        # set PLOTTER by calling base class method
        self.set_plotter( tdc_Fields_Plotter(self.field) )
        # read data
        self.read(i_ts)
        
    
    def read_from_dump(self,
                       filename,
                       dump_id):
        """
        setup Manip by reading the pickle'd data dumped
        by Manip called before
        """
        import pickle
        from   Auxiliary import tdc_Filenames
        # set restored_from_dump flag so the data cannot be read again
        self.restored_from_dump=True
        # Field <<<<<<<
        # full file name of the file with manipulator dump
        filename=tdc_Filenames.get_full_vis_filename(dump_id, filename+'.pickle')
        fields = pickle.load( open(filename,'r') )
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
    
