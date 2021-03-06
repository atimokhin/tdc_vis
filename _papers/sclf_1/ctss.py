# for printing:
# => use png device
# => use dpi=600 --> tdc_set_hires_dpi()
#
if __name__ == '__main__':
    import tdc_vis

import numpy             as np
import matplotlib.pyplot as plt
from   matplotlib.cbook  import flatten

from ATvis.Common_Data_Plot import *

from Auxiliary        import *
from Common_Data_Plot import *
from x_PlottingFunctions.MPP      import tdc_mpp__n_rho_j_e_xp

#------------------------------------


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
AT_rcParams.set_hardcopy()
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    
tdc_Filenames.set_results_dir('../RESULTS/WD/_paper_TDC2')


fig_param=dict()

#------------------------------------
# PLot Flags
#------------------------------------

plot_flag = 'jm1.5__1'
# plot_flag = 'jm1.5__2'
# plot_flag = 'jm1.5__3'

# plot_flag = 'jp0.5__1'
# plot_flag = 'jp0.5__2'
# plot_flag = 'jp0.5__3'

# plot_flag = 'RhoGJ_lin2__jm2.0__1'
# plot_flag = 'RhoGJ_lin2__jm2.0__2'

# plot_flag = 'RhoGJ_lin2__jm1.059'
#------------------------------------



# ------------------------------------------------------------
# j=m1.5
# ------------------------------------------------------------

if ( plot_flag == 'jm1.5__1' ):
    ID='SCLF__jm1.5_Pcf1e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJConst__R6C_Xb0.7__dP5e-2_inj8_s1'
    timeshots1 = [470, 472, 474, 476]
    sample_dict=dict(name='regular',n_reduce=1,n_min=400)
    fig_param=dict(aspect_ratio = 1.618*1.355)
    tick_and_labels_commands="""
mpp.set_xlim([-0.02,1.02])
mpp.set_xticks(np.arange(0,1.2,.2))
mpp.set_xticklabels(['0','.2','.4','.6','.8','1'])
mpp.set_xticks(np.arange(.1,1,.2), minor=True)

mpp.set_ylim( 0, [-4.9,3] )
mpp.set_yticks( 0, [-4,-2,0,2] )
mpp.set_yticklabels( 0, ['$-4$','$-2$','$0$','$2$'] )
mpp.set_yticks( 0, np.arange(-3,3,2), minor=True )

mpp.set_ylim( 1, [-3.9,1.3] )
mpp.set_yticks(1,[-2,0])
mpp.set_yticklabels( 1, ['$-2$','$0$'] )
mpp.set_yticks(1,np.arange(-3,2,2), minor=True)

mpp.set_ylim( 2, [-4,0.5] )
mpp.set_yticks( 2, [-3,-2,-1,0] )
mpp.set_yticklabels( 2, ['$-3$','$-2$','$-1$','$0$'] )
mpp.set_yticks( 2, np.arange(-2.5,0,0.5), minor=True )

mpp.set_ylim( 3, [-1.1,0.2] )
mpp.set_yticks( 3, [-1,0] )
mpp.set_yticklabels( 3, ['$-1$','$0$'] )
mpp.set_yticks( 3, np.arange(-0.9,0.1,0.2), minor=True )

mpp.set_yscale([4,5,6],'symlog',linthreshy=3)
mpp.set_ylim([4,5,6],[-7e8,7e8])
mpp.set_yticks([4,5,6], [-1e8, -1e4, 0, 1e4, 1e8] )
mpp.set_yticklabels( [4,5,6], ['$-10^8$', '$-10^4$', '$0$', '$10^4$', '$10^8$'] )
mpp.set_yticks([4,5,6], np.sort([i for i in flatten([[ (-10**i,10**i) for i in range(8)] ,0])]),minor=True )

mpp._delete_ylabels_for_middle_plots()
"""
    
