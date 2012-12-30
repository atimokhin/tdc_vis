# for printing use dpi=600
#

import matplotlib.pyplot as plt
import numpy             as np

from Auxiliary        import *
from Common_Data_Plot import *

from Particles  import *
from Plots_MPP  import tdc_mpp__n_rho_e_xp

import ATvis.MPP

tdc_Filenames.set_results_dir('../RESULTS/FreeAgent/')



plot_flag = 'cts_paper_1'
plot_flag = 'cts_paper_2'

#plot_flag = 'poster2'

if ( plot_flag == 'cts_paper_1' ):
    ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU__3d_cycle'
    timeshots1 = [10, 70, 130]
    sample_dict=dict(name='regular',n_reduce=1,n_min=400)
    tick_and_labels_commands="""
mpp.set_xlim([0,.3])
mpp.set_xticks([0,.1,.2])
mpp.set_xticklabels(['0','.1','.2'])
mpp.set_xticks(np.arange(0,.3,0.05), minor=True)

mpp.set_ylim( 0, [-1.1,2.1] )
mpp.set_yticks( 0, [-1,0,1,2] )
mpp.set_yticklabels( 0, ['-1','0','1','2'] )
mpp.set_yticks( 0, np.arange(-1,2.1,.5), minor=True )

mpp.set_ylim( 1, [-1.1,2.1] )
mpp.set_yticks(1,[-1,0,1,2])
mpp.set_yticklabels( 1, ['-1','0','1','2'] )
mpp.set_yticks(1,np.arange(-1,2.1,.5), minor=True)

mpp.set_ylim( 2, [-.1,1.1] )
mpp.set_yticks( 2, [0,1] )
mpp.set_yticklabels( 2, ['0','1'] )
mpp.set_yticks( 2, np.arange(-0.1,1.1,.1), minor=True )

mpp.set_ylim( 3, [-.2e7,1.1e7] )
mpp.set_yticks( 3, [0,1e7] )
mpp.set_yticklabels( 3, ['0','10^7'] )
mpp.set_yticks( 3, np.arange(-.2e7,1.1e7,1e6), minor=True )

mpp.set_ylim( 4, [-1.1e7,.2e7] )
mpp.set_yticks( 4, [-1e7,0] )
mpp.set_yticklabels( 4, ['-10^7','0'] )
mpp.set_yticks( 4, np.arange(-1.1e7,.3e7,1e6), minor=True )

mpp.set_ylim( 5, [-6e4,6e4] )
mpp.set_yticks( 5, [-5e4,0,5e4] )
mpp.set_yticklabels( 5, ['-10^4','0','10^4'] )
mpp.set_yticks( 5, np.arange(-5e4,6e4,1e4), minor=True )
"""
    
elif ( plot_flag == 'cts_paper_2' ):
    ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU__3d_cycle'
    timeshots1 = [190, 280, 370, 460]
    sample_dict=dict(name='regular',n_reduce=2,n_min=400)
    tick_and_labels_commands="""
mpp.set_xlim([0,.3])
mpp.set_xticks([0,.1,.2])
mpp.set_xticklabels(['0','.1','.2'])
mpp.set_xticks(np.arange(0,.3,0.05), minor=True)

mpp.set_ylim(0, [-150,150])
mpp.set_yticks(0, [-100,0,100])
mpp.set_yticklabels(0, ['-100','0','100'])

mpp.set_ylim(1, [-69,69])
mpp.set_yticks(1, [-50,0,50])
mpp.set_yticks(1, np.arange(-70,70,10), minor=True)
mpp.set_yticklabels(1, ['-50','0','50'])

mpp.set_ylim( 2, [-.2,1.1] )
mpp.set_yticks( 2, [0,1] )
mpp.set_yticks( 2, np.arange(-0.2,1.2,.1), minor=True )

mpp.set_ylim( 3, [-.2e7,1.4e7] )
mpp.set_yticks( 3, [0,1e7] )
mpp.set_yticklabels( 3, ['0','10^7'] )
mpp.set_yticks( 3, np.arange(-.2e7,1.5e7,1e6), minor=True )

mpp.set_ylim( 4, [-1.4e7,.2e7] )
mpp.set_yticks( 4, [-1e7,0] )
mpp.set_yticklabels( 4, ['-10^7','0'] )
mpp.set_yticks( 4, np.arange(-1.4e7,.3e7,1e6), minor=True )

mpp.set_ylim( 5, [-6e5,6e5] )
mpp.set_yticks( 5, [-5e5,0,5e5] )
mpp.set_yticklabels( 5, ['-10^5','0','10^5'] )
mpp.set_yticks( 5, np.arange(-5e5,6e5,1e5), minor=True )
"""

