# for printing use dpi=600
#

import matplotlib.pyplot as plt
import numpy             as np

from ATvis.Common_Data_Plot import *

from Auxiliary        import *
from Common_Data_Plot import *

from x_PlottingFunctions.MPP      import tdc_mpp_v__e_rho_n
# -------------------------------


AT_rcParams.set_hardcopy()

tdc_Filenames.set_results_dir('../RESULTS/WD/_paper_TDC2')




plot_flag = 'wave2'


# ------------------------------------------------------------
# j=p0.5
# ------------------------------------------------------------

if ( plot_flag == 'wave1' ):
    ID='SCLF__jp0.5_Pcf1e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJConst__R6C_Xb0.7__dP5e-2_inj5_sU_P'
    timeshots = [834, 835, 836, 837, 838, 839]
    moving_grid_dict = dict(n_lines=22, speed=1, extend_grid_y=[-18,18])
    tick_and_labels_commands="""
mpp.set_xlim([0.33,0.75])
mpp.set_xticks([.4, .5, .6, .7])
mpp.set_xticklabels(['.4', '.5', '.6', '.7'])
#mpp.set_xticks(np.arange(0,.19,0.01), minor=True)

mpp.set_ylim(0,[-0.195,0.195])
mpp.set_yticks( 0, [-.1,0,.1] )
mpp.set_yticklabels( 0, ['-.1','0','.1'] )
mpp.set_yticks( 0, np.arange(-.18,.19,.02), minor=True )

mpp.set_ylim(1,[-6,6])
mpp.set_yticks( 1, [-5,0,5] )
mpp.set_yticklabels( 1, ['-5','0','5'] )
mpp.set_yticks(1,np.arange(-6,7,1), minor=True)

mpp.set_ylim(2,[-17,17])
mpp.set_yticks( 2, [-10,0,10] )
mpp.set_yticklabels( 2, ['-10','0','10'] )
mpp.set_yticks( 2, np.arange(-16,18,2), minor=True )
"""

# ------------------------------------------------------------
# j=m2.0
# ------------------------------------------------------------

if ( plot_flag == 'wave2' ):
    ID='Arons__j2.000_Pcf9e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJlin2_A1_AAm0.7_X1__R6C__dP5e-2_inj12_sU__wave'
    timeshots = [45, 49, 53, 57, 61, 65]
    moving_grid_dict = dict(n_lines=22, speed=1, extend_grid_y=[-18,18])
    tick_and_labels_commands="""
mpp.set_xlim([-0.01,0.41])
mpp.set_xticks([0, .1, .2, .3, .4])
mpp.set_xticklabels(['0', '.1', '.2', '.3', '.4'])
## mpp.set_xticks(np.arange(0,.19,0.01), minor=True)

mpp.set_ylim(0,[-0.03,0.03])
mpp.set_yticks( 0, [-.02,0,.02] )
mpp.set_yticklabels( 0, ['-.02','0','.02'] )
mpp.set_yticks( 0, np.arange(-.01,.02,.01), minor=True )

mpp.set_ylim(1,[-2.5,.5])
mpp.set_yticks( 1, [-2,-1,0] )
mpp.set_yticklabels( 1, ['-2','-1','0'] )
mpp.set_yticks(1,np.arange(-1.8,0.5,0.2), minor=True)

mpp.set_ylim(2,[-7,7])
mpp.set_yticks( 2, [-5,0,5] )
mpp.set_yticklabels( 2, ['-5','0','5'] )
mpp.set_yticks( 2, np.arange(-6,7,1), minor=True )
"""
    
paramMPP_WavePropagation_MNRAS = paramMPP_MNRAS.copy()

paramMPP_WavePropagation_MNRAS['aspect_ratio']    = 2.4;
paramMPP_WavePropagation_MNRAS['dx_pad_abs']      = .26;
paramMPP_WavePropagation_MNRAS['dy_pad_abs']      = .05;
paramMPP_WavePropagation_MNRAS['left_margin_abs'] = .7;

    
mpp = tdc_mpp_v__e_rho_n(ID,timeshots,
                         moving_grid_dict,
                         fig_param=paramMPP_WavePropagation_MNRAS)
mpp.set_window_title(ID)
mpp.interactive_off()

# xlabels
for j in range(3):
    mpp.set_bottom_xlabel(j, r'$x$')

exec tick_and_labels_commands

mpp.interactive_on()

plt.show()
AT_rcParams.set_default()
