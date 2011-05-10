import matplotlib.pyplot as plt
from   matplotlib.cbook  import flatten
import numpy             as np
import pickle

from Common    import *
from Particles import *

from MPP import tdc_MPP

from plot_params import mpp_params


tick_and_labels_commands="""
for i in range(3):
    mpp.grid[0][i].set_xlim([-1,51])
    mpp.grid[0][i].set_xticks([0,25,50])
    mpp.grid[0][i].set_xticks(np.arange(5,50,5),minor=True)
    mpp.grid[0][i].set_xticklabels(['0','25','50'])

mpp.grid[1][0].set_xlim([-1,101])
mpp.grid[1][0].set_xticks(np.arange(0,101,50))
mpp.grid[1][0].set_xticklabels(['0','50','100'])
mpp.grid[1][0].set_xticks(np.arange(0,100,10),minor=True)

mpp.grid[1][1].set_xlim([-5,305])
mpp.grid[1][1].set_xticks(np.arange(0,301,100))
mpp.grid[1][1].set_xticklabels(['0','100','200','300'])
mpp.grid[1][1].set_xticks(np.arange(50,300,100),minor=True)

mpp.grid[1][2].set_xlim([-10,820])
mpp.grid[1][2].set_xticks(np.arange(0,801,200))
mpp.grid[1][2].set_xticklabels(['0','200','400','600', '800'])
mpp.grid[1][2].set_xticks(np.arange(100,800,200),minor=True)

mpp.grid[0][0].set_ylim([-1.15,1.15])
mpp.grid[0][0].set_yticks([-1,0,1])
mpp.grid[0][0].set_yticklabels(['-1','0','1'])
mpp.grid[0][0].set_yticks([-0.5,0.5],minor=True)

mpp.grid[0][1].set_ylim([-2.3,2.3])
mpp.grid[0][1].set_yticks([-2,-1,0,1,2])
mpp.grid[0][1].set_yticklabels(['-2','-1','0','1','2'])

mpp.grid[0][2].set_ylim([-4.6,4.6])
mpp.grid[0][2].set_yticks([-4,-2,0,2,4])
mpp.grid[0][2].set_yticklabels(['-4','-2','0','2','4'])

mpp.grid[1][0].set_ylim([-13,13])
mpp.grid[1][0].set_yticks([-10,0,10])
mpp.grid[1][0].set_yticklabels(['-10','0','10'])
mpp.grid[1][0].set_yticks([-5,5],minor=True)

mpp.grid[1][1].set_ylim([-26,26])
mpp.grid[1][1].set_yticks([-20,-10,0,10,20])
mpp.grid[1][1].set_yticklabels(['-20','-10','0','10','20'])

mpp.grid[1][2].set_ylim([-52,52])
mpp.grid[1][2].set_yticks([-40,-20,0,20, 40])
mpp.grid[1][2].set_yticklabels(['-40','-20','0','20','40'])
"""

j_label_coord={'x' : 0.038, 'y' : .75}
j_label_fontsize = 8
    
mpp_params['dx_pad_abs']      = 0.30
mpp_params['dy_pad_abs']      = 0.25
mpp_params['left_margin_abs'] = 0.40
mpp_params['top_margin_abs']  = 0.1

# ---------------------------------

sed_list=[['0.1' , 'sed_jm0.1_2' ],
          ['0.25', 'sed_jm0.25_2'],
          ['0.5' , 'sed_jm0.5_2' ],
          ['0.75', 'sed_jm0.75_2'],
          ['0.9' , 'sed_jm0.9_2' ],
          ['0.95', 'sed_jm0.95_2']]

# create MPP
mpp=tdc_MPP(3,2, **mpp_params)
# set parameters (after figure is created)
tdc_set_hardcopy_rcparams()

# set parameters (after figure is created)
tdc_set_hardcopy_rcparams()

# plotters and labels
plotters=[]
j_labels=[]
for jl,fn in sed_list:
    j_labels.append( r'$j_0 = %s\,j_{\rm GJ}$' % jl )
    dump_dict = pickle.load( open('../RESULTS/__TDC_2/SEDs__OF/' + fn + '.pickle','r') )
    plotters.append( tdc_XPs_Plotter( (dump_dict['seds'][0].xp,)) )
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
mpp.set_ylabel(0,plotters[0].plot_ylabel)
mpp.set_ylabel(1,plotters[0].plot_ylabel)
# ticke and tick labels
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
tdc_set_default_rcparams()
# draw figure
mpp.fig.canvas.draw()
plt.interactive(True)
plt.show()