elif ( plot_flag == 'jm1.5__2' ):
    ID='SCLF__jm1.5_Pcf1e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJConst__R6C_Xb0.7__dP5e-2_inj8_s1'
    timeshots1 = [477, 483, 489, 495]
    sample_dict=dict(name='regular',n_reduce=1,n_min=400)
    fig_param=dict(aspect_ratio = 1.618*1.355)
    tick_and_labels_commands="""
mpp.set_xlim([-0.02,1.02])
mpp.set_xticks(np.arange(0,1.2,.2))
mpp.set_xticklabels(['0','.2','.4','.6','.8','1'])
mpp.set_xticks(np.arange(.1,1,.2), minor=True)

mpp.set_ylim( 0, [-80,80] )
mpp.set_yticks( 0, [-50,0,50] )
mpp.set_yticklabels( 0, ['$-50$','$0$','$50$'] )
mpp.set_yticks( 0, np.arange(-80,90,10), minor=True )

mpp.set_ylim( 1, [-19,19] )
mpp.set_yticks( 1, [-10,0,10])
mpp.set_yticklabels( 1, ['$-10$','$0$','$10$'] )
mpp.set_yticks( 1, np.arange(-15,19,5), minor=True)

mpp.set_ylim( 2, [-19,19] )
mpp.set_yticks( 2, [-10,0,10])
mpp.set_yticklabels( 2, ['$-10$','$0$','$10$'] )
mpp.set_yticks( 2, np.arange(-15,19,5), minor=True)

mpp.set_ylim( 3, [-1.1,0.2] )
mpp.set_yticks( 3, [-1,0] )
mpp.set_yticklabels( 3, ['$-1$','$0$'] )
mpp.set_yticks( 3, np.arange(-0.9,0.1,0.2), minor=True )

mpp.set_yscale([4,5,6],'symlog',linthreshy=3)
mpp.set_ylim([4,5,6],[-7e8,7e8])
mpp.set_yticks([4,5,6], [-1e8, -1e4, 0, 1e4, 1e8] )
mpp.set_yticklabels( [4,5,6], ['$-10^8$', '$-10^4$', '$0$', '$10^4$', '$10^8$'] )
mpp.set_yticks([4,5,6], np.sort([i for i in flatten([[ (-10**i,10**i) for i in range(8)] ,0])]),minor=True )

mpp._delete_ylabels_for_middle_plots()
"""

elif ( plot_flag == 'jm1.5__3' ):
    ID='SCLF__jm1.5_Pcf1e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJConst__R6C_Xb0.7__dP5e-2_inj8_s1'
    timeshots1 = [496, 506, 516, 526]
    sample_dict=dict(name='regular',n_reduce=1,n_min=400)
    fig_param=dict(aspect_ratio = 1.618*1.355)
    tick_and_labels_commands="""
mpp.set_xlim([-0.02,1.02])
mpp.set_xticks(np.arange(0,1.2,.2))
mpp.set_xticklabels(['0','.2','.4','.6','.8','1'])
mpp.set_xticks(np.arange(.1,1,.2), minor=True)

mpp.set_ylim( 0, [-190,190] )
mpp.set_yticks( 0, [-100,0,100] )
mpp.set_yticklabels( 0, ['$-100$','$0$','$100$'] )
mpp.set_yticks( 0, np.arange(-150,190,50), minor=True )

mpp.set_ylim( 1, [-19,19] )
mpp.set_yticks( 1, [-10,0,10])
mpp.set_yticklabels( 1, ['$-10$','$0$','$10$'] )
mpp.set_yticks( 1, np.arange(-15,19,5), minor=True)

mpp.set_ylim( 2, [-19,19] )
mpp.set_yticks( 2, [-10,0,10])
mpp.set_yticklabels( 2, ['$-10$','$0$','$10$'] )
mpp.set_yticks( 2, np.arange(-15,19,5), minor=True)

mpp.set_ylim( 3, [-1.1,0.2] )
mpp.set_yticks( 3, [-1,0] )
mpp.set_yticklabels( 3, ['$-1$','$0$'] )
mpp.set_yticks( 3, np.arange(-0.9,0.1,0.2), minor=True )

mpp.set_yscale([4,5,6],'symlog',linthreshy=3)
mpp.set_ylim([4,5,6],[-7e8,7e8])
mpp.set_yticks([4,5,6], [-1e8, -1e4, 0, 1e4, 1e8] )
mpp.set_yticklabels( [4,5,6], ['$-10^8$', '$-10^4$', '$0$', '$10^4$', '$10^8$'] )
mpp.set_yticks([4,5,6], np.sort([i for i in flatten([[ (-10**i,10**i) for i in range(8)] ,0])]),minor=True )

mpp._delete_ylabels_for_middle_plots()
"""
# ------------------------------------------------------------
 
