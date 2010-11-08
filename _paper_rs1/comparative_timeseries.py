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
from ComplexPlots  import tdc_mpp__n_rho_e_xp

import MPP


tdc_set_hardcopy_rcparams()
    
tdc_set_results_dir('../RESULTS/FreeAgent/')


fig_style=dict()

plot_flag = 'j1_ignition'
## plot_flag = 'j1_e_screening'

## plot_flag = 'j0.5_e_screening'
## plot_flag = 'j1.5_e_screening'

# ------------------------------------------------------------
# j=1
# ------------------------------------------------------------

if ( plot_flag == 'j1_ignition' ):
    ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU__3d_cycle'
    timeshots1 = [10, 70, 130]
    sample_dict=dict(name='regular',n_reduce=1,n_min=400)
    fig_style=dict(aspect_ratio = 1.618*1.355)
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
mpp.set_yticklabels( 5, ['-5\cdot10^4','0','5\cdot10^4'] )
mpp.set_yticks( 5, np.arange(-5e4,6e4,1e4), minor=True )
"""
    
elif ( plot_flag == 'j1_e_screening' ):
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
mpp.set_yticklabels( 5, ['-5\cdot10^5','0','5\cdot10^5'] )
mpp.set_yticks( 5, np.arange(-5e5,6e5,1e5), minor=True )
"""
# ------------------------------------------------------------
 
# ------------------------------------------------------------
# j=0.5 
# ------------------------------------------------------------

elif ( plot_flag == 'j0.5_e_screening' ):
    ID='RS_1_R6_jp0.5_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU'
    timeshots1 = [434, 440, 446, 455]
    sample_dict=dict(name='regular',n_reduce=2,n_min=400)
    tick_and_labels_commands="""
mpp.set_xlim([0,.3])
mpp.set_xticks([0,.1,.2])
mpp.set_xticklabels(['0','.1','.2'])
mpp.set_xticks(np.arange(0,.3,0.05), minor=True)

mpp.set_ylim(0, [-38,38])
mpp.set_yticks(0, [-20,0,20])
mpp.set_yticks(0, np.arange(-40,40,5), minor=True)
mpp.set_yticklabels(0, ['-20','0','20'])

mpp.set_ylim(1, [-9,9])
mpp.set_yticks(1, [-5,0,5])
mpp.set_yticks(1, np.arange(-9,10,1), minor=True)
mpp.set_yticklabels(1, ['-5','0','5'])

mpp.set_ylim( 2, [-.2,.6] )
mpp.set_yticks( 2, [0,.5] )
mpp.set_yticklabels( 2, ['0','0.5'] )
mpp.set_yticks( 2, np.arange(-0.2,.7,.1), minor=True )

mpp.set_ylim( 3, [-.2e7,1.1e7] )
mpp.set_yticks( 3, [0,1e7] )
mpp.set_yticklabels( 3, ['0','10^7'] )
mpp.set_yticks( 3, np.arange(-.2e7,1.2e7,1e6), minor=True )

mpp.set_ylim( 4, [-1.1e7,.2e7] )
mpp.set_yticks( 4, [-1e7,0] )
mpp.set_yticklabels( 4, ['-10^7','0'] )
mpp.set_yticks( 4, np.arange(-1.1e7,.3e7,1e6), minor=True )

mpp.set_ylim( 5, [-3e5,3e5] )
mpp.set_yticks( 5, [-2e5,0,2e5] )
mpp.set_yticklabels( 5, ['-2\cdot10^5','0','2\cdot10^5'] )
mpp.set_yticks( 5, np.arange(-3e5,3e5,1e5), minor=True )
"""
# ------------------------------------------------------------

# ------------------------------------------------------------
# j=1.5 
# ------------------------------------------------------------

elif ( plot_flag == 'j1.5_e_screening' ):
    ID='RS_1_R6_jp1.5_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU'
    timeshots1 = [371, 377, 383, 392]
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
mpp.set_yticklabels( 5, ['-5\cdot10^5','0','5\cdot10^5'] )
mpp.set_yticks( 5, np.arange(-5e5,6e5,1e5), minor=True )
"""
# ------------------------------------------------------------
    
mpp = tdc_mpp__n_rho_e_xp(ID,timeshots1,sample_dict=sample_dict,**fig_style)
mpp.set_window_title(ID)
mpp.interactive_off()

# xlabels
for j in range(len(timeshots1)):
    mpp.set_bottom_xlabel(j, r'$x$')

exec tick_and_labels_commands

mpp.interactive_on()

plt.show()
tdc_set_default_rcparams()
