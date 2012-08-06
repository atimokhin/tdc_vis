import matplotlib.pyplot as plt
from   matplotlib.cbook  import flatten
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
for i in range(3):
    mpp.grid[0][i].set_xlim([-2,52])
    mpp.grid[0][i].set_xticks([0,25,50])
    mpp.grid[0][i].set_xticks(np.arange(5,50,5),minor=True)
    mpp.grid[0][i].set_xticklabels(['0','25','50'])

mpp.grid[1][0].set_xlim([-4,104])
mpp.grid[1][0].set_xticks(np.arange(0,101,50))
mpp.grid[1][0].set_xticklabels(['0','50','100'])
mpp.grid[1][0].set_xticks(np.arange(0,100,10),minor=True)

mpp.grid[1][1].set_xlim([-12,312])
mpp.grid[1][1].set_xticks(np.arange(0,301,100))
mpp.grid[1][1].set_xticklabels(['0','100','200','300'])
mpp.grid[1][1].set_xticks(np.arange(50,300,100),minor=True)

mpp.grid[1][2].set_xlim([-30,830])
mpp.grid[1][2].set_xticks(np.arange(0,801,200))
mpp.grid[1][2].set_xticklabels(['0','200','400','600', '800'])
mpp.grid[1][2].set_xticks(np.arange(100,800,200),minor=True)

mpp.grid[0][0].set_ylim([-1.15,1.15])
mpp.grid[0][0].set_yticks([-1,0,1])
mpp.grid[0][0].set_yticklabels(['-1','0','1'])
mpp.grid[0][0].set_yticks([-0.5,0.5],minor=True)

for i in [1,2]:
    mpp.grid[0][i].set_ylim([-2.6,2.6])
    mpp.grid[0][i].set_yticks([-2,0,2])
    mpp.grid[0][i].set_yticklabels(['-2','0','2'])
    mpp.grid[0][i].set_yticks([-1,1],minor=True)

for i in range(3):
    mpp.grid[1][i].set_ylim([-5.5,5.5])
    mpp.grid[1][i].set_yticks([-5,0,5])
    mpp.grid[1][i].set_yticklabels(['-5','0','5'])
    mpp.grid[1][i].set_yticks([-2.5,2.5],minor=True)

"""

j_label_coord={'x' : 0.038, 'y' : .69}
j_label_fontsize = 9
    
fig_param = dict( dx_pad_abs          = 0.30,
                  dy_pad_abs          = 0.25,
                  left_margin_abs     = 0.40,
                  top_margin_abs      = 0.1,
                  yticklabel_fontsize = 9 )
# ---------------------------------


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
    j_labels.append( r'$j_{\rm m} = %s\,j_{\rm GJ}$' % jl )
    # full file name of the file with manipulator dump
    filename=tdc_Filenames().get_full_vis_filename(dump_id, filename+'.pickle')
    dump_dict = pickle.load( open(filename,'r') )
    plotters.append( tdc_Fields_Plotter(dump_dict['fft_data'][0].field) )
# do plotting 
mpp.interactive_off()
ip=0
for i in range(0,mpp.ny):
    for j in range(0,mpp.nx):
        ax=mpp.grid[i][j]
        plotters[ip].plot( ax )
        ip+=1
# xlabels
for j in range(mpp.nx):
    mpp.set_bottom_xlabel(j, r'$x\,[\lambda_{\rm D}]$')
# ylabels
ylabel=plotters[0].plot_ylabel
mpp.set_ylabel(0,ylabel)
mpp.set_ylabel(1,ylabel)
# draw figure
mpp.fig.canvas.draw()
# ticks and tick labels
exec tick_and_labels_commands
mpp._change_fonsize([ g for g in flatten(mpp.grid)])
# current labels --
ip=0
for i in range(0,mpp.ny):
    for j in range(0,mpp.nx):
        ax=mpp.grid[i][j]
        ax.text(j_label_coord['x']*ax.get_xlim()[1],
                j_label_coord['y']*ax.get_ylim()[1],
                j_labels[ip],
                fontsize = j_label_fontsize )
        ip+=1
#------------------
mpp.interactive_on()

plt.show()

plt.interactive(True)