# ------------------------------------------------------------
# j=p0.5 
# ------------------------------------------------------------

elif ( plot_flag == 'jp0.5__1' ):
    ID='SCLF__jp0.5_Pcf1e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJConst__R6C_Xb0.7__dP5e-2_inj5_sU_P'
    timeshots1 = [803, 811, 819, 827]
    sample_dict=dict(name='regular',n_reduce=1,n_min=400)
    fig_param=dict(aspect_ratio = 1.618*1.355)
    tick_and_labels_commands="""
mpp.set_xlim([-0.02,1.02])
mpp.set_xticks(np.arange(0,1.2,.2))
mpp.set_xticklabels(['0','.2','.4','.6','.8','1'])
mpp.set_xticks(np.arange(.1,1,.2), minor=True)

mpp.set_ylim( 0, [-4.6,3] )
mpp.set_yticks( 0, [-4,-2,0,2] )
mpp.set_yticklabels( 0, ['$-4$','$-2$','$0$','$2$'] )
mpp.set_yticks( 0, np.arange(-3,3,2), minor=True )

mpp.set_ylim( 1, [-3,2.4] )
mpp.set_yticks(1,[-2,0,2])
mpp.set_yticklabels( 1, ['$-2$','$0$','$2$'] )
mpp.set_yticks(1,np.arange(-1,3,2), minor=True)

mpp.set_ylim( 2, [-0.3,3.9] )
mpp.set_yticks( 2, [0,1,2,3] )
mpp.set_yticklabels( 2, ['$0$','$1$','$2$','$3$'] )
mpp.set_yticks( 2, np.arange(0.5,4,0.5), minor=True )

mpp.set_ylim( 3, [-0.3,3.1] )
mpp.set_yticks( 3, [0,1,2,3] )
mpp.set_yticklabels( 3, ['$0$','$1$','$2$','$3$'] )
mpp.set_yticks( 3, np.arange(-0.2,3,0.2), minor=True )

mpp.set_yscale([4,5,6],'symlog',linthreshy=3)
mpp.set_ylim([4,5,6],[-7e8,7e8])
mpp.set_yticks([4,5,6], [-1e8, -1e4, 0, 1e4, 1e8] )
mpp.set_yticklabels( [4,5,6], ['$-10^8$', '$-10^4$', '$0$', '$10^4$', '$10^8$'] )
mpp.set_yticks([4,5,6], np.sort([i for i in flatten([[ (-10**i,10**i) for i in range(8)] ,0])]),minor=True )

mpp._delete_ylabels_for_middle_plots()
"""
    
