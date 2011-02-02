import numpy as np
import h5py

from Common  import tdc_Filenames, tdc_Timetable, tdc_Setup_Props

class tdc_Field_Data:
    """
    This class contains field and positions
    Members:
    f    -- field
    x    -- positions
    
    timetable -- Timetable instanse

    i_ts      -- # of currently stored timeshot
    name      -- name of the field (dataset name in HDF file)
    file_id   -- HDF5 file_id (with field file)
    """

    __default_Filename = 'fields.h5'

    def __init__(self, calc_id, field_name,
                 time_normalization = 'flyby',
                 filename=__default_Filename ):
        """
        Opens HDF5 file, reads positions
        the field is not read yet and all variables except
        x, name, plot_label, file_id are uninitialized
        """
        # store calc_id
        self.calc_id=calc_id
        # store field name
        self.name=field_name
        # open HDF file ------------------
        h5_filename=tdc_Filenames().get_full_filename(calc_id, filename)
        self.file_id=h5py.h5f.open(h5_filename,flags=h5py.h5f.ACC_RDONLY)
        # --------------------------------
        # read Positions -----------------
        dset_name='/' + self.name + '/Positions'
        self.__dset_x   = h5py.h5d.open(self.file_id,dset_name)
        self.__dtype_x  = self.__dset_x.get_type()
        self.__dspace_x = self.__dset_x.get_space()
        (self.nx,) = self.__dspace_x.get_simple_extent_dims()
        # preallocate space for positions <x> 
        self.x = np.empty(self.nx, dtype=self.__dtype_x)
        # read field positions
        self.__dset_x.read(self.__dspace_x, self.__dspace_x, self.x, self.__dtype_x)
        # --------------------------------
        # Timetable class member ---------
        self.timetable = tdc_Timetable(self.file_id)
        # set time normalization
        self.timetable.set_normalization(time_normalization)
        # --------------------------------
        # define publically available members
        self.f    = None
        self.i_ts = None
        # --------------------------------

    def read(self, i_ts, re_read_x=False,**kwargs):
        """
        Read field for timeshot i_ts
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
        # read field values
        # ===============================================
        dset_name='/' + self.name + '/' + str(self.i_ts)
        dset=h5py.h5d.open(self.file_id,dset_name)
        # -----------------------------------------------
        # if field is read for the first time define
        # dataspaces and datattype
        if self.f == None:
            # field datatype
            self.__dtype=dset.get_type()
            # preallocate f
            self.f=np.empty(self.nx,dtype=self.__dtype)
            # field file dataspace
            self.__file_dspace=dset.get_space()
            (nf,)=self.__file_dspace.get_simple_extent_dims()
            guard=(nf-self.nx)/2
            self.__file_dspace.select_hyperslab( (guard,),
                                                 (self.nx,),
                                                 (1,),
                                                 op=h5py.h5s.SELECT_SET )
            # field memory dataspace
            self.__mem_dspace=h5py.h5s.create_simple( (self.nx,), (self.nx,) );
        # -----------------------------------------------
        # read field from file
        dset.read(self.__mem_dspace,self.__file_dspace, self.f, self.__dtype)
        # ===============================================
        # re-read field positions if asked
        # ===============================================
        if re_read_x:
            self.__dset_x.read(self.__dspace_x, self.__dspace_x, self.x, self.__dtype_x)


    def __repr__(self):
        s  = 'tdc_Field_Data:\n'
        s += '  field name : %s\n' % self.name
        s += '     calc_id : %s\n' % self.calc_id
        s += '        i_ts : %g\n' % self.i_ts
        return s

