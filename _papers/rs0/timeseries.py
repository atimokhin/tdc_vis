import matplotlib.pyplot as plt
import numpy             as np

from Auxiliary        import *
from Common_Data_Plot import *

from  Fields  import tdc_Field_Data
from  Fields  import tdc_Fields_Plotter

import ATvis.MPP

#tdc_Filenames.set_results_dir('../RESULTS/')
tdc_Filenames.set_results_dir('../RESULTS/FreeAgent/')

plot_flag = 'overview_paper_1'
plot_flag = 'close_view_paper_1'

#plot_flag = 'overview'
#plot_flag = 'overview_talk'
#plot_flag = 'close_view'
#plot_flag = 'close_view_talk'


if ( plot_flag == 'overview_paper_1' ):
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
elif ( plot_flag == 'close_view_paper_1' ):
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

 
elif ( plot_flag == 'overview' ):
    ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU'
    select =()
    timeshots = range(535,735,12);
    shape     = (5,3)
    tick_and_labels_commands="""
mpp.set_xticks([0,.1,.2])
mpp.set_xticklabels(['0','.1','.2'])
mpp.set_xticks(np.arange(0,.3,0.05), minor=True)

mpp.set_ylim( (0,2), [-1.5,3.5] )

mpp.set_ylim(1,[-36,36])
mpp.set_yticks(1,[-30,0,30])
mpp.set_yticks(1,np.arange(-30,40,10), minor=True)
mpp.set_yticklabels(1,['-30','0','30'])
"""
    
elif ( plot_flag == 'overview_talk' ):
    ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU'
    select =()
    timeshots = range(535,735,12);
    shape     = (5,3)
    tick_and_labels_commands="""
mpp.set_xticks([0,.1,.2])
mpp.set_xticklabels(['0','.1','.2'])
mpp.set_xticks(np.arange(0,.3,0.05), minor=True)

mpp.set_ylim( (0,2), [-1.5,3.5] )

mpp.set_ylim(1,[-36,36])
mpp.set_yticks(1,[-30,0,30])
mpp.set_yticks(1,np.arange(-30,40,10), minor=True)
mpp.set_yticklabels(1,['-30','0','30'])
"""
    
elif ( plot_flag == 'close_view' ):
    ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU'
    ## timeshots = range(570,650,5)
    select =(2,3,4,6,8,10)
    timeshots = range(573,650,4)
    shape = (4,4)
    tick_and_labels_commands="""
mpp.set_xticks([0,.1,.2])
mpp.set_xticklabels(['0','.1','.2'])
mpp.set_xticks(np.arange(0,.3,0.05), minor=True)

mpp.set_ylim(0,[-1.5,3.5])

mpp.set_ylim(1,[-28,28])
mpp.set_yticks(1,[-20,0,20])
mpp.set_yticklabels(1,['-20','0','20'])
mpp.set_yticks(1,np.arange(-30,30,10), minor=True)

mpp.set_ylim( (2,3), [-69,69])
mpp.set_yticks( (2,3), [-50,0,50])
mpp.set_yticks( (2,3), np.arange(-70,70,10), minor=True)
mpp.set_yticklabels( (2,3), ['-50','0','50'])
"""
elif ( plot_flag == 'close_view_talk' ):
    ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU'
    ## timeshots = range(570,650,5)
    select =()
    timeshots = range(573,650,4)
    shape = (4,3)
    tick_and_labels_commands="""
mpp.set_xticks([0,.1,.2])
mpp.set_xticklabels(['0','.1','.2'])
mpp.set_xticks(np.arange(0,.3,0.05), minor=True)

mpp.set_ylim(0,[-1.5,3.5])

mpp.set_ylim(1,[-28,28])
mpp.set_yticks(1,[-20,0,20])
mpp.set_yticklabels(1,['-20','0','20'])
mpp.set_yticks(1,np.arange(-30,30,10), minor=True)

mpp.set_ylim( (2,), [-69,69])
mpp.set_yticks( (2,), [-50,0,50])
mpp.set_yticks( (2,), np.arange(-70,70,10), minor=True)
mpp.set_yticklabels( (2,), ['-50','0','50'])
"""



# DATA ---------------------
# charge density
f2 = tdc_Field_Data(ID, 'Rho')
# PLOTTER -----------------
# field plotter
p2 = tdc_Fields_Plotter(f2)
# MFP instance -------------
mpp = MPP.AT_MPP_Timeseries( shape, p2, timeshots,select)
mpp.interactive_off()

# adjust tick and labels
exec tick_and_labels_commands

mpp.interactive_on()

# show figure
plt.show()