elif ( plot_flag == 'jp0.5__2' ):
    ID='SCLF__jp0.5_Pcf1e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJConst__R6C_Xb0.7__dP5e-2_inj5_sU_P'
    timeshots1 = [828, 836, 844, 852]
    sample_dict=dict(name='regular',n_reduce=1,n_min=400)
    fig_param=dict(aspect_ratio = 1.618*1.355)
    tick_and_labels_commands="""
mpp.set_xlim([-0.02,1.02])
mpp.set_xticks(np.arange(0,1.2,.2))
mpp.set_xticklabels(['0','.2','.4','.6','.8','1'])
mpp.set_xticks(np.arange(.1,1,.2), minor=True)

mpp.set_ylim( 0, [-48,48] )
mpp.set_yticks( 0, [-40,-20,0,20,40] )
mpp.set_yticklabels( 0, ['$-40$','$-20$','$0$','$20$','$40$'] )
mpp.set_yticks( 0, np.arange(-30,40,10), minor=True )

mpp.set_ylim( 1, [-9,9] )
mpp.set_yticks( 1, [-5,0,5] )
mpp.set_yticklabels( 1, ['$-5$','$0$','$5$'] )
mpp.set_yticks( 1, np.arange(-8,9,1), minor=True )

mpp.set_ylim( 2, [-9,9] )
mpp.set_yticks( 2, [-5,0,5] )
mpp.set_yticklabels( 2, ['$-5$','$0$','$5$'] )
mpp.set_yticks( 2, np.arange(-8,9,1), minor=True )

mpp.set_ylim( 3, [-0.3,3.1] )
mpp.set_yticks( 3, [0,1,2,3] )
mpp.set_yticklabels( 3, ['$0$','$1$','$2$','$3$'] )
mpp.set_yticks( 3, np.arange(-0.2,3,0.2), minor=True )

mpp.set_yscale([4,5,6],'symlog',linthreshy=3)
mpp.set_ylim([4,5,6],[-7e8,7e8])
mpp.set_yticks([4,5,6], [-1e8, -1e4, 0, 1e4, 1e8] )
mpp.set_yticklabels( [4,5,6], ['$-10^8$', '$-10^4$', '$0$', '$10^4$', '$10^8$'] )
mpp.set_yticks([4,5,6], np.sort([i for i in flatten([[ (-10**i,10**i) for i in range(8)] ,0])]),minor=True )

mpp._delete_ylabels_for_middle_plots()
"""
    
elif ( plot_flag == 'jp0.5__3' ):
    ID='SCLF__jp0.5_Pcf1e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJConst__R6C_Xb0.7__dP5e-2_inj5_sU_P'
    timeshots1 = [858, 872, 886, 900]
    sample_dict=dict(name='regular',n_reduce=1,n_min=400)
    fig_param=dict(aspect_ratio = 1.618*1.355)
    tick_and_labels_commands="""
mpp.set_xlim([-0.02,1.02])
mpp.set_xticks(np.arange(0,1.2,.2))
mpp.set_xticklabels(['0','.2','.4','.6','.8','1'])
mpp.set_xticks(np.arange(.1,1,.2), minor=True)

mpp.set_ylim( 0, [-140,140] )
mpp.set_yticks( 0, [-100,0,100] )
mpp.set_yticklabels( 0, ['$-100$','$0$','$100$'] )
mpp.set_yticks( 0, np.arange(-120,140,20), minor=True )

mpp.set_ylim( 1, [-9,9] )
mpp.set_yticks( 1, [-5,0,5] )
mpp.set_yticklabels( 1, ['$-5$','$0$','$5$'] )
mpp.set_yticks( 1, np.arange(-8,9,1), minor=True )

mpp.set_ylim( 2, [-9,9] )
mpp.set_yticks( 2, [-5,0,5] )
mpp.set_yticklabels( 2, ['$-5$','$0$','$5$'] )
mpp.set_yticks( 2, np.arange(-8,9,1), minor=True )

mpp.set_ylim( 3, [-0.3,3.1] )
mpp.set_yticks( 3, [0,1,2,3] )
mpp.set_yticklabels( 3, ['$0$','$1$','$2$','$3$'] )
mpp.set_yticks( 3, np.arange(-0.2,3,0.2), minor=True )

mpp.set_yscale([4,5,6],'symlog',linthreshy=3)
mpp.set_ylim([4,5,6],[-7e8,7e8])
mpp.set_yticks([4,5,6], [-1e8, -1e4, 0, 1e4, 1e8] )
mpp.set_yticklabels( [4,5,6], ['$-10^8$', '$-10^4$', '$0$', '$10^4$', '$10^8$'] )
mpp.set_yticks([4,5,6], np.sort([i for i in flatten([[ (-10**i,10**i) for i in range(8)] ,0])]),minor=True )

mpp._delete_ylabels_for_middle_plots()
"""
# ------------------------------------------------------------

