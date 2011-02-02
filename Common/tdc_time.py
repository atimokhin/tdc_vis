import numpy as np
import h5py
import os

from tdc_filenames import tdc_Filenames
from tdc_functions import tdc_get_bound_index
from tdc_exception import tdc_Exception

class tdc_TimeInfo:
    """
    Provides intormation about timetable.
    (by default uses timetable from 'fields.h5')

    Redirects all non-implemented requests to timetable

    Members:
    timetable -- tdc_Timetable instance
    timearray -- timearray from the current time
    """

    __default_filename='fields.h5'

    def __init__(self, calc_id, filename=None):
        """
        Opens HDF5 file (default:'fields.h5'), sets up
        timetable and reads timearray
        """
        # if no fielname defined use default one
        if not filename: filename=tdc_TimeInfo.__default_filename
        # HDF5 file
        h5_filename = tdc_Filenames().get_full_filename(calc_id, filename)
        file_id  = h5py.h5f.open(h5_filename,flags=h5py.h5f.ACC_RDONLY)
        # setup timetable
        self.timetable=tdc_Timetable(file_id)
        # set time to flyby time
        self.timetable.set_flyby_time()
        # retrieve timearray
        self.timearray = self.timetable.get_time_array()

    def __getattr__(self,attrname):
        return getattr(self.timetable,attrname)

    def __repr__(self):
        s  = 'TimeInfo:\n'
        s += '  # of timeshots: %g\n' % self.get_number_of_ts()
        s += '  # of timesteps: %g\n' % self.get_number_of_timesteps()
        s += '  time normalization: [%s] ' % self.timetable.get_normalization()
        return s

    def ts2time(self,ts):
        return self.timearray[ts-1]

    def time2ts(self,time):
        return tdc_get_bound_index(time,self.timearray)+1

    def get_number_of_ts(self):
        return len(self.timearray)

    def get_number_of_timesteps(self):
        timesteps=self.timetable.get_timestep_array()
        return timesteps[-1]-timesteps[0]

        
        

class tdc_Time_Normalizer:
    """
    This class contains constants and methods
    for time normalization.

    When printed gives 'noramlization'

    For proper functioning it requires file 'setup_properties.h5'.
    If this file is not present, the only available normalization is
    'absolute', and it cannot be changed.
    """

    def __init__(self, calc_id):
        # setup time normalization constants
        filename=tdc_Filenames().get_full_filename(calc_id, '/setup_properties.h5')
        # ...............................................
        # try to setup constants for other normalizations
        try:
            f=h5py.File(filename,'r')
        except IOError:
            self.__no_normalization_flag__flyby=True
            self.__no_normalization_flag__plasma_osc=True
        else:
            # plasma frequency --------------------------
            self.__no_normalization_flag__plasma_osc=False
            # Workaround--------<<<<<<<<<<<<
            if f.get('/PlasmaProps/Tau', False):
                self.__Tau_pl=f['/PlasmaProps/Tau'].value
            elif f.get('/GJPlasmaProps/Tau', False):
                self.__Tau_pl=f['/GJPlasmaProps/Tau'].value
            else:
                self.__no_normalization_flag__plasma_osc=True
            # domain length -----------------------------
            if f.get('/GridProps/L', False):
                self.__L = f['/GridProps/L'].value
                self.__no_normalization_flag__flyby=False
            else:
                self.__no_normalization_flag__flyby=True
            # -------------------------------------------
            f.close()
        # ...............................................
        self.__normalization_coeff=1
        self.__normalization_type='absolute'

    def __repr__(self):
        return '%s' % self.get_normalization()
        
    def to_normalized_time(self,time_abs):
        """
        Converst absolute time into normalized time
        [for currently active normalization]
        time_abs  -- absolute time
        ()=> normalized time
        """
        if isinstance( time_abs, (list,tuple) ):
            return [ t/self.__normalization_coeff for t in time_abs ]
        else:
            return time_abs/self.__normalization_coeff

    def to_absolute_time(self,time_norm):
        """
        Convert normalized time [for currently active normalization]
        into absolute time
        time_norm  -- normalized time
        ()=> absolute time
        """
        if isinstance( time_norm, (list,tuple) ):
            return [ t*self.__normalization_coeff for t in time_norm ]
        else:
            return self.__normalization_coeff*time_norm


    def set_flyby_time(self):
        if self.__no_normalization_flag__flyby:
            print 'Cannot set Time normalization to \'flyby\'!'
        else:
            self.__normalization_type='flyby'
            self.__normalization_coeff=self.__L

    def set_plasma_osc_time(self):
        if self.__no_normalization_flag__plasma_osc:
            print 'Cannot set Time normalization to \'plasma_osc\'!'
        else:
            self.__normalization_type='plasma_osc'
            self.__normalization_coeff=self.__Tau_pl            

    def set_absolute_time(self):
        self.__normalization_type='absolute'
        self.__normalization_coeff=1

    def set_normalization(self,normalization_type):
        "set normalization according to normalization_type"
        if normalization_type=='flyby':
            self.set_flyby_time()
        elif normalization_type=='plasma_osc':
            self.set_plasma_osc_time()
        elif normalization_type=='absolute':
            self.set_absolute_time()
        else:
            raise tdc_Exception()

    def get_normalization(self):
        "returns string with current normalization name"
        return self.__normalization_type


