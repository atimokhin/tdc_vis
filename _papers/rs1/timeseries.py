import matplotlib.pyplot as plt
import numpy             as np

from ATvis.Common_Data_Plot import *

from Auxiliary        import *
from Common_Data_Plot import *

from  Fields  import tdc_Field_Data
from  Fields  import tdc_Fields_Plotter

import ATvis.MPP

AT_rcParams.set_hardcopy()

#tdc_Filenames.set_results_dir('../RESULTS/')
tdc_Filenames.set_results_dir('../RESULTS/FreeAgent/')

plot_flag = 'j1_overview'
## plot_flag = 'j1_close_view'

## plot_flag = 'j0.5_overview'
## plot_flag = 'j0.5_close_view'

## plot_flag = 'j1.5_overview'
## plot_flag = 'j1.5_close_view'


# ------------------------------------------------------------
# j=1 
# ------------------------------------------------------------

if ( plot_flag == 'j1_overview' ):
    ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU'
    select =()
    timeshots = range(363,635,12);
    shape     = (5,3)
    tick_and_labels_commands="""
mpp.set_xticks([0,.1,.2])
mpp.set_xticklabels(['0','.1','.2'])
mpp.set_xticks(np.arange(0,.3,0.05), minor=True)

mpp.set_ylim( (0,2), [-1.5,3.5] )
mpp.set_yticks((0,2),[-1,0,1,2,3])
mpp.set_yticklabels((0,2),['-1','0','1','2','3'])

mpp.set_ylim(1,[-36,36])
mpp.set_yticks(1,[-30,0,30])
mpp.set_yticks(1,np.arange(-30,40,10), minor=True)
mpp.set_yticklabels(1,['-30','0','30'])
"""
    
elif ( plot_flag == 'j1_close_view' ):
    ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU__3d_cycle'
    select =(0,2,4,6,9,12,15)
    ## timeshots = range(397,500,4);
    timeshots = range(10,525,30);
    shape = (4,4)
    tick_and_labels_commands="""
mpp.set_xticks([0,.1,.2])
mpp.set_xticklabels(['0','.1','.2'])
mpp.set_xticks(np.arange(0,.3,0.05), minor=True)

mpp.set_ylim(0,[-.4,1.9])
mpp.set_yticks( 0, [0,1])
mpp.set_yticks( 0, np.arange(0,2,.5), minor=True)
mpp.set_yticklabels( 0, ['0','1'])

mpp.set_ylim(1,[-1.5,3.5])
mpp.set_yticks( 1, [-1,0,1,2,3])
mpp.set_yticklabels( 1, ['-1','0','1','2','3'])

mpp.set_ylim( 2, [-26,26])
mpp.set_yticks( 2, [-20,0,20])
mpp.set_yticks( 2, np.arange(-25,26,5), minor=True)
mpp.set_yticklabels( 2, ['-20','0','20'])

mpp.set_ylim( 3, [-69,69])
mpp.set_yticks( 3, [-50,0,50])
mpp.set_yticks( 3, np.arange(-70,70,10), minor=True)
mpp.set_yticklabels( 3, ['-50','0','50'])
"""
# ------------------------------------------------------------
 
# ------------------------------------------------------------
# j=0.5 
# ------------------------------------------------------------
if ( plot_flag == 'j0.5_overview' ):
    ID='RS_1_R6_jp0.5_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU'
    select =()
    timeshots = range(349,635,12);
    shape     = (5,3)
    tick_and_labels_commands="""
mpp.set_xticks([0,.1,.2])
mpp.set_xticklabels(['0','.1','.2'])
mpp.set_xticks(np.arange(0,.3,0.05), minor=True)

mpp.set_ylim( 0, [-1.5,3.5] )
mpp.set_yticks(0,[-1,0,1,2,3])
mpp.set_yticklabels(0,['-1','0','1','2','3'])

mpp.set_ylim(1,[-8,8])
mpp.set_yticks(1,[-5,0,5])
mpp.set_yticks(1,np.arange(-8,9,1), minor=True)
mpp.set_yticklabels(1,['-5','0','5'])

mpp.set_ylim(2,[-11,11])
mpp.set_yticks(2,[-10,0,10])
mpp.set_yticks(2,np.arange(-11,12,1), minor=True)
mpp.set_yticklabels(2,['-10','0','10'])
"""

