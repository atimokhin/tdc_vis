import numpy as np
import h5py

from tdc_filenames  import tdc_Filenames

class tdc_Mesh:
    """
    This class contains coordinates of cell boundaries
    and function for transforming x coordinate in to a cell number

    Members:
    --------
    x_b
       coordinates of cell boundaries
    dx
       cell width
    xmin
       x_b[0]
    xmax
        x_b[-1]
    """

    __default_Filename = 'mesh.h5'

    def __init__(self, calc_id, **kwargs):
        """
        Opens mesh.h5 file, reads positions
        """
        # open HDF file
        h5_filename=tdc_Filenames().get_full_filename(calc_id, self.__default_Filename)
        ## self.file_id=h5py.h5f.open(h5_filename,flags=h5py.h5f.ACC_RDONLY)
        file_id=h5py.h5f.open(h5_filename,flags=h5py.h5f.ACC_RDONLY)
        # read positions parameters from HDF file
        dset_name='/Mesh/CellBoundaries'
        ## dset=h5py.h5d.open(self.file_id,dset_name)
        dset=h5py.h5d.open(file_id,dset_name)
        dtype=dset.get_type()
        dspace=dset.get_space()
        (self.nx,)=dspace.get_simple_extent_dims()
        # preallocate space for positions <x> 
        self.x_b=np.empty(self.nx,dtype=dtype)
        # read field positions
        dset.read(dspace,dspace,self.x_b,dtype)
        # set dx
        self.dx = self.x_b[1]-self.x_b[0]
        # set xmin, xmax
        self.xmin=self.x_b[0]
        self.xmax=self.x_b[-1]
        

    def x2cell(self,xx):
        """
        Transforms positions x into cell boundaries numbers
        xx
          Positions
        ()=>
          Cell #s
        """
        if isinstance(xx, (list,tuple)):
            return [ x/self.dx for x in xx ]
        return xx/self.dx

    def cell2x(self,cc):
        """
        Transforms cell boundaries numbers into positions
        cc
          Cell #s
        ()=>
          Positions
        """
        if isinstance(cc, (list,tuple)):
            return [ c*self.dx for c in cc ]
        else:
            return cc*self.dx
        
