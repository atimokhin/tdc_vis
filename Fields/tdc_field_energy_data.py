import h5py
import math

import scipy
import scipy.fftpack
import numpy as np

from Auxiliary         import tdc_Mesh
from Auxiliary         import tdc_get_bound_index
from Auxiliary         import tdc_Setup_Props
from tdc_field_data    import tdc_Field_Data


class tdc_Field_Energy_Data:
    """
    This class contains data for field energy density: E^2

    The spatial interval where energy density is collected and averaged
    is fixed at class initialization
    -----------
    Attributes:
    -----------
    field tdc_XP_Data

    xx_default
       default space interval
    xx
       current space interval
    nx
       number of sampled points in x axis
    tt
       current time interval
    nt
       number of sampled timeshots
    W
       <ndarray> energy density at the current timeshot
    W_av__x
       <scalar> mean energy density averaged over x at the current timeshot
    W_av__x_std
       <scalar> standard deviation for the mean energy density averaged over x at the current timeshot
    W_av__x_timearray
       <ndarray> mean energy density averaged over x (function of time)
    W_av__xt
       <scalar> mean energy density averaged over x and t 
    W_av__xt_std
       <scalar> standard vediation for the mean energy density averaged over x and t 
    """

    def __init__(self, calc_id, field_name, xx=None):
        """
        - opens fields HDF5 file, 
        - setup timetable,
        - setup default space interval
        ---------
        Parameters:
        ---------
        calc_id
        field_name
        ---------
        Options:
        ---------
        xx     = (x1,x2)
            *Default* spacial interval
            <None> by default the whole domain will be used
        """
        # name and calc_id
        self.name    = field_name
        self.calc_id = calc_id
        self.field   = tdc_Field_Data(calc_id, field_name)
        # interface to timetable
        self.timetable = self.field.timetable
        # set space interval -- initialize self.xx 
        self.setup_xx(xx)
        # initialize members
        self.W = None
        self.t = None
        self.W_av__x_timearray = None
        self.W_av__x      = None
        self.W_av__x_std  = None
        self.W_av__xt     = None
        self.W_av__xt_std = None
        # normalization constant for the electric field
        setup_props = tdc_Setup_Props(calc_id)
        B0 = setup_props.get_papam('PulsarGapProps/B_12')
        P  = setup_props.get_papam('PulsarGapProps/P')
        self.E_NORM = np.sqrt(P/B0)

    def get_pure_data_copy(self):
        """
        Returns copy containing only data necessary for producing a sinle plot,
        without HDF file specific info
        Used for saving data for subsequent restoring of plot without
        accesing original data files
        """
        import copy
        data = copy.copy(self)
        data.field = data.field.get_pure_data_copy() 
        data.timetable = data.timetable.get_pure_data_copy() 
        return data

    def __repr__(self):
        s  = 'tdc_Field_Energy_Data:\n'
        s += '    field name : %s\n' % self.name
        s += '       calc_id : %s\n' % self.calc_id
        if self.field.i_ts:
            s += '          i_ts : %g\n' % self.field.i_ts
            s += '            xx = [%g, %g]\n' % tuple(self.xx)
            s += '            nx = %i\n' % self.nx
            s += '        <W>_xx = %g\n' % self.W_av__x
        else:
            s += '==> No data has been read yet!\n'
        return s

    def read(self, i_ts, **kwargs):
        """
        Read field data for timeshot i_ts and calculate energy density and
        the mean energy density over the spacial interval xx
        """
        self.field.read(i_ts)
        self.calculate_W()

    def calculate_W(self):
        """
        Calculate energy density for the current timeshot
        """
        # find indexies for the desired spatial interval
        n1 = (self.field.x<=self.xx[0]).nonzero()[0][-1]
        n2 = (self.field.x<=self.xx[1]).nonzero()[0][-1]
        # number of sampled points
        self.nx = n2 - n1 + 1
        # calculate W(x)
        self.W = self.field.f[n1:n2]**2 * self.E_NORM**2
        # calculate <W>_xx -- mean energy density in the interval xx
        self.W_av__x     = self.W.mean()
        self.W_av__x_std = self.W.std()

    def calculate_W_t(self,tt):
        """
        Calculate energy density for time interval tt
        """
        timearray = self.timetable.get_time_array()
        i_ts__start = tdc_get_bound_index( tt[0], timearray )
        i_ts__end   = tdc_get_bound_index( tt[1], timearray )
        self.t = timearray[i_ts__start:i_ts__end]
        # preallocate array
        self.W_av__x_timearray = np.zeros(i_ts__end - i_ts__start)
        for i in range(i_ts__start,i_ts__end):
            self.read(i)
            self.W_av__x_timearray[i-i_ts__start] = self.W_av__x
        # mean energy density over the whole time interval
        self.W_av__xt     = self.W_av__x_timearray.mean()
        self.W_av__xt_std = self.W_av__x_timearray.std()
        
 
    def setup_xx(self,xx=None):
        """
        Set **default** space interval for which particle spectrum
        will be calculated and also sets dx!
        NB: Reads mesh.h5 !
        xx
          (x1,x2), if None [default] use whole computational domain
        """
        mesh = tdc_Mesh(self.field.calc_id)
        if xx:
            self.xx = xx
        else:
            self.xx = (mesh.xmin,mesh.xmax)



