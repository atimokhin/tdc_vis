# for printing:
# => use png device
# => use dpi=600 --> tdc_set_hires_dpi()
#
#commands for raster graphics format 
import matplotlib as mpl
## mpl.use('Agg')

from Auxiliary        import *
from Common_Data_Plot import *

#------------------------------------

#------------------------------------
import matplotlib.pyplot as plt
from   matplotlib.cbook  import flatten

import numpy             as np

from Particles  import *
from Plots_MPP  import tdc_mpp__n_rho_j_e_xp_epgp

import MPP
#------------------------------------


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
tdc_set_hardcopy_rcparams()
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    
tdc_set_results_dir('../RESULTS/WD/')


fig_param=dict()

#------------------------------------
# PLot Flags
#------------------------------------


plot_flag = 'jp1.5__1'
plot_flag = 'jp1.5__2'
plot_flag = 'jp1.5__3'

#------------------------------------



# ------------------------------------------------------------
# j=1.5 
# ------------------------------------------------------------

if ( plot_flag == 'jp1.5__1' ):
    ID='SCLF__jp1.5_Pcf1e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJConst__R6C_Xb0.7__dP5e-2_inj7_sU'
    timeshots1 = [632, 636, 640, 644]
    sample_dict=dict(name='regular',n_reduce=1,n_min=400)
    fig_param=dict(aspect_ratio = 1.618*1.355)
    tick_and_labels_commands="""
mpp.set_xlim([-0.02,1.02])
mpp.set_xticks(np.arange(0,1.2,.2))
mpp.set_xticklabels(['0','.2','.4','.6','.8','1'])
mpp.set_xticks(np.arange(.1,1,.2), minor=True)

mpp.set_ylim( 0, [-4.6,4.6] )
mpp.set_yticks( 0, [-4,-2,0,2,4] )
mpp.set_yticklabels( 0, ['$-4$','$-2$','$0$','$2$','$4$'] )
mpp.set_yticks( 0, np.arange(-3,4,2), minor=True )

mpp.set_ylim( 1, [-3.7,3.7] )
mpp.set_yticks(1,[-2,0,2])
mpp.set_yticklabels( 1, ['$-2$','$0$','$2$'] )
mpp.set_yticks(1,np.arange(-3,4,2), minor=True)

mpp.set_ylim( 2, [-0.3,4.6] )
mpp.set_yticks( 2, [0,1,2,3,4] )
mpp.set_yticklabels( 2, ['$0$','$1$','$2$','$3$','$4$'] )
mpp.set_yticks( 2, np.arange(0.5,5,0.5), minor=True )

mpp.set_ylim( 3, [-0.3,3.1] )
mpp.set_yticks( 3, [0,1,2,3] )
mpp.set_yticklabels( 3, ['$0$','$1$','$2$','$3$'] )
mpp.set_yticks( 3, np.arange(-0.2,3,0.2), minor=True )

mpp.set_yscale([4,5,6,7],'symlog',linthreshy=3)
mpp.set_ylim([4,5,6,7],[-7e8,7e8])
mpp.set_yticks([4,5,6,7], [-1e8, -1e4, 0, 1e4, 1e8] )
mpp.set_yticklabels( [4,5,6], ['$-10^8$', '$-10^4$', '$0$', '$10^4$', '$10^8$'] )
mpp.set_yticks([4,5,6,7], np.sort([i for i in flatten([[ (-10**i,10**i) for i in range(8)] ,0])]),minor=True )

mpp._delete_ylabels_for_middle_plots()
"""