elif ( plot_flag == 'j0.5_close_view' ):
    ID='RS_1_R6_jp0.5_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU'
    select =(8,10,12,15)
    ## timeshots = range(410,525,4);
    timeshots = range(410,525,3);
    shape = (4,4)
    tick_and_labels_commands="""
mpp.set_xticks([0,.1,.2])
mpp.set_xticklabels(['0','.1','.2'])
mpp.set_xticks(np.arange(0,.3,0.05), minor=True)

mpp.set_ylim(0,[-.4,1.9])
mpp.set_yticks( 0, [0,1])
mpp.set_yticks( 0, np.arange(0,2,.5), minor=True)
mpp.set_yticklabels( 0, ['0','1'])

mpp.set_ylim( 1, [-6.5,6.5])
mpp.set_yticks( 1, [-5,0,5])
mpp.set_yticks( 1, np.arange(-6,7,1), minor=True)
mpp.set_yticklabels( 1, ['-5','0','5'])

mpp.set_ylim( 2, [-6.5,6.5])
mpp.set_yticks( 2, [-5,0,5])
mpp.set_yticks( 2, np.arange(-6,7,1), minor=True)
mpp.set_yticklabels( 2, ['-5','0','5'])

mpp.set_ylim( 3, [-14,14])
mpp.set_yticks( 3, [-10,0,10])
mpp.set_yticks( 3, np.arange(-15,20,5), minor=True)
mpp.set_yticklabels( 3, ['-10','0','10'])
"""
# ------------------------------------------------------------


# ------------------------------------------------------------
# j=1.5 
# ------------------------------------------------------------

if ( plot_flag == 'j1.5_overview' ):
    ID='RS_1_R6_jp1.5_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU'
    select =()
    timeshots = range(330,635,12);
    shape     = (5,3)
    tick_and_labels_commands="""
mpp.set_xticks([0,.1,.2])
mpp.set_xticklabels(['0','.1','.2'])
mpp.set_xticks(np.arange(0,.3,0.05), minor=True)

mpp.set_ylim( 0, [-15,15] )
mpp.set_yticks(0,[-10,0,10])
mpp.set_yticks(0,np.arange(-15,20,5), minor=True)
mpp.set_yticklabels(0,['-10','0','10'])

mpp.set_ylim(1,[-36,36])
mpp.set_yticks(1,[-30,0,30])
mpp.set_yticks(1,np.arange(-30,40,10), minor=True)
mpp.set_yticklabels(1,['-30','0','30'])

mpp.set_ylim( 2, [-1.5,3.5] )
mpp.set_yticks(2,[-1,0,1,2,3])
mpp.set_yticklabels(2,['-1','0','1','2','3'])
"""
    
elif ( plot_flag == 'j1.5_close_view' ):
    ID='RS_1_R6_jp1.5_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU'
    select =(7,9,11,14)
    ## timeshots = range(397,500,4);
    timeshots = range(350,525,3);
    shape = (4,4)
    tick_and_labels_commands="""
mpp.set_xticks([0,.1,.2])
mpp.set_xticklabels(['0','.1','.2'])
mpp.set_xticks(np.arange(0,.3,0.05), minor=True)

mpp.set_ylim(0,[-1.5,2.5])
mpp.set_yticks( 0, [-1,0,1,2])
mpp.set_yticks( 0, np.arange(-1.5,2,.5), minor=True)
mpp.set_yticklabels( 0, ['-1','0','1','2'])

mpp.set_ylim(1,[-1.5,3.5])
mpp.set_yticks( 1, [-1,0,1,2,3])
mpp.set_yticklabels( 1, ['-1','0','1','2','3'])

mpp.set_ylim( 1, [-6.5,6.5])
mpp.set_yticks( 1, [-5,0,5])
mpp.set_yticks( 1, np.arange(-6,7,1), minor=True)
mpp.set_yticklabels( 1, ['-5','0','5'])

mpp.set_ylim( 2, [-26,26])
mpp.set_yticks( 2, [-20,0,20])
mpp.set_yticks( 2, np.arange(-25,26,5), minor=True)
mpp.set_yticklabels( 2, ['-20','0','20'])

mpp.set_ylim( 3, [-69,69])
mpp.set_yticks( 3, [-50,0,50])
mpp.set_yticks( 3, np.arange(-70,70,10), minor=True)
mpp.set_yticklabels( 3, ['-50','0','50'])
"""
# ------------------------------------------------------------



# DATA ---------------------
# charge density
f2 = tdc_Field_Data(ID, 'Rho')
# PLOTTER -----------------
# field plotter
p2 = tdc_Fields_Plotter(f2)
# MFP instance -------------
mpp = MPP.AT_MPP_Timeseries( shape, p2, timeshots,select)
mpp.set_window_title(ID)
mpp.interactive_off()

# xlabels
for j in range(shape[0]):
    mpp.set_bottom_xlabel(j, r'$x$')

# adjust tick and labels
exec tick_and_labels_commands

mpp.interactive_on()

# show figure
plt.show()
AT_rcParams.set_default()
