# for printing use dpi=600
#

import matplotlib.pyplot as plt
import numpy             as np

from Auxiliary        import *
from Common_Data_Plot import *

## from Particles  import *
from Plots_MPP  import tdc_mpp_v__e_fft_discharge

import MPP

tdc_set_hardcopy_rcparams()

tdc_set_results_dir('../RESULTS/WD/')



plot_flag = 'wave1'


# ------------------------------------------------------------
# j=p0.5
# ------------------------------------------------------------

if ( plot_flag == 'wave1' ):
    ID='SCLF__jp0.5_Pcf1e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJConst__R6C_Xb0.7__dP5e-2_inj5_sU_P'
    ## timeshots = [834, 835, 836, 837, 838, 839]
    ## timeshots = [825, 829, 833, 837, 840, 844, 848]
    # Presentation
    timeshots = [825, 829, 833, 837, 844]
    xx_discharge = [0.35,0.65] 
    xx_out = [0,0.25] 
    moving_grid_dict = dict(n_lines=22, speed=1, extend_grid_y=[-18,18])
    tick_and_labels_commands="""
mpp.set_xlim_columns([1,2],[1.1,5e3])

mpp.set_ylim(0,[-0.3,0.7])
## mpp.set_yticks( 0, [-.1,0,.1] )
## mpp.set_yticklabels( 0, ['-.1','0','.1'] )
## mpp.set_yticks( 0, np.arange(-.18,.19,.02), minor=True )

mpp.set_ylim(1,[2e-5,3e4])
## mpp.set_yticks( 1, [-5,0,5] )
## mpp.set_yticklabels( 1, ['-5','0','5'] )
## mpp.set_yticks(1,np.arange(-4,4,1), minor=True)

mpp.set_ylim(2,[2e-9,2e-3])
## mpp.set_yticks( 2, [-10,0,10] )
## mpp.set_yticklabels( 2, ['-10','0','10'] )
## mpp.set_yticks( 2, np.arange(-16,18,2), minor=True )
"""
#presentation
    tick_and_labels_commands="""
mpp.set_xlim_columns([1,2],[1.1,5e3])

mpp.set_ylim(0,[-0.3,0.7])
## mpp.set_yticks( 0, [-.1,0,.1] )
## mpp.set_yticklabels( 0, ['-.1','0','.1'] )
## mpp.set_yticks( 0, np.arange(-.18,.19,.02), minor=True )

mpp.set_ylim((1,2),[2e-7,3e4])
mpp.set_yticks((1,2),[1e-6,1e-3,1,1e3],minor=False)
mpp.set_yticks((1,2),[1e-7,1e-5,1e-4,1e-2,1e-1,10,100,1e4],minor=True)
"""



# ------------------------------------------------------------
# j=m2.0
# ------------------------------------------------------------

if ( plot_flag == 'wave2' ):
    ID='Arons__j2.000_Pcf9e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJlin2_A1_AAm0.7_X1__R6C__dP5e-2_inj12_sU__wave'
    ## timeshots = [45, 49, 53, 57, 61, 65]
    ## timeshots = [26, 43, 50, 57, 64, 71, 88]
    # Presentation
    timeshots = [26, 50, 57, 64, 88]
    xx_discharge = [0.15,0.4] 
    xx_out = [0.4,1] 
    moving_grid_dict = dict(n_lines=22, speed=1, extend_grid_y=[-18,18])
    tick_and_labels_commands="""
mpp.set_xlim_columns([1,2],[1.1,5e3])

mpp.set_ylim(0,[-0.055,0.055])
mpp.set_yticks( 0, np.arange(-.04,.05,.02) )
mpp.set_yticklabels( 0, ['-.04','-.02','0','.02','.04'] )
## mpp.set_yticks( 0, np.arange(-.18,.19,.02), minor=True )

mpp.set_ylim(1,[3e-7,3e2])
## mpp.set_yticks( 1, [-5,0,5] )
## mpp.set_yticklabels( 1, ['-5','0','5'] )
## mpp.set_yticks(1,np.arange(-4,4,1), minor=True)

mpp.set_ylim(2,[3e-7,3e2])
## mpp.set_yticks( 2, [-10,0,10] )
## mpp.set_yticklabels( 2, ['-10','0','10'] )
## mpp.set_yticks( 2, np.arange(-16,18,2), minor=True )
"""
#presentation
    tick_and_labels_commands="""
mpp.set_xlim_columns([1,2],[1.1,5e3])

mpp.set_ylim(0,[-0.055,0.055])
mpp.set_yticks( 0, np.arange(-.04,.05,.02) )
mpp.set_yticklabels( 0, ['-.04','-.02','0','.02','.04'] )

mpp.set_ylim((1,2),[2e-7,3e4])
mpp.set_yticks((1,2),[1e-6,1e-3,1,1e3],minor=False)
mpp.set_yticks((1,2),[1e-7,1e-5,1e-4,1e-2,1e-1,10,100,1e4],minor=True)
"""
    
paramMPP_WavePropagation_MNRAS = paramMPP_MNRAS.copy()

paramMPP_WavePropagation_MNRAS['aspect_ratio']    = 2.4;
paramMPP_WavePropagation_MNRAS['dx_pad_abs']      = .35;
paramMPP_WavePropagation_MNRAS['dy_pad_abs']      = .05;
paramMPP_WavePropagation_MNRAS['left_margin_abs'] = .7;
paramMPP_WavePropagation_MNRAS['bottom_margin_abs'] = 0.4; 
    
mpp = tdc_mpp_v__e_fft_discharge(ID,
                                 timeshots,
                                 xx_discharge,
                                 xx_out,
                                 fig_param=paramMPP_WavePropagation_MNRAS)
mpp.set_window_title(ID)
mpp.interactive_off()

# xlabels
mpp.set_bottom_xlabel(0, r'$x$')
mpp.set_bottom_xlabel(1, r'$k$')
mpp.set_bottom_xlabel(2, r'$k$')

mpp._delete_xlabels_for_middle_plots()

exec tick_and_labels_commands

mpp.interactive_on()

plt.show()
tdc_set_default_rcparams()
