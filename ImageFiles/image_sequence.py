import os
import re
import numpy as np

from Auxiliary        import *
from Common_Data_Plot import tdc_Sequence

from image_data import Image_Data


class Image_Sequence(tdc_Sequence):
    """
    Data sequence for Image Data classes
    initialized from directory containing image files created by
    data payer
    """

    _default_index_filename = 'index.txt'
    
    def __init__(self, image_data, image_id, ii=None):
        """
        Intialized data sequence from list of fmci_xps objects
        data files in: results_vis_dir/image_id/

        image_data
           instance of tdc_FMCI_*_Data class for data intialization
        image_id
           image id (directory with image files)
        --------
        Options:
        --------
        ii
           i_ts index interval <[i1,<i2>]>           
        """
        self.dirname = os.path.join(tdc_Filenames.get_vis_results_dir(),image_id)
        # read data from index file
        filename = os.path.join(self.dirname,self._default_index_filename)
        try:
            f=open(filename,'r')
        except IOError:
            raise tdc_Exception( 'Cannot open \"%s\"' % filename )
        # read index file content into string
        index_file_str = f.read()
        f.close()
        # parse index file and initialize index array
        array_idx_str=re.findall(r'(\d{5})\.png',index_file_str)
        self.array_idx=np.loadtxt(array_idx_str, dtype=np.int32)
        # initialize start and end sequence indexies
        self.idx_seq__start = self.array_idx[0]
        self.idx_seq__end   = self.array_idx[-1]
        # adjust indexies according to ii
        if ii is not None:
            # be sure t is tuple or list
            if not isinstance( ii, (list,tuple) ): ii = (ii,)
            # for non-default t set limits
            if len(ii) == 1:
                self.idx_seq__start = max( self.idx_seq__start, min(ii[0],self.idx_seq__end))
            elif len(ii) == 2:
                self.idx_seq__start = max( self.idx_seq__start, min(ii[0],self.idx_seq__end))
                self.idx_seq__end   = min( self.idx_seq__end,   max(ii[1],self.idx_seq__start))
        # -------------------------------------------
        # setup FMCI_Data_Base instance
        self.image_data = image_data

    @staticmethod
    def init_from_data(image_data_class, image_id, ii=None, **kwargs):
        """
        Intialized data sequence from list of calc_ids and tdc_*_Data class
        data files in: results_vis_dir/fmci_id/data_dir/

        image_data_class
           Image_Data class for data intialization
        image_id
           image id
        --------
        Options:
        --------
        ii
           i_ts index interval <[i1,<i2>]>
           
        data class for each id is initialized as data_class(*args, **kwargs)
        """
        # initialize sequence with empty class
        seq = Image_Sequence(None, image_id, ii)
        # initialize data class
        filename = os.path.join(seq.dirname,
                                Image_Data.default_image_filename_format % seq.idx_seq__start)
        image_data = image_data_class.init_from_file(filename, **kwargs)
        # initialize sequence
        seq.image_data = image_data
        return seq

    
    def __getattr__(self,attrname):
        "Redirects all non-mplemented requests to the current data class"
        return getattr(self.image_data,attrname)
        
    def read(self,i_seq, **kwargs):
        "Perform read operation for the data[i_seq]"
        i_ts = (i_seq-1) + self.idx_seq__start
        self.image_data.read(i_ts)
        
    def get__id(self):
        "()=>id  current"
        return 0

    def get__i_ts(self):
        "()=>i_ts current"
        return self.image_data.i_im

       
        
        
