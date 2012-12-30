import matplotlib.pyplot as plt
import numpy             as np

from ATvis.Common_Data_Plot import *

from Auxiliary        import *
from Common_Data_Plot import *

from Plot_CMD import *

from single_figure_style import fig_style

AT_rcParams.set_hardcopy()

tdc_Filenames.set_results_dir('../RESULTS/FreeAgent/')

plot_flag = 'j1.0'


if ( plot_flag == 'j1.0' ):
    IDs=['RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU',
         'RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU__1']
    tick_and_labels_commands="""
manip_j.set_xlim([3,12])
manip_j.set_xticks(range(4,12))                
manip_j.set_xticklabels(['%g' % i  for i in range(4,12)])   
manip_j.set_xticks(np.arange(3.1,12,0.1), minor=True)

manip_j.set_ylim([-9,9])
manip_j.set_yticks( [-5,0,5] )
manip_j.set_yticklabels( ['-5','0','5'] )
manip_j.set_yticks(np.arange(-9,10,1), minor=True)
"""

elif ( plot_flag == 'j0.5' ):
    IDs=['RS_1_R6_jp0.5_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU']
    tick_and_labels_commands="""
manip_j.set_xlim([3.6,12.6])
manip_j.set_xticks(range(4,13))                
manip_j.set_xticklabels(['%g' % i  for i in range(4,13)])   
manip_j.set_xticks(np.arange(3.7,12.6,0.1), minor=True)

manip_j.set_ylim([-3.5,3.5])
manip_j.set_yticks( [-3,-2,-1,0,1,2,3] )
manip_j.set_yticklabels( ['','-2','','0','','2',''] )
"""

elif ( plot_flag == 'j1.5' ):
    IDs=['RS_1_R6_jp1.5_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU']
    tick_and_labels_commands="""
manip_j.set_xlim([2.4,11.4])
manip_j.set_xticks(range(3,12))                
manip_j.set_xticklabels(['%g' % i  for i in range(3,12)])   
manip_j.set_xticks(np.arange(2.5,11.5,0.1), minor=True)

manip_j.set_ylim([-9,9])
manip_j.set_yticks( [-5,0,5] )
manip_j.set_yticklabels( ['-5','0','5'] )
manip_j.set_yticks(np.arange(-9,10,1), minor=True)
"""



# uncomment this to get big picture
#fig_style = {}

manip_j=tdc_plot_fluxes(IDs,'J',no_plot=True,**fig_style)
manip_j.interactive_off()

manip_j.smooth(window_len=10)
manip_j.plot()

exec tick_and_labels_commands

manip_j.interactive_on()
plt.show()
AT_rcParams.set_default()
