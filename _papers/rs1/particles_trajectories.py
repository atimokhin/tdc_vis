import matplotlib.pyplot as plt
import numpy             as np

from Auxiliary        import *
from Common_Data_Plot import *

from Particles     import *
from Plot_CMD      import *

from single_figure_style import fig_style


tdc_set_hardcopy_rcparams()

tdc_set_results_dir('../RESULTS/FreeAgent/')

plot_flag = 'j1'


# ------------------------------------------------------------
# j=1
# ------------------------------------------------------------

if ( plot_flag == 'j1' ):
    ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU__3d_cycle'
    timeshots = [280, 370, 460]
    xxs = ( [0,0.135], [0,0.18], [0,0.225] )
    tick_and_labels_commands="""
manip_tp.set_xlim([0.045,0.139])                           
manip_tp.set_xticks([.05, .1])                
manip_tp.set_xticklabels(['.05', '.1'])   
manip_tp.set_xticks(np.arange(0.05,.15,0.01), minor=True)

manip_tp.set_ylim( [-1.6e4,1.6e4] )
manip_tp.set_yticks( [-1e4,0,1e4] )
manip_tp.set_yticklabels( ['-10^4','0','10^4'] )
manip_tp.set_yticks( np.arange(-1.6e4,1.6e4,1e3), minor=True )
"""

trail_dict=dict(length     = -1,
                style      = 'bw',
                marker     = 'numbers',
                markersize = 8)

# uncomment this to get big picture
#fig_style = {}

tp = tdc_TP_Data()
tp.setup_from_file(ID,'p500_ts370_2')
tp.select(idxs=[21, 8, 14])

## tp1 = tdc_TP_Data()
## tp1.setup_from_file(ID,'p500_ts370')
## tp.add(tp1,[1,2,3,4,5,6,7,8,9])


tt=tp.time_interval

manip_tp = tdc_plot_tp(tp,370, trail_dict=trail_dict, **fig_style)
manip_tp.interactive_off()

exec tick_and_labels_commands

manip_tp.interactive_on()
plt.show()
tdc_set_default_rcparams()
