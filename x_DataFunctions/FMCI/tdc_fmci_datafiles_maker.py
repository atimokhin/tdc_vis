from __future__ import print_function

import numpy as np
import os
import glob

from Auxiliary import tdc_Filenames, tdc_TimeInfo

from FMCI import tdc_FMCI_XP_Partition__LinSemiLogUniform
from FMCI import tdc_FMCI_XP_Data


class tdc_FMCI_DataFiles_Maker(object):
    """
    Class for reading particle data from TDC simulations and
    creating of FMCI files
    """

    __default_particles = ['Electrons', 'Positrons', 'Pairs']
    __default_partition = tdc_FMCI_XP_Partition__LinSemiLogUniform( x_dict=dict(n=90,xx=None),
                                                                    p_dict=dict(n=30,pp=[1,1e8]) )
    _index_filename = 'index.txt'
    
    def __init__(self, 
                 calc_id,
                 particles=None,
                 partition=None):
        """
        """
        self.calc_id = calc_id
        self.data_top_dir = tdc_Filenames.get_vis_results_dir() + 'FMCI__%s' % calc_id
        # set particles -----------------------
        self.particles = self.__default_particles if particles is None else particles 
        # default__i_ts__range to all i_ts ----
        timeinfo=tdc_TimeInfo(calc_id,self.particles[0]+'.h5')
        i_ts_max = timeinfo.get_number_of_ts()
        self.default__i_ts__range = [1,i_ts_max+1,1]
        # set partition -----------------------
        self.partition = self.__default_partition if partition is None else partition

    def make_files(self, i_ts__range=None):
        """
        Reads data and creates FMCI files and directories
        """
        if i_ts__range is not None:
            i_ts__range[0] = max(1, i_ts__range[0])
            i_ts__range[1] = min(i_ts__range[1],self.default__i_ts__range[1])
            i_ts_array = np.arange(*i_ts__range)
        else:
            i_ts_array = np.arange(*self.default__i_ts__range)
        # iterates over particles
        for p in self.particles:
            # if data directory exists, remove all files from it,
            # otherwise create it
            data_dir = os.path.join(self.data_top_dir, '%s' % p)
            if os.path.exists(data_dir):
                [ os.remove(f) for f in glob.glob(data_dir+os.sep+'*') ]
            else:
                os.makedirs(data_dir)
            # initialise data class
            fmci_xp=tdc_FMCI_XP_Data(self.calc_id, p, self.partition)
            print("i_ts=", end="")
            # open index file
            index_file = open( os.path.join(data_dir,self._index_filename), "w")
            for i_ts in i_ts_array:
                print(" %d," % i_ts, end="")
                fmci_xp.read(i_ts,print_progress=False)
                filename = os.path.join( data_dir, fmci_xp.default_ascii_filename_format % i_ts )
                fmci_xp.save_to_ascii(filename,print_progress=False)
                # write i_ts to index file
                index_file.write("%d\n" % i_ts)
            index_file.close()
