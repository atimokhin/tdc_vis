import os
import numpy as np

from Auxiliary        import *
from Common_Data_Plot import tdc_Sequence

from tdc_fmci_xp_data import tdc_FMCI_XP_Data_Base


class tdc_FMCI_Sequence(tdc_Sequence):
    """
    Data sequence for FMCI Data classes
    initialized from directory containing FMCI ascii data files
    """

    _default_index_filename = 'index.txt'
    
    def __init__(self, fmci_xp, fmci_id, data_dir, ii=None):
        """
        Intialized data sequence from list of fmci_xps objects
        data files in: results_vis_dir/fmci_id/data_dir/

        fmci_xp
           instance of tdc_FMCI_*_Data class for data intialization
        fmci_id
           fmci id
        data_dir
           sub directory of fmci_id with data files
        --------
        Options:
        --------
        ii
           i_ts index interval <[i1,<i2>]>           
        """
        self.dirname = os.path.join(tdc_Filenames.get_results_dir(),fmci_id, data_dir)
        # read data from index file
        filename = os.path.join(self.dirname,self._default_index_filename)
        try:
            f=open(filename,'r')
        except IOError:
            raise tdc_Exception( 'Cannot open \"%s\"' % filename )
        self.array_idx=np.loadtxt(f, dtype=np.int32)
        f.close()
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
        self.fmci_xp = fmci_xp

    @staticmethod
    def init_from_data(fmci_data_class, fmci_id, data_dir, ii=None, **kwargs):
        """
        Intialized data sequence from list of calc_ids and tdc_*_Data class
        data files in: results_vis_dir/fmci_id/data_dir/

        fmci_data_class
           tdc_FMCI_*_Data class for data intialization
        fmci_id
           fmci id
        data_dir
           sub directory of fmci_id with data files
        --------
        Options:
        --------
        ii
           i_ts index interval <[i1,<i2>]>
           
        data class for each id is initialized as data_class(*args, **kwargs)
        """
        # initialize sequence with empty class
        seq = tdc_FMCI_Sequence(None, fmci_id, data_dir, ii)
        # initialize data class
        filename = os.path.join(seq.dirname,
                                tdc_FMCI_XP_Data_Base.default_ascii_filename_format % seq.idx_seq__start)
        fmci_data = fmci_data_class.init_from_ascii(filename, **kwargs)
        # initialize sequence
        seq.fmci_xp = fmci_data
        return seq

    
    def __getattr__(self,attrname):
        "Redirects all non-mplemented requests to the current data class"
        return getattr(self.fmci_xp,attrname)
        
    def read(self,i_seq, **kwargs):
        "Perform read operation for the data[i_seq]"
        i_ts = (i_seq-1) + self.idx_seq__start
        self.fmci_xp.read(i_ts)
        
    def get__id(self):
        "()=>id  current"
        return 0

    def get__i_ts(self):
        "()=>i_ts current"
        return self.fmci_xp.i_ts
       
        
        
