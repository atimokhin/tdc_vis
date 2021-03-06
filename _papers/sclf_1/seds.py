if __name__ == '__main__':
    import tdc_vis

import matplotlib.pyplot as plt
import numpy             as np

from ATvis.Common_Data_Plot import *

from Auxiliary        import *
from Common_Data_Plot import *

from x_PlottingFunctions.MPP      import tdc_mpp__sed
# ---------------------------------


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
AT_rcParams.set_hardcopy()
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# ---------------------------------
tdc_Filenames.set_results_dir('../RESULTS/WD/_paper_TDC2')
# ---------------------------------


plot_flag = 'jm1.5'
# plot_flag = 'jp0.5'
# plot_flag = 'jp1.5'


# ------------------------------------------------------------
# j=-1.5
# ------------------------------------------------------------
if ( plot_flag == 'jm1.5' ):
    ID='SCLF__jm1.5_Pcf1e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJConst__R6C_Xb0.7__dP5e-2_inj8_s1'
    timeshots = [483, 495, 506]
    xxs = ( [0,0.795], [0,1], [0,1] )
    tick_and_labels_commands="""
mpp.set_xlim([.9,1e8])
mpp.set_xticks(np.logspace(0,7,8))
mpp.set_xticklabels(['$10^{%g}$' % np.log10(x) for x in np.logspace(0,7,8)])

mpp.set_ylim( (0,1), [8e-4,2e2] )
mpp.set_yticks( (0,1), np.logspace(-3,2,6) )
mpp.set_yticklabels( (0,1),['$10^{%g}$' % np.log10(x) for x in np.logspace(-3,2,6)])
"""
    
# ------------------------------------------------------------
# j=0.5
# ------------------------------------------------------------
elif ( plot_flag == 'jp0.5' ):
    ID='SCLF__jp0.5_Pcf1e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJConst__R6C_Xb0.7__dP5e-2_inj5_sU_P'
    timeshots = [836, 852, 872]
    xxs = ( [0,0.7], [0,0.75], [0,0.85] )
    tick_and_labels_commands="""
mpp.set_xlim([.9,1e8])
mpp.set_xticks(np.logspace(0,7,8))
mpp.set_xticklabels(['$10^{%g}$' % np.log10(x) for x in np.logspace(0,7,8)])

mpp.set_ylim( (0,1), [8e-4,2e2] )
mpp.set_yticks( (0,1), np.logspace(-3,2,6) )
mpp.set_yticklabels( (0,1),['$10^{%g}$' % np.log10(x) for x in np.logspace(-3,2,6)])
"""

# ------------------------------------------------------------
# j=1.5
# ------------------------------------------------------------
elif ( plot_flag == 'jp1.5' ):
    ID='SCLF__jp1.5_Pcf1e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJConst__R6C_Xb0.7__dP5e-2_inj7_sU'
    timeshots = [657, 674, 694]
    xxs = ( [0,0.75], [0,0.88], [0,1] )
    tick_and_labels_commands="""
mpp.set_xlim([.9,1e8])
mpp.set_xticks(np.logspace(0,7,8))
mpp.set_xticklabels(['$10^{%g}$' % np.log10(x) for x in np.logspace(0,7,8)])

mpp.set_ylim( (0,1), [8e-4,2e2] )
mpp.set_yticks( (0,1), np.logspace(-3,2,6) )
mpp.set_yticklabels( (0,1),['$10^{%g}$' % np.log10(x) for x in np.logspace(-3,2,6)])
"""
    
fig_param = dict( dx_pad_abs         = 0.07,
                  dy_pad_abs         = 0.07,
                  left_margin_abs    = 0.65,
                  bottom_margin_abs  = 0.37,
                  f_ylabel_left      = 0.0175)
    
mpp = tdc_mpp__sed(ID, timeshots, xxs, fig_param=fig_param)
mpp.set_window_title(ID)
mpp.interactive_off()

# xlabels
for j in range(len(timeshots)):
    mpp.set_bottom_xlabel(j, r'$|p|$')
# ylabels
ylabel=r'$\displaystyle{}p\:\frac{\partial\!n}{\partial{}\!p}$'
mpp.set_ylabel(0,ylabel)
mpp.set_ylabel(1,ylabel)

exec tick_and_labels_commands

mpp.interactive_on()

plt.show()

plt.interactive(True)
