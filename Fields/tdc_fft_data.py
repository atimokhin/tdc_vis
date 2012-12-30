import h5py
import math

import scipy
import scipy.fftpack

from ATvis.Common_Data_Plot  import AT_Data

from Common_Data_Plot  import tdc_Data__with_Timetable
from Auxiliary         import tdc_Mesh
from tdc_field_data    import tdc_Field_Data


class tdc_FFT_Data(tdc_Data__with_Timetable, AT_Data):
    """
    This class contains data for discrete Fourier 
    transform of for a field
    -----------
    Attributes:
    -----------
    field
       tdc_XP_Data

    xx_default
       default space interval
    xx
       current space interval
    nx
       number of sampled points
    dx
       cell size (need for frequency calculation),
       set by set_xx_default__and_dx()

    power_2_flag
       whether to adjust the desired number of sampled points toward the closest
       power of 2
       
    kk
       wavevector interval
    imax__kk
        index of the last positive wave vector in self.kk
    Fk
       Fourier transform coefficients 
    Ik
       power spectrum
    """

    def __init__(self, calc_id, field_name, xx=None, power_2_flag=False):
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
        power_2_flag = True|False
            <False>
        """
        # name and calc_id
        self.name    = field_name
        self.calc_id = calc_id
        self.field   = tdc_Field_Data(calc_id, field_name)
        # interface to timetable
        self.timetable = self.field.timetable
        # set default space interval and dx
        self.set_xx_default__and_dx(xx)
        # initialize xx
        self.xx = self.xx_default
        # initialize members
        self.Fk = None
        self.Ik = None
        self.kk = None
        # default value for power_2_flag
        self.power_2_flag = power_2_flag

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
        s  = 'tdc_FFT_Data:\n'
        s += '    field name : %s\n' % self.name
        s += '       calc_id : %s\n' % self.calc_id
        s += '          i_ts : %g\n' % self.field.i_ts
        s += '            xx = [%g, %g]\n' % tuple(self.xx)
        s += '            nx = %i\n' % self.nx
        s += '      imax__kk = %i\n' % self.imax__kk
        return s

    def read(self, i_ts, xx=None, **kwargs):
        """
        Read field data for timeshot i_ts and calculate Fourier spectrum for
        specified space interval xx,
        or if xx==None for the default space interval
        """
        self.field.read(i_ts)
        self.calculate_spectrum(xx,self.power_2_flag)

    def calculate_spectrum(self, xx=None, power_2_flag=False):
        """
        Calculate Fourier spectrum for current timeshot,
        also sets current xx
        NB: power_2_flag not yeat implemented!<==
        --------
        Options:
        --------
        xx     = (x1,x2) <None> by default domain given
                 at initilaization domain will be used
        """
        # change current space interval
        if xx:
            self.xx = xx
        else:
            self.xx = self.xx_default
        # find indexies for the desired spatial interval
        n1 = (self.field.x<=self.xx[0]).nonzero()[0][-1]
        n2 = (self.field.x<=self.xx[1]).nonzero()[0][-1]
        # number of sampled points
        self.nx = n2 - n1 + 1
        # frequencies (wave vector)
        self.kk = scipy.fftpack.fftfreq(self.nx, self.dx)
        # index of the last positive wave vector in self.kk
        self.imax__kk = (self.kk>=0).nonzero()[0][-1]
        # Fourier transform coefficients (complex)
        self.Fk = scipy.fftpack.fft(self.field.f[n1:n2])
        # Power spectrum
        self.Ik = (abs(self.Fk))**2


 
    def set_xx_default__and_dx(self,xx=None):
        """
        Set **default** space interval for which particle spectrum
        will be calculated and also sets dx!
        NB: Reads mesh.h5 !
        xx
          (x1,x2), if None [default] use whole computational domain
        """
        # read Mesh <=== !
        mesh = tdc_Mesh(self.field.calc_id)
        self.dx = mesh.dx
        if xx:
            self.xx_default = xx
        else:
            self.xx_default = (mesh.xmin,mesh.xmax)



