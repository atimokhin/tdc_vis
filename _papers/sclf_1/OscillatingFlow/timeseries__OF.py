import matplotlib.pyplot as plt
import numpy             as np

from ATvis.Common_Data_Plot import *

from Auxiliary        import *
from Common_Data_Plot import *
from Common_Data_Plot import tdc_Data_Sequence

from Particles import tdc_XP_Data
from ATvis.MPP import AT_MPP_Timeseries

from xps_plotter__OF import XPs_Plotter__OF
# -----------------------------------


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
AT_rcParams.set_hardcopy()
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


## tdc_Filenames.set_results_dir('../RESULTS/')
## tdc_Filenames.set_results_dir('../RESULTS/FreeAgent/')
tdc_Filenames.set_results_dir('../RESULTS/__TDC_2/')


fig_param = dict( yticklabel_fontsize = 9 )



plot_flag = 'jm05'


# ------------------------------------------------------------
# j=0.5
# ------------------------------------------------------------

if ( plot_flag == 'jm05' ):
    ID=['SCLF__jm0.5_L50_X0.5_nGJ2e5_nx5e3_dt2e-3__RhoGJConst__noMC__dP5e-2_inj15_s1',
        'SCLF__jm0.5_L50_X0.5_nGJ2e5_nx5e3_dt2e-3__RhoGJConst__noMC__dP5e-2_inj15_s1__1']
    of__filename = 'OF__j05'
    select =()
    timeshots = (2,5,7,9, 10,11,12,13, 20,30,40,50, 100,350,600,850);
    shape     = (4,4)
    tick_and_labels_commands="""
mpp.set_xlim([-1,23])
mpp.set_xticks([0,10,20])
mpp.set_xticklabels(['0','10','20'])
mpp.set_xticks(np.arange(0,23,1), minor=True)

mpp.set_ylim((0,1), [-1.8,1.8])
mpp.set_yticks((0,1),[-1,0,1])
mpp.set_yticklabels((0,1),['-1','0','1'])
mpp.set_yticks((0,1),np.arange(-1.5,2,1), minor=True)

mpp.set_ylim( (2,),  [-3,3])
mpp.set_yticks((2),[-2,-1,0,1,2])
mpp.set_yticklabels((2,),['-2','','0','','2'])
mpp.set_yticks((2,),np.arange(-2.5,3,1), minor=True)

mpp.set_ylim( (3,),  [-4,4])
mpp.set_yticks((3),[-4,-3,-2,-1,0,1,2,3,4])
mpp.set_yticklabels((3,),['-4','','-2','','0','','2','','4'])
mpp.set_yticks((3,),np.arange(-3.5,4,1), minor=True)
"""
    
# ------------------------------------------------------------



# DATA ---------------------
# XP data
f2 = tdc_Data_Sequence.init_from_data( tdc_XP_Data,
                                       calc_ids=ID,
                                       particle_name='Electrons' )

#f2 = tdc_XP_Data(calc_id=ID, particle_name='Electrons')
# PLOTTER -----------------
# field plotter
p2 = XPs_Plotter__OF( (f2,), of__filename)
# MFP instance -------------
mpp = AT_MPP_Timeseries( shape, p2, timeshots,select, fig_param=fig_param)
mpp.set_window_title(ID[0])
mpp.interactive_off()

# xlabels
for j in range(shape[0]):
    mpp.set_bottom_xlabel(j, r'$x\,[\lambda_{\rm D}]$')

# adjust tick and labels
exec tick_and_labels_commands

mpp.interactive_on()

# show figure
plt.interactive(True)
plt.show()