class tdc_Timetable(tdc_Time_Normalizer):
    """
    This class provides time information by reading HDF file Timetable
    time -- current time ( for timeshot# i_ts ) 
    i_ts -- current timeshot#

    when printed gives 't [noralization]'
    """

    TimetableGrpName   = 'Timetable'    
    TimeArrayName      = 'Time'
    TimestepArrayName  = 'Timestep'
    TimeshotsName      = 'NumberOfTimeshots'
    RefGrpName         = 'Ref'

    def __init__(self, file_id):
        """
        Set up dasaset/dataspace for reading Timetable
        in HDF file with file_id
        """
        # store HDF5 file_id
        self.file_id=file_id
        # setup normalization constants in base class
        calc_id = os.path.basename(os.path.dirname(self.file_id.name))
        tdc_Time_Normalizer.__init__(self,calc_id)
        # setup Timetable HDF variables
        dset_name='/' + self.TimetableGrpName + '/' + self.TimeArrayName
        self.__dset = h5py.h5d.open(self.file_id, dset_name)
        self.__dtype      = self.__dset.get_type()
        self.__dspace     = self.__dset.get_space()
        self.__mem_dspace = h5py.h5s.create_simple( (1,), (1,) );
        # preallocate space for time
        self.time = np.array([0],dtype=self.__dtype)
        # define i_ts
        self.i_ts = None

    def __repr__(self):
        return '%g [ %s ]' % ( self.get_time(), self.get_normalization() )

    def read_time(self,i_ts):
        "reads time from HDF file for  timeshot# i_ts"
        self.i_ts=i_ts
        self.__dspace.select_elements([(i_ts-1,)])
        self.__dset.read(self.__mem_dspace,self.__dspace, self.time, self.__dtype)

    def get_time(self):
        "returns current time properly normalized"
        return self.to_normalized_time(self.time[0])

    def get_absolute_time(self):
        "return absolute time"
        return self.time[0]

    def get_time_array(self):
        """
        read the whole time array from the file
        () => time array in currently active normalization (ndarray)
        """
        dspace = self.__dset.get_space()
        (nt,) = dspace.get_simple_extent_dims()
        time  = np.empty(nt,dtype=self.__dtype)
        self.__dset.read( dspace, dspace, time, self.__dtype)
        return self.to_normalized_time(time)

    def get_timestep_array(self):
        """
        read the whole timestep array from the file
        () => timestep array 
        """
        dset_name = '/' + self.TimetableGrpName + '/' + self.TimestepArrayName
        dset = h5py.h5d.open(self.file_id, dset_name)
        dtype  = dset.get_type()
        dspace = dset.get_space()
        (nt,) = dspace.get_simple_extent_dims()
        timesteps = np.empty(nt,dtype=dtype)
        dset.read( dspace, dspace, timesteps, dtype)
        return timesteps

    def get_number_of_timeshots(self):
        """
        read /Timetable/NumberOfTimeshots
        () => number_of_timeshots
        """
        dset_name = '/' + self.TimetableGrpName + '/' + self.TimeshotsName
        dset = h5py.h5d.open(self.file_id, dset_name)
        dtype  = dset.get_type()
        dspace = dset.get_space()
        (nt,) = dspace.get_simple_extent_dims()
        number_of_timeshots = np.empty(nt,dtype=dtype)
        dset.read( dspace, dspace, number_of_timeshots, dtype)
        return number_of_timeshots[0]


class tdc_Timetable_Cached(tdc_Time_Normalizer):
    """
    This class provides tdc_Timetable functionality by
    using internally stored timetable and timeshots

    time -- current time ( for timeshot# i_ts ) 
    i_ts -- current timeshot#

    when printed gives 't [noralization]'
    """
    def __init__(self, timetable):
        """
        Set up arrays and normalization using information
        from Timetable instance timetable
        """
        # setup normalization constants in base class
        calc_id = os.path.basename(os.path.dirname(timetable.file_id.name))
        tdc_Time_Normalizer.__init__(self,calc_id)
        # set normalization
        self.set_normalization(timetable.get_normalization())
        # setup arrays
        self.timesteps     = timetable.get_timestep_array()
        self.abstime_array = self.to_absolute_time(timetable.get_time_array())
        self.number_of_timeshots = timetable.get_number_of_timeshots()

    def __repr__(self):
        return '%g [ %s ]' % ( self.get_time(), self.get_normalization() )

    def read_time(self,i_ts):
        "store i_ts in internal variable"
        self.i_ts=i_ts-1

    def get_time(self):
        "returns current time properly normalized"
        return self.to_normalized_time(self.abstime_array[self.i_ts])

    def get_absolute_time(self):
        "return absolute time"
        return self.abstime_array[self.i_ts]

    def get_time_array(self):
        """
        return the whole time array in currently active normalization (ndarray)
        """
        return self.to_normalized_time(self.abstime_array)

    def get_timestep_array(self):
        """
        return the whole timestep array
        """
        return self.timesteps
    
    def get_number_of_timeshots(self):
        """
        return number_of_timeshots
        """        
        return self.number_of_timeshots