# ------------------------------------------------------------
# j=m2.0 RhoGH lin2 
# ------------------------------------------------------------

elif ( plot_flag == 'RhoGJ_lin2__jm2.0__1' ):
    ID='Arons__j2.000_Pcf9e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJlin2_A1_AAm0.7_X1__R6C__dP5e-2_inj12_sU'
    timeshots1 = [786, 795, 804, 813]
    sample_dict=dict(name='regular',n_reduce=1,n_min=400)
    fig_param=dict(aspect_ratio = 1.618*1.355)
    tick_and_labels_commands="""
mpp.set_xlim([-0.02,1.02])
mpp.set_xticks(np.arange(0,1.2,.2))
mpp.set_xticklabels(['0','.2','.4','.6','.8','1'])
mpp.set_xticks(np.arange(.1,1,.2), minor=True)

mpp.set_ylim( 0, [-6,6] )
mpp.set_yticks( 0, [-5,0,5] )
mpp.set_yticklabels( 0, ['$-5$','$0$','$5$'] )
mpp.set_yticks( 0, np.arange(-4,5,1), minor=True )

mpp.set_ylim( 1, [-3,0.5] )
mpp.set_yticks(1,[-2,0])
mpp.set_yticklabels( 1, ['$-2$','$0$'] )
mpp.set_yticks(1,np.arange(-3,0.5,1), minor=True)

mpp.set_ylim( 2,[-3.2,0.5] )
mpp.set_yticks( 2, [-2,0] )
mpp.set_yticklabels( 2, ['$-2$','$0$'] )
mpp.set_yticks( 2, np.arange(-3,0.1,1), minor=True )

mpp.set_ylim( 3,[-0.08,0.08] )
mpp.set_yticks( 3, [-0.05, 0, 0.05] )
mpp.set_yticklabels( 3, ['$-0.05$','$0$','$0.05$'] )
mpp.set_yticks( 3, np.arange(-0.07,0.08,0.01), minor=True )

mpp.set_yscale([4,5,6],'symlog',linthreshy=3)
mpp.set_ylim([4,5,6],[-7e8,7e8])
mpp.set_yticks([4,5,6], [-1e8, -1e4, 0, 1e4, 1e8] )
mpp.set_yticklabels( [4,5,6], ['$-10^8$', '$-10^4$', '$0$', '$10^4$', '$10^8$'] )
mpp.set_yticks([4,5,6], np.sort([i for i in flatten([[ (-10**i,10**i) for i in range(8)] ,0])]),minor=True )

mpp._delete_ylabels_for_middle_plots()
"""
    
elif ( plot_flag == 'RhoGJ_lin2__jm2.0__2' ):
    ID='Arons__j2.000_Pcf9e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJlin2_A1_AAm0.7_X1__R6C__dP5e-2_inj12_sU'
    timeshots1 = [816, 819, 839, 859]
    sample_dict=dict(name='regular',n_reduce=1,n_min=400)
    fig_param=dict(aspect_ratio = 1.618*1.355)
    tick_and_labels_commands="""
mpp.set_xlim([-0.02,1.02])
mpp.set_xticks(np.arange(0,1.2,.2))
mpp.set_xticklabels(['0','.2','.4','.6','.8','1'])
mpp.set_xticks(np.arange(.1,1,.2), minor=True)

mpp.set_ylim( 0, [-280,280] )
mpp.set_yticks( 0, [-200,0,200] )
mpp.set_yticklabels( 0, ['$-200$','$0$','$200$'] )
mpp.set_yticks( 0, np.arange(-250,280,50), minor=True )

mpp.set_ylim( 1, [-9,9] )
mpp.set_yticks( 1, [-5,0,5] )
mpp.set_yticklabels( 1, ['$-5$','$0$','$5$'] )
mpp.set_yticks( 1, np.arange(-8,9,1), minor=True )

mpp.set_ylim( 2, [-9,9] )
mpp.set_yticks( 2, [-5,0,5] )
mpp.set_yticklabels( 2, ['$-5$','$0$','$5$'] )
mpp.set_yticks( 2, np.arange(-8,9,1), minor=True )

mpp.set_ylim( 3,[-0.08,0.08] )
mpp.set_yticks( 3, [-0.05, 0, 0.05] )
mpp.set_yticklabels( 3, ['$-0.05$','$0$','$0.05$'] )
mpp.set_yticks( 3, np.arange(-0.07,0.08,0.01), minor=True )

mpp.set_yscale([4,5,6],'symlog',linthreshy=3)
mpp.set_ylim([4,5,6],[-7e8,7e8])
mpp.set_yticks([4,5,6], [-1e8, -1e4, 0, 1e4, 1e8] )
mpp.set_yticklabels( [4,5,6], ['$-10^8$', '$-10^4$', '$0$', '$10^4$', '$10^8$'] )
mpp.set_yticks([4,5,6], np.sort([i for i in flatten([[ (-10**i,10**i) for i in range(8)] ,0])]),minor=True )

mpp._delete_ylabels_for_middle_plots()
"""
# ------------------------------------------------------------

