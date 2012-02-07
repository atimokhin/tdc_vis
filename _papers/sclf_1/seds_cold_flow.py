import matplotlib.pyplot as plt
import numpy             as np

from Auxiliary        import *
from Common_Data_Plot import *

from Particles import *

from MPP import tdc_MPP_H

import pickle

from plot_params import mpp_params
# -------------------------

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
tdc_set_hardcopy_rcparams()
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


#tdc_set_results_dir('../RESULTS/FreeAgent/')

# ------------------------------
# SubDirectory with dumped files
# ------------------------------
dump_id='__TDC_2/SEDs'


tick_and_labels_commands="""
mpp.set_xlim([0.06,80])
mpp.set_xticks([0.1,1,10])
mpp.set_xticklabels(['0.1','1','10'])

mpp.set_ylim( (0,1), [3e-4,30])
mpp.set_yticks( (0,1), [1e-3, 1e-2, 0.1, 1, 10] )
mpp.set_yticklabels( (0,1),['10^{-3}','10^{-2}','0.1','1','10'], tex=True, size=8 )

mpp._delete_xlabels_for_middle_plots()
mpp._delete_ylabels_for_middle_plots()
"""

j_label_coord={'x' : 0.09, 'y' : 5}
j_label_fontsize=8
    
mpp_params['dx_pad_abs']      = 0.07
mpp_params['dy_pad_abs']      = 0.07
mpp_params['left_margin_abs'] = 0.65
mpp_params['top_margin_abs']  = 0.1
# ---------------------------------

sed_list=[['0.1' , 'sed_jm0.1_2' ],
          ['0.25', 'sed_jm0.25_2'],
          ['0.5' , 'sed_jm0.5_2' ],
          ['0.75', 'sed_jm0.75_2'],
          ['0.9' , 'sed_jm0.9_2' ],
          ['0.95', 'sed_jm0.95_2']]

# create MPP
mpp=tdc_MPP_H(3,2, **mpp_params)
# plotters and labels
plotters=[]
j_labels=[]
for jl,filename in sed_list:
    j_labels.append( r'$j_0 = %s\,j_{\rm GJ}$' % jl )
    # full file name of the file with manipulator dump
    filename=tdc_Filenames().get_full_vis_filename(dump_id, filename+'.pickle')
    dump_dict = pickle.load( open(filename,'r') )
    plotters.append( tdc_SEDs_Plotter(dump_dict['seds']) )
# do plotting 
mpp.interactive_off()
ip=0
for i in range(0,mpp.ny):
    for j in range(0,mpp.nx):
        ax=mpp.grid[i][j]
        plotters[ip].plot( ax )
        ax.text(j_label_coord['x'],
                j_label_coord['y'],
                j_labels[ip],
                fontsize = j_label_fontsize )
        ip+=1
# xlabels
for j in range(mpp.nx):
    mpp.set_bottom_xlabel(j, r'$|p|$')
# ylabels
ylabel=r'$\displaystyle{}p\:\frac{\partial\!n}{\partial{}\!p}$'
mpp.set_ylabel(0,ylabel)
mpp.set_ylabel(1,ylabel)
# draw figure
mpp.fig.canvas.draw()

exec tick_and_labels_commands

mpp.interactive_on()

plt.show()

plt.interactive(True)
