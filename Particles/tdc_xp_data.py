import numpy as np
import h5py
import math

import Common
from Common import tdc_Filenames, tdc_Timetable, tdc_Setup_Props

from tdc_xp_samples import *


class tdc_XP_Data:
    """
    This class contains data for phase portrait of particles
    Members:
    --------
    x    -- Positions
    p    -- Momentum
    w    -- Weight [ initialized only if requested ]

    x_em -- Position of pair-creating photon emission [exists only for Pairs]
    x_cr -- Position of pair injection                [exists only for Pairs]
    t_cr -- Time of pair injection                    [exists only for Pairs]  
    
    i_ts       -- # of currently stored timeshot
    timetable  -- tdc_Timetable instanse

    sample -- instance of a sample class
              (used bu default if no sample at reading is specified)
    
    name     -- name of the particles
    calc_id  -- calc_id
    file_id  -- HDF5 file_id (with field file)
    """

    def __init__(self, calc_id, particle_name, sample_dict=None, get_weight=False):
        """
        Opens HDF5 file, setup time class
        particle attributes are not read yet and all variables except
        name, file_id are uninitialized

        by default read all particles
        
        if  get_weight is set to True the instanse will
        read statistical weights too
        """
        # store calc_id
        self.calc_id = calc_id
        # store particle name
        self.name    = particle_name
        # default sample class
        if sample_dict==None:
            sample_dict=dict(name='regular')
        self.sample = tdc_get_XP_Sample(sample_dict)
        # set get_weight_flag
        self.get_weight_flag = get_weight
        # open HDF file -----------------
        h5_filename  = tdc_Filenames().get_full_filename(calc_id, self.name+'.h5')
        self.file_id = h5py.h5f.open(h5_filename,flags=h5py.h5f.ACC_RDONLY)
        # tdc_Timetable class member -----
        self.timetable = tdc_Timetable(self.file_id)
        # set time to flyby time
        self.timetable.set_flyby_time()
        # define members ----------------
        self.i_ts=None
        self.__dspace=None
        self.__mem_dspace=None
        self.x=np.empty(0)
        self.p=np.empty(0)
        self.w=np.empty(0)
        if self.name == 'Pairs':
            self.x_em=np.empty(0)
            self.x_cr=np.empty(0)
            self.t_cr=np.empty(0)


    def __len__(self):
        "Return number of currently stored particles"
        return len(self.x)

    def __repr__(self):
        s  = 'tdc_XP_Data :\n'
        s += ' particle name : %s\n' % self.name
        s += '       calc_id : %s\n' % self.calc_id
        s += '          i_ts : %g\n' % self.i_ts
        return s

    def read(self, i_ts, sample_dict=None,**kwargs):
        """
        Read particle data for timeshot i_ts
        Options:
        --------
        sample_dict
           If sample_dict is specified use the requested sample
           instead of the default one
        """
        # timeshot and time
        self.i_ts = i_ts
        self.timetable.read_time(i_ts)
        if self.any_particle_at_timeshot(self.i_ts):
            # setup positions and momenta ===========
            if self.name != 'Pairs':
                x_dset_name    = '/X/'      + str(self.i_ts)
                p_dset_name    = '/P_par/'  + str(self.i_ts)
                # read x and p ----------------------
                self.setup_dataspaces(p_dset_name, sample_dict)
                self.p = self.read_dataset(p_dset_name)
                self.x = self.read_dataset(x_dset_name)
                self.x = self.x.reshape(len(self.x))    # must be reshaped
            else:
                x_dset_name    = '/X_em/'   + str(self.i_ts)
                p_dset_name    = '/Energy/' + str(self.i_ts)
                x_cr_dset_name = '/X_cr/'   + str(self.i_ts)
                t_cr_dset_name = '/T_cr/'   + str(self.i_ts)
                # read p, x_em, x_cr, t_cr ----------
                self.setup_dataspaces(p_dset_name, sample_dict)
                self.p    = self.read_dataset(p_dset_name)
                self.x_em = self.read_dataset(x_dset_name)
                self.x_cr = self.read_dataset(x_cr_dset_name)       
                self.t_cr = self.read_dataset(t_cr_dset_name)                
                self.x_em = self.x_em.reshape(len(self.x_em))    # must be reshaped
                self.x_cr = self.x_cr.reshape(len(self.x_cr))    # must be reshaped
                self.x    = self.x_em.copy()
                # change Pairs positions: calculate actual position of the photon 
                dx_ph = self.x_cr - self.x_em       
                t = self.timetable.get_absolute_time()
                self.x += np.sign(dx_ph)*( t - (self.t_cr - np.abs(dx_ph)) )
            # ========================================
            # get statistical weight if requested
            if self.get_weight_flag:
                w_dset_name='/Weight/'+ str(self.i_ts)
                self.w = self.read_dataset(w_dset_name)
        else:
            self.x=np.empty(0)
            self.p=np.empty(0)
            self.w=np.empty(0)
            if self.name == 'Pairs':
                self.x_em=np.empty(0)
                self.x_cr=np.empty(0)
                self.t_cr=np.empty(0)


    def any_particle_at_timeshot(self,i_ts):
        """
        Check whether there are any particles at the timestep i_ts
        """
        dset = h5py.h5d.open(self.file_id, '/PP/Numbers/' + str(i_ts))
        dspace = dset.get_space()
        dtype  = dset.get_type()
        n, = dspace.get_simple_extent_dims()
        n_particles  = np.empty(n,dtype=dtype)
        dset.read( dspace, dspace, n_particles, dtype)
        return ( n_particles[0] > 0 )


    def setup_dataspaces(self, attr_name, sample_dict=None):
        """
        Setup dataspaces according to the sample

        If sample_dict is specified use the requested sample
        instead of the default one
        """
        # open dataset
        dset = h5py.h5d.open(self.file_id, attr_name)
        # get  dataspace
        self.__dspace = dset.get_space();
        # set sample
        if sample_dict:
            sample = tdc_get_XP_Sample(sample_dict)
        else:
            sample = self.sample
        # modify dataspace according to the reading sample
        sample.set_dataspace(self.__dspace)
        # setup memory dataspace
        self.__mem_dspace = h5py.h5s.create_simple( (sample.count,),
                                                    (sample.count,) )

    def read_dataset(self, dataset_name):
        """
        Read and return dataset with name dataset_name 
        
        1) memory and dataset dataspaces (self.__mem_dspace,
        self.__dspace) must be set up before by calling
        self.setup_dataspaces(attr_name, sample_dict)
        2) it returns an array of the same datatype as it has in HDF file!
        ( Positions arrays must be reshaped after that! )
        """
        dset  = h5py.h5d.open(self.file_id, dataset_name)
        dtype = dset.get_type()
        arr  = np.empty(self.sample.count,dtype=dtype)
        dset.read( self.__mem_dspace, self.__dspace, arr, dtype)
        return arr




