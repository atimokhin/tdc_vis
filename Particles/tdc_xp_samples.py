import h5py
import math
import numpy as np

__all__ = [ 'tdc_get_XP_Sample' ] 

def tdc_get_XP_Sample(sample_dict):
    """
    Returns instance of one of XP_Sample class according to sample_dict
    
    Available Samples:
    tdc_XP_Sample_Regular:  dict(name='regular', n_reduce=1, n_min=1)
    tdc_XP_Sample_Selected: dict(name='selected', idxs=[1,2,3] )
    """
    name = sample_dict.get('name')
    if name=='regular':
        return tdc_XP_Sample_Regular( sample_dict.get('n_reduce'),
                                      sample_dict.get('n_min')     )
    elif name=='selected':
        return tdc_XP_Sample_Selected( sample_dict.get('idxs') )
    else:
        raise tdc_XP_Sample_Exception(name)



class tdc_XP_Sample_Regular:
    """
    Selects each n_reduce' particle, but tries to keep particle number
    not smaller than n_min.
    It does all actions via set_dataspace() member function
    where given HDF5 dataspace is modified

    Members:
    n_reduce -- stride in particle selection
    n_min    -- minimum number of particles
    count    -- total number of selected particles
    """

    def __init__(self, n_reduce=None, n_min=None):
        # set default values for  n_reduce, n_min
        if n_reduce==None: n_reduce=1
        if n_min==None:    n_min=1
        # initilaize attributes
        self.n_reduce = n_reduce
        self.n_min    = n_min
        self.count    = 0

    def reset(self,n_reduce,n_min):
        "Reset n_reduce, n_min"
        self.n_reduce = n_reduce
        self.n_min    = n_min
        
    def set_dataspace(self,dspace):
        """
        select hyperslab in the dataspace and set count variable
        """
        # total number of particles in dataset
        n_particles, = dspace.get_simple_extent_dims();
        # select stride, so that do not reduce particle# below self.n_reduce
        if ( n_particles/self.n_reduce < self.n_min ):
            n_reduce = max( 1, math.floor(n_particles/self.n_min) )
        else:
            n_reduce = self.n_reduce
        # set count - number of particles to be read
        self.count = math.floor(n_particles/n_reduce);
        # select hyperslab
        dspace.select_hyperslab( start  = (0,),
                                 count  = (self.count,),
                                 stride = (n_reduce,),
                                 block  = (1,),
                                 op     = h5py.h5s.SELECT_SET )

    def __repr__(self):
        return 'tdc_XP_Sample_Regular:  n_reduce=%g, n_min=%g' % \
               (self.n_reduce, self.n_min)



class tdc_XP_Sample_Selected:
    """
    Selects particles with given indexies
    
    It does all actions via set_dataspace() member function
    where given HDF5 dataspace is modified

    Members:
    idxs  -- indexies
    count -- total number of selected particles
    """

    def __init__(self, idxs):
        # initilaize attributes
        self.count = len(idxs)
        self.idxs  = np.array(idxs)
        self.idxs  = self.idxs.reshape(self.count,1)

    def reset(self,idxs):
        "Reset n_reduce, n_min"
        self.count = len(idxs)
        self.idxs  = np.array(idxs)
        self.idxs  = self.idxs.reshape(self.count,1)
        
    def set_dataspace(self,dspace):
        """
        select elements with given idxs
        """
        # select hyperslab
        dspace.select_elements( self.idxs,
                                op = h5py.h5s.SELECT_SET )

    def __repr__(self):
        return 'tdc_XP_Selected:  %s' % self.idxs



class tdc_XP_Sample_Exception:
    "Exception class for XP_Sample"
    def __init__(self, name):
        print 'Sample "%s" does not exist!\nAborting\n' % name
    
