import numpy as np
import h5py

from Auxiliary import tdc_Filenames, tdc_Time_Normalizer, tdc_Setup_Props

class tdc_Flux_Data:
    """
    This class contains flux data for multiple cals_ids
    Members:
    --------
    f
       array with flux values
    t
       array tith time values
    name
       flux name
    prefix
       ns|lc
    flux_raw
       array with all (normalized)flux data from hdf file(s)
    time_raw
       array with all (absolute)time data from hdf file(s)
    time_normalizer
       Time_Normalizer instanse
    """

    __default_Filename = '_particle_flux.h5'

    def __init__(self, calc_ids, flux_name, prefix):
        """
        calc_ids
           claculation ids
        flux_name
           name of HDF file dataset with corresponding flux
        prefix
           'ns'|'lc'
        """
        # store flux name
        self.name=flux_name
        # store flux name
        self.prefix=prefix
        filename = self.prefix+tdc_Flux_Data.__default_Filename
        # store calc_ids
        if not isinstance( calc_ids, (list,tuple) ):
            calc_ids = (calc_ids,)
        self.calc_ids=calc_ids
        # read raw flux data from file =======
        self.time_raw=np.empty(0)
        self.flux_raw=np.empty(0)
        for calc_id in calc_ids:
            # get quantities for flux normalization
            setup_prop=tdc_Setup_Props(calc_id)
            W0=setup_prop.get_papam('/FMPProps/W0')
            dT=setup_prop.get_papam('/GridProps/dT')
            # ************************************
            # Read fluxes from file **************
            # open HDF file ------------------
            full_filename = tdc_Filenames().get_full_filename(calc_id,filename)
            self.file_id=h5py.h5f.open(full_filename,flags=h5py.h5f.ACC_RDONLY)
            # --------------------------------
            # read Timearray -----------------
            dset=h5py.h5d.open(self.file_id,'/TimeArray')
            dtype=dset.get_type()
            dspace=dset.get_space()
            (nt,)=dspace.get_simple_extent_dims()
            # preallocate space in auxiliary array 
            arr=np.empty(nt,dtype=dtype)
            # read time
            dset.read(dspace,dspace,arr,dtype)
            # append read timearray to self.time_raw
            self.time_raw=np.concatenate((self.time_raw,arr))
            # --------------------------------
            # read Flux ----------------------
            dset=h5py.h5d.open(self.file_id,self.name)
            dtype=dset.get_type()
            # read flux
            dset.read(dspace,dspace,arr,dtype)
            # normalize flux and append it to self.flux_raw
            self.flux_raw=np.concatenate((self.flux_raw, W0/dT*arr))
            # --------------------------------
        # ====================================
        # indexies for working domain---------
        self.idx=[0,-1]
        # -------------------------------------
        self.time_normalizer=tdc_Time_Normalizer(calc_ids[0])
        self.time_normalizer.set_flyby_time()
        self.reset()

    def get_pure_data_copy(self):
        """
        Returns copy containing only data necessary for producing a sinle plot,
        without HDF file specific info
        Used for saving data for subsequent restoring of plot without
        accesing original data files
        """
        import copy
        data=copy.copy(self)
        data.file_id = None
        return data

    def __repr__(self):
        s  = 'tdc_Flux_Data:\n'
        s += '      flux : "%s"\n' % self.name 
        s += ' direction : %s\n'   % self.prefix 
        s += '      time : ( %g, %g )  [%s]\n' %  (self.t[0],self.t[-1],self.time_normalizer)
        return s

    def set_time(self,tt):
        "Set working time domain"
        # set indexies
        tt=self.time_normalizer.to_absolute_time(tt)
        for j,t in enumerate(tt):
            if t >= self.time_raw[-1]:
                self.idx[j] = len(self.time_raw)
            else:
                self.idx[j] = ( i for i,t_r in enumerate(self.time_raw) if t_r>t ).next() 
            self.idx[j] = max(0,self.idx[j]-1)
        # reset working arrays
        self.reset()


    def mean(self,tt=None):
        """
        Return mean value of the flux for time interval tt
        if tt=None (delault) calculate mean flux for the current interval
        """
        # store old idx and set new time
        if tt:
            idx_old=self.idx[:]
            self.set_time(tt)
        # calculate mean value of the flux
        f_mean=np.mean(self.f)
        # restore idx
        if tt:
            self.idx=idx_old
            self.reset()
        return f_mean


    def smooth(self,window_len=10,window='flat'):
        """
        Smooth flux distribution
        window_len  -- length of the window
        window      -- window type
        """
        if self.f.size < window_len:
            raise ValueError, "Input vector needs to be bigger than window size."
        if window_len>3:
            # prepare array boundaries
            s=np.r_[2*self.f[0] - self.f[window_len:1:-1],
                    self.f,
                    2*self.f[-1] - self.f[-1:-window_len:-1]]    
            # set window
            if window == 'flat': #moving average
                w=np.ones(window_len,'d')
            else:
                w=eval('np.'+window+'(window_len)')
            # do convolution
            y=np.convolve(w/w.sum(),s,mode='same')
            # extract physical part
            self.f=y[window_len-1:-window_len+1]


    def reset(self):
        "Reset working arrays for current time domain"
        self.t=self.time_normalizer.to_normalized_time(self.time_raw[self.idx[0]:self.idx[1]])
        self.f=self.flux_raw[self.idx[0]:self.idx[1]]
        

