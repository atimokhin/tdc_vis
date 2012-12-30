# for printing use dpi=600
#

import matplotlib.pyplot as plt
import numpy             as np

from ATvis.Common_Data_Plot import *

from Auxiliary        import *
from Common_Data_Plot import *

from x_PlottingFunctions.MPP      import tdc_mpp_v__e_n_fft
# -------------------------------


AT_rcParams.set_hardcopy()

tdc_Filenames.set_results_dir('../RESULTS/WD/_paper_TDC2')




plot_flag = 'wave1'


# ------------------------------------------------------------
# j=p0.5
# ------------------------------------------------------------

if ( plot_flag == 'wave1' ):
    ID='SCLF__jp0.5_Pcf1e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJConst__R6C_Xb0.7__dP5e-2_inj5_sU_P'
    ## timeshots = [833, 837, 844]
    timeshots = [832, 837, 842]
    ## timeshots = [834, 835, 836, 837, 838, 839]
    xx_discharge = [0.4,0.65] 
    ## xx_discharge = [0.35,0.7] 
    moving_grid_dict = None
    tick_and_labels_commands="""
mpp.set_xlim_columns([0,2],[0.33,0.75])
mpp.set_xlim_columns([1],[3,3e3])

mpp.set_xticks_columns([0,2],[.4, .5, .6, .7])
mpp.set_xticklabels_columns([0,2],['.4', '.5', '.6', '.7'])

mpp.set_ylim(0,[-0.24,0.24])
mpp.set_yticks( 0, [-.2,0,.2] )
mpp.set_yticklabels( 0, ['-.2','0','.2'] )
mpp.set_yticks( 0, np.arange(-.22,.23,.02), minor=True )

mpp.set_ylim(2,[-24,24])
mpp.set_yticks( 2, [-20,0,20] )
mpp.set_yticklabels( 2, ['-20','0','20'] )
mpp.set_yticks( 2, np.arange(-22,23,2), minor=True )

mpp.set_ylim([1],[1e-5,1e4])
mpp.set_yticks(1,[1e-3,1,1e3],minor=False)
mpp.set_yticks(1,[1e-4,1e-2,1e-1,1e1,1e2],minor=True)
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
paramMPP_WavePropagation_MNRAS['dx_pad_abs']      = .35;
paramMPP_WavePropagation_MNRAS['dy_pad_abs']      = .05;
paramMPP_WavePropagation_MNRAS['left_margin_abs'] = .7;
paramMPP_WavePropagation_MNRAS['bottom_margin_abs'] = 0.4; 

    
mpp = tdc_mpp_v__e_n_fft(ID,timeshots,
                         xx_discharge,
                         moving_grid_dict,
                         fig_param=paramMPP_WavePropagation_MNRAS)
mpp.set_window_title(ID)
mpp.interactive_off()

# xlabels
mpp.set_bottom_xlabel(0, r'$x$')
mpp.set_bottom_xlabel(1, r'$k$')
mpp.set_bottom_xlabel(2, r'$x$')

exec tick_and_labels_commands

mpp.interactive_on()

plt.show()
AT_rcParams.set_default()