elif ( plot_flag == 'jp1.5__2' ):
    ID='SCLF__jp1.5_Pcf1e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJConst__R6C_Xb0.7__dP5e-2_inj7_sU'
    timeshots1 = [645, 651, 657, 663]
    sample_dict=dict(name='regular',n_reduce=1,n_min=400)
    fig_param=dict(aspect_ratio = 1.618*1.355)
    tick_and_labels_commands="""
mpp.set_xlim([-0.02,1.02])
mpp.set_xticks(np.arange(0,1.2,.2))
mpp.set_xticklabels(['0','.2','.4','.6','.8','1'])
mpp.set_xticks(np.arange(.1,1,.2), minor=True)

mpp.set_ylim( 0, [-128,128] )
mpp.set_yticks( 0, [-100,0,100] )
mpp.set_yticklabels( 0, ['$-100$','$0$','$100$'] )
mpp.set_yticks( 0, np.arange(-120,140,20), minor=True )

mpp.set_ylim( 1, [-38,38] )
mpp.set_yticks( 1,[-20,0,20])
mpp.set_yticklabels( 1, ['$-20$','$0$','$20$'] )
mpp.set_yticks(1,np.arange(-30,40,10), minor=True)

mpp.set_ylim( 2, [-38,38] )
mpp.set_yticks( 2,[-20,0,20])
mpp.set_yticklabels( 2, ['$-20$','$0$','$20$'] )
mpp.set_yticks( 2, np.arange(-30,40,10), minor=True)

mpp.set_ylim( 3, [-0.3,3.1] )
mpp.set_yticks( 3, [0,1,2,3] )
mpp.set_yticklabels( 3, ['$0$','$1$','$2$','$3$'] )
mpp.set_yticks( 3, np.arange(-0.2,3,0.2), minor=True )

mpp.set_yscale([4,5,6,7],'symlog',linthreshy=3)
mpp.set_ylim([4,5,6,7],[-7e8,7e8])
mpp.set_yticks([4,5,6,7], [-1e8, -1e4, 0, 1e4, 1e8] )
mpp.set_yticklabels( [4,5,6], ['$-10^8$', '$-10^4$', '$0$', '$10^4$', '$10^8$'] )
mpp.set_yticks([4,5,6,7], np.sort([i for i in flatten([[ (-10**i,10**i) for i in range(8)] ,0])]),minor=True )

mpp._delete_ylabels_for_middle_plots()
"""

elif ( plot_flag == 'jp1.5__3' ):
    ID='SCLF__jp1.5_Pcf1e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJConst__R6C_Xb0.7__dP5e-2_inj7_sU'
    timeshots1 = [664, 674, 684, 694]
    sample_dict=dict(name='regular',n_reduce=1,n_min=400)
    fig_param=dict(aspect_ratio = 1.618*1.355)
    tick_and_labels_commands="""
mpp.set_xlim([-0.02,1.02])
mpp.set_xticks(np.arange(0,1.2,.2))
mpp.set_xticklabels(['0','.2','.4','.6','.8','1'])
mpp.set_xticks(np.arange(.1,1,.2), minor=True)

mpp.set_ylim( 0, [-1100,1100] )
mpp.set_yticks( 0, [-1e3,0,1e3] )
mpp.set_yticklabels( 0, ['$-10^3$','$0$','$10^3$'] )
mpp.set_yticks( 0, np.arange(-900,1000,100), minor=True )

mpp.set_ylim( 1, [-38,38] )
mpp.set_yticks( 1,[-20,0,20])
mpp.set_yticklabels( 1, ['$-20$','$0$','$20$'] )
mpp.set_yticks(1,np.arange(-30,40,10), minor=True)

mpp.set_ylim( 2, [-38,38] )
mpp.set_yticks( 2,[-20,0,20])
mpp.set_yticklabels( 2, ['$-20$','$0$','$20$'] )
mpp.set_yticks( 2, np.arange(-30,40,10), minor=True)

mpp.set_ylim( 3, [-0.3,3.1] )
mpp.set_yticks( 3, [0,1,2,3] )
mpp.set_yticklabels( 3, ['$0$','$1$','$2$','$3$'] )
mpp.set_yticks( 3, np.arange(-0.2,3,0.2), minor=True )

mpp.set_yscale([4,5,6,7],'symlog',linthreshy=3)
mpp.set_ylim([4,5,6,7],[-7e8,7e8])
mpp.set_yticks([4,5,6,7], [-1e8, -1e4, 0, 1e4, 1e8] )
mpp.set_yticklabels( [4,5,6], ['$-10^8$', '$-10^4$', '$0$', '$10^4$', '$10^8$'] )
mpp.set_yticks([4,5,6,7], np.sort([i for i in flatten([[ (-10**i,10**i) for i in range(8)] ,0])]),minor=True )

mpp._delete_ylabels_for_middle_plots()
"""
# ------------------------------------------------------------


# ============================================================
# Actual Plotting Commands
# ============================================================
    
mpp = tdc_mpp__n_rho_j_e_xp_epgp(ID,
                                 timeshots1,
                                 sample_dict=sample_dict,
                                 fig_param=fig_param)
mpp.set_window_title(ID)
mpp.interactive_off()

# xlabels
for j in range(len(timeshots1)):
    mpp.set_bottom_xlabel(j, r'$x$')

exec tick_and_labels_commands

mpp.interactive_on()

plt.show()
# ============================================================
