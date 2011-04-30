#
# insert ylabel later in inkscape !
#

import matplotlib.pyplot as plt
from   matplotlib.cbook  import flatten
import numpy             as np

from Common    import *
from Particles import *

from MPP import tdc_MPP

import pickle


#tdc_set_results_dir('../RESULTS/FreeAgent/')


tick_and_labels_commands="""
mpp.set_xlim([0.085,80])
mpp.set_xticks([0.1,1,10])
mpp.set_xticklabels(['0.1','1','10'])

mpp.set_ylim( (0,1), [3e-4,30])
mpp.set_yticks( (0,1), [1e-3, 1e-2, 0.1, 1, 10] )
mpp.set_yticklabels( (0,1),['10^{-3}','10^{-2}','0.1','1','10'] )

mpp._delete_xlabels_for_middle_plots()
mpp._delete_ylabels_for_middle_plots()
"""

j_label_coord={'x' : 0.12, 'y' : 6}
j_label_fontsize = 9
    
    ## fig_width_abs = 7;
    ## dx_pad_abs = 0.1
    ## dy_pad_abs = 0.1
    ## left_margin_abs   = 0.45
    ## right_margin_abs  = 0.05
    ## top_margin_abs    = 0.2
    ## bottom_margin_abs = 0.25
    ## f_ylabel_left   = 0.2
    ## f_ylabel_right  = 0.3333
    ## f_xlabel_bottom = 0.3333
    ## f_xlabel_top    = 0.25
    ## aspect_ratio = 1.618

fig_style = dict( dx_pad_abs         = 0.28,
                  dy_pad_abs         = 0.25,
                  left_margin_abs    = 0.55,
                  bottom_margin_abs  = 0.37,
                  f_ylabel_left      = 0.0175,
                  f_xlabel_bottom    = 0.35 )
# ---------------------------------

sed_list=[['0.1' , 'sed_jm0.1_2' ],
          ['0.25', 'sed_jm0.25_2'],
          ['0.5' , 'sed_jm0.5_2' ],
          ['0.75', 'sed_jm0.75_2'],
          ['0.9' , 'sed_jm0.9_2' ],
          ['0.95', 'sed_jm0.95_2']]

# create MPP
mpp=tdc_MPP(3,2, **fig_style)
mpp._change_fonsize([ g for g in flatten(mpp.grid)])

# set parameters (after figure is created)
tdc_set_hardcopy_rcparams()

## # plotters and labels
## plotters=[]
## j_labels=[]
## for jl,fn in sed_list:
##     j_labels.append( r'$j = %s\,j_{\rm GJ}$' % jl )
##     dump_dict = pickle.load( open('../RESULTS/SEDs/' + fn + '.pickle','r') )
##     plotters.append( tdc_XPs_Plotter(dump_dict['seds'][0].xp) )
## # do plotting 
## mpp.interactive_off()
## ip=0
## for i in range(0,mpp.ny):
##     for j in range(0,mpp.nx):
##         ax=mpp.grid[i][j]
##         plotters[ip].plot( ax )
##         ax.text(j_label_coord['x'],
##                 j_label_coord['y'],
##                 j_labels[ip],
##                 fontsize = j_label_fontsize )
##         ip+=1
## # xlabels
## for j in range(mpp.nx):
##     mpp.set_bottom_xlabel(j, r'$|p|$')
# draw figure
mpp.fig.canvas.draw()

## exec tick_and_labels_commands

mpp.interactive_on()
tdc_set_default_rcparams()

plt.interactive(True)
plt.show()
