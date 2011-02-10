# for printing:
# => use png device
# => use dpi=600 --> tdc_set_hires_dpi()
#
#commands for raster graphics format 
import matplotlib as mpl
mpl.use('Agg')
from Common        import *
tdc_set_hires_dpi()
#------------------------------------

import matplotlib.pyplot as plt
import numpy             as np

from Common        import *
from Particles     import *
from ComplexPlots  import tdc_mpp__n_rho_e

import MPP


tdc_set_hardcopy_rcparams()
    
tdc_set_results_dir('../RESULTS/FreeAgent/')


fig_style=dict()

## plot_flag = 'j1_ignition'
plot_flag = 'j1_e_screening'




if ( plot_flag == 'j1_e_screening' ):
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
mpp.set_yticklabels( 2, ['0','1'] )
mpp.set_yticks( 2, np.arange(-0.2,1.2,.1), minor=True )
"""
# ------------------------------------------------------------


mpp = tdc_mpp__n_rho_e(ID,timeshots1,**fig_style)
mpp.set_window_title(ID)
mpp.interactive_off()

# xlabels
for j in range(len(timeshots1)):
    mpp.set_bottom_xlabel(j, r'$x$')

exec tick_and_labels_commands

mpp.interactive_on()

plt.show()
tdc_set_default_rcparams()