# ------------------------------------------------------------
# j=m1.059 RhoGH lin2 
# ------------------------------------------------------------
elif ( plot_flag == 'RhoGJ_lin2__jm1.059' ):
    ID='Arons__j1.059_Pcf9e8_L1_nGJ1e5_nx5e3_dt4e-5__RhoGJlin2_A1_AAm0.7_X1__R6C__dP5e-2_inj12_sU'
    timeshots1 = [441, 521, 581, 681]
    sample_dict=dict(name='regular',n_reduce=1,n_min=400)
    fig_param=dict(aspect_ratio = 1.618*1.355)
    tick_and_labels_commands="""
mpp.set_xlim([-0.02,1.02])
mpp.set_xticks(np.arange(0,1.2,.2))
mpp.set_xticklabels(['0','.2','.4','.6','.8','1'])
mpp.set_xticks(np.arange(.1,1,.2), minor=True)

mpp.set_ylim(0,[-2.5,0.5])
mpp.set_yticks( 0, [-2,-1,0] )
mpp.set_yticklabels( 0, ['$-2$','$-1$','$0$'] )
mpp.set_yticks( 0, np.arange(-1.5,0,.5), minor=True )

mpp.set_ylim(1,[-2.2,0.2])
mpp.set_yticks( 1, [-2,-1,0] )
mpp.set_yticklabels( 1, ['$-2$','$-1$','$0$'] )
mpp.set_yticks( 1, np.arange(-1.5,0,.5), minor=True )

mpp.set_ylim(1,[-2.2,0.2])
mpp.set_yticks( 2, [-2,-1,0] )
mpp.set_yticklabels( 2, ['$-2$','$-1$','$0$'] )
mpp.set_yticks( 2, np.arange(-1.5,0,.5), minor=True )

mpp.set_ylim(3,[-0.013,0.013])
mpp.set_yticks( 3, [-0.01, 0, 0.01] )
mpp.set_yticklabels( 3, ['$-0.01$','$0$','$0.01$'] )
mpp.set_yticks( 3, np.arange(-0.005,0.01,0.005), minor=True )

mpp.set_yscale([4,5,6],'symlog',linthreshy=3)
mpp.set_ylim([4,5,6],[-7e8,7e8])
mpp.set_yticks([4,5,6], [-1e8, -1e4, 0, 1e4, 1e8] )
mpp.set_yticklabels( [4,5,6], ['$-10^8$', '$-10^4$', '$0$', '$10^4$', '$10^8$'] )
mpp.set_yticks([4,5,6], np.sort([i for i in flatten([[ (-10**i,10**i) for i in range(8)] ,0])]),minor=True )

mpp._delete_ylabels_for_middle_plots()
"""
    
# ------------------------------------------------------------


# ============================================================
# Actual Plotting Commands
# ============================================================
    
mpp = tdc_mpp__n_rho_j_e_xp( ID,
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
