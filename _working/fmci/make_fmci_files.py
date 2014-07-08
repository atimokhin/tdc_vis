#!/usr/bin/python
if __name__ == '__main__':
    import tdc_vis

import os

from ATvis.Common_Data_Plot import *

from Auxiliary           import *
from x_DataFunctions     import *

from FMCI                import tdc_FMCI_XP_Partition__LinSemiLogUniform


# ============================================================
# Directory
# ============================================================
# ------------------------------------------------------------ 
# TDC data will be read from this directory
# ------------------------------------------------------------
# tdc_Filenames.set_results_dir('../RESULTS/')
# tdc_Filenames.set_results_dir('../RESULTS/WD1TB')
tdc_Filenames.set_results_dir('../RESULTS/WD2TB/Crab')
# tdc_Filenames.set_results_dir('../RESULTS/WD2TB/Test')

# ------------------------------------------------------------ 
# FMCI files will be writtent in this directory:
# ------------------------------------------------------------
# tdc_Filenames.set_vis_results_dir('../RESULTS_FMCI/')
# tdc_Filenames.set_vis_results_dir('../RESULTS_FMCI/Crab/')
tdc_Filenames.set_vis_results_dir('../RESULTS_FMCI/Crab/HiRes')


# ============================================================
# IDs 
# ============================================================
# ID='RS__Crab_B3_Dipole_jp1_P0.033_L0.2_nGJ5e4_nx5e3_dt1.5e-5_sU'
# ID='RS__Crab_B3_Dipole_jp1_P0.033_L0.2_nGJ5e4_nx1e4_dt8e-6_sU'
# ID='RS__Crab_B1_Dipole_jp1_P0.033_L0.2_nGJ5e4_nx5e3_dt1.5e-5_sU__test_debug_3_MC'

# ID='RS__Crab_B3_Rc2e6_jp1_P0.033_L0.2_nGJ5e4_nx1e4_dt8e-6_sU'
# ID='RS__Crab_B3_Dipole_jp1_P0.033_L0.2_nGJ5e4_nx1e4_dt8e-6_sU_a'
# ID='RS__Crab_B3_Dipole_theta0.5_jp1_P0.033_L0.2_nGJ5e4_nx1e4_dt8e-6_sU_a'
# ID='RS__Crab_B1_Dipole_jp1_P0.033_L0.2_nGJ5e4_nx1e4_dt8e-6_sU_a'
# ID='RS__Crab_B1_Dipole_theta0.5_jp1_P0.033_L0.2_nGJ5e4_nx1e4_dt8e-6_sU_a'
# ID='RS__Crab_B3_R8.6e6_jp1_P0.033_L0.2_nGJ5e4_nx1e4_dt8e-6_sU_a'
# ID='RS__Crab_B1_R8.6e6_jp1_P0.033_L0.2_nGJ5e4_nx1e4_dt8e-6_sU_a'

# ID='SCLF__Crab_B1_Dipole_jp1.5_P0.033_L0.2_nGJ5e4_nx1e4_dt8e-6_sU_a'
# ID='SCLF__Crab_B1_Dipole_jm1.5_P0.033_L0.2_nGJ5e4_nx1e4_dt8e-6_sU_a'

ID='SCLF__Crab_B1_Dipole_jm1.5_P0.033_Chi60_L0.3_nGJ5e4_nx1e4_dt1e-5_sU'


# ============================================================
# parameters:
# ============================================================
particles = ['Electrons', 'Positrons', 'Pairs']
# partition = tdc_FMCI_XP_Partition__LinSemiLogUniform( x_dict=dict(n=200,xx=None),
#                                                       p_dict=dict(n=100,pp=[5,5e8]) )
partition = tdc_FMCI_XP_Partition__LinSemiLogUniform( x_dict=dict(n=100,xx=None),
                                                      p_dict=dict(n=50,pp=[5,5e8]) )
# i_ts__range=[295,315]
i_ts__range=None
# ============================================================




def do_files():
    mk_fmci=tdc_FMCI_DataFiles_Maker(ID,
                                     particles=particles,
                                     partition=partition)
    mk_fmci.make_files(i_ts__range=i_ts__range)
    

if __name__ == "__main__":
    do_files()
