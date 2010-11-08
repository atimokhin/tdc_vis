import matplotlib.pyplot as plt
import numpy             as np

from Common import *
from Fluxes import *

from single_figure_style import fig_style

tdc_set_hardcopy_rcparams()

tdc_set_results_dir('../RESULTS/FreeAgent/')

plot_flag = 'j1.0'


# ------------------------------------------------------------
# j=1
# ------------------------------------------------------------
tick_and_labels_commands="""
manip_e.set_xlim([3,12])
manip_e.set_xticks(range(4,12))                
manip_e.set_xticklabels(['%g' % i  for i in range(4,12)])   
manip_e.set_xticks(np.arange(3,12,0.1), minor=True)

manip_e.set_ylim([6e4,6e8])
manip_e.set_yticks( [1e5,1e6,1e7,1e8] )
manip_e.set_yticklabels( ['10^5','10^6','10^7','10^8'] )
"""

if ( plot_flag == 'j1.0' ):
    IDs=['RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU',
         'RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU__1']

elif ( plot_flag == 'j0.5' ):
    IDs=['RS_1_R6_jp0.5_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU']

elif ( plot_flag == 'j1.5' ):
    IDs=['RS_1_R6_jp1.5_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU']




manip_e=tdc_plot_fluxes(IDs,'Energy',no_plot=True,**fig_style)
manip_e.interactive_off()

manip_e.smooth(window_len=10)
manip_e.semilogy()

exec tick_and_labels_commands

manip_e.interactive_on()
plt.show()
tdc_set_default_rcparams()
