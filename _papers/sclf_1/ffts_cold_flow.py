import matplotlib.pyplot as plt
import numpy             as np

from Auxiliary        import *
from Common_Data_Plot import *

from Fields import *

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
dump_id='__TDC_2/FFTs'


tick_and_labels_commands="""
mpp.set_xlim([2e-3,130])

mpp.set_ylim( (0,1), [1e-5,5e7])
mpp.set_yticks( (0,1), [1e-4, 1e-2, 1, 1e2, 1e4, 1e6] )

mpp._delete_xlabels_for_middle_plots()
mpp._delete_ylabels_for_middle_plots()
"""

j_label_coord={'x' : 0.004, 'y' : 1e-3}
j_label_fontsize=9
    
fig_param = dict( dx_pad_abs          = 0.07,
                  dy_pad_abs          = 0.07,
                  left_margin_abs     = 0.65,
                  top_margin_abs      = 0.1)
# ---------------------------------

## fft_list=[['0.1' , 'fft_jm0.1_2' ],
##           ['0.25', 'fft_jm0.25_2'],
##           ['0.5' , 'fft_jm0.5_2' ],
##           ['0.75', 'fft_jm0.75_2'],
##           ['0.9' , 'fft_jm0.9_2' ],
##           ['0.95', 'fft_jm0.95_2']]

fft_list=[['0.1' , 'fft_jm0.1_2' ],
          ['0.25', 'fft_jm0.25_1__a'],
          ['0.5' , 'fft_jm0.5_1__a' ],
          ['0.75', 'fft_jm0.75_2__a'],
          ['0.9' , 'fft_jm0.9_1__a' ],
          ['0.95', 'fft_jm0.95_2']]

# create MPP
mpp=tdc_MPP_H(3,2, fig_param=fig_param)
# plotters and labels
plotters=[]
j_labels=[]
for jl,filename in fft_list:
    j_labels.append( r'$j_0 = %s\,j_{\rm GJ}$' % jl )
    # full file name of the file with manipulator dump
    filename=tdc_Filenames().get_full_vis_filename(dump_id, filename+'.pickle')
    dump_dict = pickle.load( open(filename,'r') )
    plotters.append( tdc_FFT_Plotter(dump_dict['fft_data']) )
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
    mpp.set_bottom_xlabel(j, r'$k$')
# ylabels
ylabel=plotters[0].plot_ylabel
mpp.set_ylabel(0,ylabel)
mpp.set_ylabel(1,ylabel)
# draw figure
mpp.fig.canvas.draw()

exec tick_and_labels_commands

mpp.interactive_on()

plt.show()

plt.interactive(True)
