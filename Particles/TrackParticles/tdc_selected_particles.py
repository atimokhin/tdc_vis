from Common.tdc_filenames  import tdc_Filenames

class tdc_Selected_Particles:
    """
    Container which stores IDs of selected particles

    Members:
    --------
    calc_id
       calc_id where particles were selected
    i_ts
       timeshot# where selection where particles were selected
    IDs
       list with IDs of selected particles:
       [[IDTS1 ID1],  -- IDs of individual selected particle
       [IDTS2 ID2] 
       ...        ]
                 
    Delegates all requests to IDs
    """

    def __init__(self):
        self.calc_id = None
        self.i_ts    = None
        self.IDs     = []

    def __getattr__(self,attrname):
        return getattr(self.IDs,attrname)

    def __repr__(self):
        s  = 'tdc_Selected_Particles:\n'
        s += ' calc_id = %s\n' % self.calc_id
        s += '    i_ts = %g\n' % self.i_ts
        s += ' # of selected particles = %g\n' % len(self.IDs)
        s += ' IDs = %s\n' % str(self.IDs)
        return s
    
    def setup_from_matlab_file(self,calc_id,sp_id):
        """
        Read .mat file created by MATLAB function save_selected_particle_to_file()
        and sets up all members
        the file to be read  is 'sp_{sp_id}.mat' in the calc_id RESULTS directory
        """
        import scipy.io
        filename = 'sp_' + sp_id + '.mat'
        full_filename = tdc_Filenames().get_full_filename(calc_id,filename)
        mat_struct   = scipy.io.loadmat(full_filename,struct_as_record=True)
        self.calc_id = str(mat_struct['sp']['calc_id'][0][0][0])
        self.i_ts    = int(mat_struct['sp']['timeshot'][0][0][0])
        self.IDs     = [ list(i) for i in mat_struct['sp']['IDs'][0][0] ]


