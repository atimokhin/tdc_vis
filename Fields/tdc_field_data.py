import numpy as np
import h5py

from ATvis.Common_Data_Plot import AT_Data

from Auxiliary        import tdc_Filenames, tdc_Timetable, tdc_Setup_Props, tdc_Mesh
from Common_Data_Plot import tdc_Data__with_Timetable


class tdc_Field_Data(tdc_Data__with_Timetable,AT_Data):
    """
    This class contains field and positions
    Members:
    self.f    -- field
    self.x    -- positions
    
    self.timetable -- Timetable instanse

    self.i_ts      -- # of currently stored timeshot
    self.name      -- name of the field (dataset name in HDF file)
    self.file_id   -- HDF5 file_id (with field file)

    self.ghost_points -- whether to read the data from ghost points
    """

    __default_Filename = 'fields.h5'
    __default_time_normalization='flyby'

    def __init__(self,
                 calc_id,
                 field_name,
                 time_normalization=None,
                 ghost_points=False,
                 filename=__default_Filename):
        """
        - opens HDF5 file (self.file_id)
        - nothing is read yet except timetable (self.timetable)
        --------
        Options:
        --------
        time_normalization
          <None> default time normalization is used ('flyby')
                 time normalization is the same as in tdc_Timetable
        ghost_points
          <False> whether to read the data from ghost points
        """
        # setup class variables ----------
        # store calc_id
        self.calc_id=calc_id
        # store field name
        self.name=field_name
        # read ghost points?
        self.ghost_points=ghost_points
        # open HDF file ------------------
        h5_filename=tdc_Filenames.get_full_filename(calc_id, filename)
        try:
            self.file_id = h5py.h5f.open(h5_filename,flags=h5py.h5f.ACC_RDONLY)
        except IOError as exception:
            print "Error opening \"%s\"\n" % h5_filename
            raise exception
        # Initialize Timetable -----------
        self.timetable = tdc_Timetable(self.file_id)
        # set time normalization <<<<<<<<<
        if not time_normalization:
            time_normalization=self.__default_time_normalization
        self.timetable.set_normalization(time_normalization)
        # Initialize Mesh ---------------
        self._Mesh = tdc_Mesh(self.calc_id)
        # set other members to None ------
        self.x    = None
        self.f    = None
        self.i_ts = None
        # set auxilary members to None ---
        self.__dtype       = None
        self.__dset_x      = None
        self.__dtype_x     = None
        self.__dspace_x    = None
        self.__file_dspace = None
        self.__mem_dspace  = None
        

    def get_pure_data_copy(self):
        """
        Returns copy containing only data necessary for producing a sinle plot,
        without HDF file specific info
        Used for saving data for subsequent restoring of plot without
        accesing original data files
        """
        import copy
        data=copy.copy(self)
        data.file_id       = None
        data.__dtype       = None
        data.__dset_x      = None
        data.__dtype_x     = None
        data.__dspace_x    = None
        data.__file_dspace = None
        data.__mem_dspace  = None
        data.timetable=data.timetable.get_pure_data_copy() 
        return data


    def read(self, i_ts, re_read_x=False,**kwargs):
        """
        Read field for timeshot i_ts
        --------
        Options:
        --------
        re_read_x
           if True read positions from disk again
           (cell <-> x coordinate changes)
        """        
        # ===============================================
        # time and timestep
        # ===============================================
        self.i_ts = i_ts
        self.timetable.read_time(i_ts)
        # ===============================================
        # Field dataset
        # ===============================================
        dset_name='/' + self.name + '/' + str(self.i_ts)
        dset=h5py.h5d.open(self.file_id,dset_name)
        # ***********************************************
        # ===============================================
        # If fields and positions are read for the first time
        # initialize HDF5 dataspaces and datattype
        # ===============================================
        # -----------------------------------------------
        # if Positions (self.x) are read for the first time 
        # -----------------------------------------------
        if self.x==None:
            dset_x_name='/' + self.name + '/Positions'
            self.__dset_x   = h5py.h5d.open(self.file_id,dset_x_name)
            self.__dtype_x  = self.__dset_x.get_type()
            self.__dspace_x = self.__dset_x.get_space()
            (self.nx,) = self.__dspace_x.get_simple_extent_dims()
        # -----------------------------------------------
        # if Field (self.f) is read for the first time 
        # -----------------------------------------------
        if self.f==None:
            # field datatype
            self.__dtype=dset.get_type()
            # field file dataspace
            self.__file_dspace=dset.get_space()
            (nf,)=self.__file_dspace.get_simple_extent_dims()
            # adjust number of read elements if no ghost points are requested
            guard=(nf-self.nx)/2
            nf_read = nf if self.ghost_points else self.nx
            nf_ghost = 0 if self.ghost_points else guard
            # preallocate self.f <=====
            self.f=np.empty(nf_read,dtype=self.__dtype)
            # field dataspace in file
            self.__file_dspace.select_hyperslab( (nf_ghost,),
                                                 (nf_read,),
                                                 (1,),
                                                 op=h5py.h5s.SELECT_SET )
            # field memory dataspace
            self.__mem_dspace=h5py.h5s.create_simple( (nf_read,), (nf_read,) );
        # ***********************************************
        # ===============================================
        # Read data
        # ===============================================
        # read field from file <<<<<<<<<<<<<<<<<<<<<<<<<<
        dset.read(self.__mem_dspace,self.__file_dspace, self.f, self.__dtype)
        # ===============================================
        # Read or re-read field positions (if asked)
        # ===============================================
        if re_read_x or self.x==None:
            # if Positions (self.x) are read for the first time
            # allocate space for an numpy array
            if self.x==None:
                self.nx_ghost = guard if self.ghost_points else 0
                # preallocate self.x <=====
                self.x = np.empty(self.nx+self.nx_ghost*2, dtype=self.__dtype_x)
            # -----------------------------------------------
            # read positions of physical points
            self.__dset_x.read(self.__dspace_x,
                               self.__dspace_x,
                               self.x[self.nx_ghost:-self.nx_ghost],
                               self.__dtype_x)
            # set positions of ghost points [if requested] 
            if self.ghost_points:
                dx = self.x[self.nx_ghost+1] - self.x[self.nx_ghost]
                for i in range(1,self.nx_ghost+1):
                    self.x[self.nx_ghost-i]    = self.x[self.nx_ghost] - i*dx
                    self.x[-self.nx_ghost+i-1] = self.x[-self.nx_ghost-1] + i*dx


    def __repr__(self):
        s  = 'tdc_Field_Data:\n'
        s += '  field name : %s\n' % self.name
        s += '     calc_id : %s\n' % self.calc_id
        s += '        i_ts : %g\n' % self.i_ts
        s += 'ghost_points : %s\n' % str(self.ghost_points)
        return s

