import os
import matplotlib.pyplot as plt

from ATvis.Common_Data_Plot import *

from Auxiliary            import *
from x_PlottingFunctions  import tdc_FMCI_XP_Manip
from FMCI                 import tdc_FMCI_XP_Partition__LinSemiLogUniform

# ============================================================
# Directory
# ============================================================
tdc_Filenames.set_results_dir('../RESULTS/WD2TB/Crab/')


# ============================================================
# IDs 
# ============================================================
ID='SCLF__Crab_B1_Dipole_jm1.5_P0.033_Chi60_L0.3_nGJ5e4_nx1e4_dt1e-5_sU'
particle='Electrons'
i_ts=480
wlims=[1e-2,11]
xlims=[-0.01,0.31]

ID='RS__Crab_B1_R8.6e6_jp1_P0.033_L0.2_nGJ5e4_nx1e4_dt8e-6_sU_a'
particle='Positrons'
i_ts=473
wlims=[1e-2,11]
xlims=[-0.01,0.21]



partition=tdc_FMCI_XP_Partition__LinSemiLogUniform( x_dict=dict(n=200,xx=None),
                                                    p_dict=dict(n=100,pp=[1,5e8]) )

manip_xp_fmci=tdc_FMCI_XP_Manip.init_from_data(ID,
                                               i_ts=i_ts,
                                               particle_name=particle,
                                               xp_partition=partition)
# make nice labels
# x-axis
manip_xp_fmci.plot(wlims=wlims)
manip_xp_fmci.set_xlim(xlims)
# y-axis
manip_xp_fmci.set_ylim( [-5e8,5e8] )
manip_xp_fmci.set_yticks( [-1e8,-1e4,0,1e4,1e8])

plt.show()










