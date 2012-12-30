# for printing use dpi=600
#

import matplotlib.pyplot as plt
import numpy             as np

from ATvis.Common_Data_Plot import *

from Auxiliary        import *
from Common_Data_Plot import *

from Particles  import *
from Plots_MPP  import tdc_mpp_v__e_rho_n

import ATvis.MPP

AT_rcParams.set_hardcopy()

tdc_Filenames.set_results_dir('../RESULTS/FreeAgent/')




plot_flag = 'wave1'


# ------------------------------------------------------------
# j=1
# ------------------------------------------------------------

if ( plot_flag == 'wave1' ):
    ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU__3d_cycle'
    timeshots = [310, 320, 330, 340, 350, 360]
    moving_grid_dict = dict(n_lines=11, speed=1, extend_grid_y=[-15,15])
    tick_and_labels_commands="""
mpp.set_xlim([0,0.18])
mpp.set_xticks([0, .05, .1, .15])
mpp.set_xticklabels(['0', '.05', '.1', '.15'])
mpp.set_xticks(np.arange(0,.19,0.01), minor=True)

mpp.set_ylim(0,[-0.12,0.12])
mpp.set_yticks( 0, [-.1,0,.1] )
mpp.set_yticklabels( 0, ['-.1','0','.1'] )
mpp.set_yticks( 0, np.arange(-.12,.13,.01), minor=True )

mpp.set_ylim(1,[-9,9])
mpp.set_yticks( 1, [-5,0,5] )
mpp.set_yticklabels( 1, ['-5','0','5'] )
mpp.set_yticks(1,np.arange(-9,10,1), minor=True)

mpp.set_ylim(2,[-40,40])
mpp.set_yticks( 2, [-20,0,20] )
mpp.set_yticklabels( 2, ['-20','0','20'] )
mpp.set_yticks( 2, np.arange(-35,40,5), minor=True )
"""
    
    
mpp = tdc_mpp_v__e_rho_n(ID,timeshots,
                         moving_grid_dict,
                         aspect_ratio    = 2.4,
                         dx_pad_abs      = .26,
                         dy_pad_abs      = .05,
                         left_margin_abs = .7,
                         f_ylabel_left   = .05)
mpp.set_window_title(ID)
mpp.interactive_off()

# xlabels
for j in range(3):
    mpp.set_bottom_xlabel(j, r'$x$')

exec tick_and_labels_commands

mpp.interactive_on()

plt.show()
AT_rcParams.set_default()
