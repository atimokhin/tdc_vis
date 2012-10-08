# for printing use dpi=600
#

import matplotlib.pyplot as plt
import numpy             as np

from Auxiliary        import *
from Common_Data_Plot import *

from Particles  import *
from Plots_MPP  import tdc_mpp__sed

import MPP

tdc_rcParams.set_hardcopy()

tdc_Filenames.set_results_dir('../RESULTS/FreeAgent/')

plot_flag = 'j1'


# ------------------------------------------------------------
# j=1
# ------------------------------------------------------------

if ( plot_flag == 'j1' ):
    ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU__3d_cycle'
    timeshots = [280, 370, 460]
    xxs = ( [0,0.135], [0.05,0.18], [0.1,0.225] )
    tick_and_labels_commands="""
mpp.set_xlim([.9,1e8])
mpp.set_xticks(np.logspace(0,7,8))
mpp.set_xticklabels(['10^{%g}' % np.log10(x) for x in np.logspace(0,7,8)])

mpp.set_ylim( (0,1), [8e-4,2e2] )
mpp.set_yticks( (0,1), np.logspace(-3,2,6) )
mpp.set_yticklabels( (0,1),['10^{%g}' % np.log10(x) for x in np.logspace(-3,2,6)])
"""
    
fig_style = dict( dx_pad_abs         = 0.07,
                  dy_pad_abs         = 0.07,
                  left_margin_abs    = 0.55,
                  bottom_margin_abs  = 0.37,
                  f_ylabel_left      = 0.0175,
                  f_xlabel_bottom    = 0.35 )
    
mpp = tdc_mpp__sed(ID, timeshots, xxs, **fig_style)
mpp.set_window_title(ID)
mpp.interactive_off()

# xlabels
for j in range(len(timeshots)):
    mpp.set_bottom_xlabel(j, r'$|p|$')

exec tick_and_labels_commands

mpp.interactive_on()

plt.show()
tdc_rcParams.set_default()