elif ( plot_flag == 'poster1' ):
    ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU'
    timeshots1 = [581, 585, 589]
    sample_dict=dict(name='regular',n_reduce=1,n_min=400)
    tick_and_labels_commands="""
mpp.set_xlim([0,.3])
mpp.set_xticks([0,.1,.2])
mpp.set_xticklabels(['0','.1','.2'])
mpp.set_xticks(np.arange(0,.3,0.05), minor=True)

mpp.set_ylim( 0, [-7,7] )
mpp.set_yticks( 0, [-5,0,5] )
mpp.set_yticks( 0, np.arange(-6,7,1), minor=True )

mpp.set_ylim( 1, [-2.5,4.5] )
mpp.set_yticks(1,[0,3])
mpp.set_yticks(1,np.arange(-2,5,1), minor=True)

mpp.set_ylim( 2, [-.5,1.2] )
mpp.set_yticks( 2, [0,1] )
mpp.set_yticks( 2, np.arange(-0.5,1.6,.1), minor=True )

mpp.set_ylim( 3, [-.2e7,1.5e7] )
mpp.set_yticks( 3, [0,1e7] )
mpp.set_yticklabels( 3, ['0','10^7'] )
mpp.set_yticks( 3, np.arange(-.2e7,1.6e7,1e6), minor=True )

mpp.set_ylim( 4, [-1.5e7,.2e7] )
mpp.set_yticks( 4, [-1e7,0] )
mpp.set_yticklabels( 4, ['-10^7','0'] )
mpp.set_yticks( 4, np.arange(-1.5e7,.3e7,1e6), minor=True )

mpp.set_ylim( 5, [-6e5,6e5] )
mpp.set_yticks( 5, [-5e5,0,5e5] )
mpp.set_yticklabels( 5, ['-10^5','0','10^5'] )
mpp.set_yticks( 5, np.arange(-5e5,6e5,1e5), minor=True )
"""

elif ( plot_flag == 'poster2' ):
    ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU'
    timeshots1 = [597, 605, 613]
    sample_dict=dict(name='regular',n_reduce=2,n_min=400)
    tick_and_labels_commands="""
mpp.set_xlim([0,.3])
mpp.set_xticks([0,.1,.2])
mpp.set_xticklabels(['0','.1','.2'])
mpp.set_xticks(np.arange(0,.3,0.05), minor=True)

mpp.set_ylim(0, [-170,170])
mpp.set_yticks(0, [-100,0,100])
mpp.set_yticklabels(0, ['-100','0','100'])

mpp.set_ylim(1, [-69,69])
mpp.set_yticks(1, [-50,0,50])
mpp.set_yticks(1, np.arange(-70,70,10), minor=True)
mpp.set_yticklabels(1, ['-50','0','50'])

mpp.set_ylim( 2, [-.5,1.2] )
mpp.set_yticks( 2, [0,1] )
mpp.set_yticks( 2, np.arange(-0.5,1.6,.1), minor=True )

mpp.set_ylim( 3, [-.2e7,1.5e7] )
mpp.set_yticks( 3, [0,1e7] )
mpp.set_yticklabels( 3, ['0','10^7'] )
mpp.set_yticks( 3, np.arange(-.2e7,1.6e7,1e6), minor=True )

mpp.set_ylim( 4, [-1.5e7,.2e7] )
mpp.set_yticks( 4, [-1e7,0] )
mpp.set_yticklabels( 4, ['-10^7','0'] )
mpp.set_yticks( 4, np.arange(-1.5e7,.3e7,1e6), minor=True )

mpp.set_ylim( 5, [-6e5,6e5] )
mpp.set_yticks( 5, [-5e5,0,5e5] )
mpp.set_yticklabels( 5, ['-10^5','0','10^5'] )
mpp.set_yticks( 5, np.arange(-5e5,6e5,1e5), minor=True )
"""
    
elif ( plot_flag == 'goddard' ):
    ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU'
    timeshots1 = [589, 597, 605, 613]
    sample_dict=dict(name='regular',n_reduce=5,n_min=400)
    tick_and_labels_commands="""
mpp.set_xlim([0,.3])
mpp.set_xticks([0,.1,.2])
mpp.set_xticklabels(['0','.1','.2'])
mpp.set_xticks(np.arange(0,.3,0.05), minor=True)

mpp.set_ylim(0, [-170,170])
mpp.set_yticks(0, [-100,0,100])
mpp.set_yticks( 2, np.arange(-0.5,1.6,.1), minor=True )
mpp.set_yticklabels(0, ['-100','0','100'])

mpp.set_ylim(1, [-69,69])
mpp.set_yticks(1, [-50,0,50])
mpp.set_yticks(1, np.arange(-70,70,10), minor=True)
mpp.set_yticklabels(1, ['-50','0','50'])

mpp.set_ylim( 2, [-.5,1.2] )
mpp.set_yticks( 2, [0,1] )
mpp.set_yticks( 2, np.arange(-0.5,1.6,.1), minor=True )

mpp.set_ylim( 3, [-.2e7,1.5e7] )
mpp.set_yticks( 3, [0,1e7] )
mpp.set_yticklabels( 3, ['0','10^7'] )
mpp.set_yticks( 3, np.arange(-.2e7,1.6e7,1e6), minor=True )

mpp.set_ylim( 4, [-1.5e7,.2e7] )
mpp.set_yticks( 4, [-1e7,0] )
mpp.set_yticklabels( 4, ['-10^7','0'] )
mpp.set_yticks( 4, np.arange(-1.5e7,.3e7,1e6), minor=True )

mpp.set_ylim( 5, [-6e5,6e5] )
mpp.set_yticks( 5, [-5e5,0,5e5] )
mpp.set_yticklabels( 5, ['-10^5','0','10^5'] )
mpp.set_yticks( 5, np.arange(-5e5,6e5,1e5), minor=True )
"""
    
mpp = tdc_mpp__n_rho_e_xp(ID,timeshots1,sample_dict=sample_dict)

mpp.interactive_off()

exec tick_and_labels_commands

mpp.interactive_on()

plt.show()
