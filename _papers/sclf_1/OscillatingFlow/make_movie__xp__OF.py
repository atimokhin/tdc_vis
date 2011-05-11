#!/usr/bin/python

from Common  import *
from Plots   import *

from plot_xp__OF_movie import *



# ============================================================
# Interface
# ============================================================
import Plot_GUI as plot_module
## import Plot_CMD as plot_module

# ============================================================
# Directory
# ============================================================
tdc_set_results_dir('../RESULTS/')
## tdc_set_results_dir('../RESULTS/FreeAgent/')

# ============================================================
# ID 
# ============================================================
ID=['SCLF__jm0.5_L50_X0.5_nGJ2e5_nx5e3_dt2e-3__RhoGJConst__noMC__dP5e-2_inj15_s1',
    'SCLF__jm0.5_L50_X0.5_nGJ2e5_nx5e3_dt2e-3__RhoGJConst__noMC__dP5e-2_inj15_s1__1']

# ============================================================
# OF solution file 
# ============================================================
of__filename = 'OF__j05'

# ============================================================
# Plots 
# ============================================================
Plots = {'XP'           : True}
# ============================================================

#-----------------
# plot limits:
# ----------------
xlim=[-0.05,50.05]
# ----------------

tt=None
fps = 14

use_cell_coordinates=False
show_cells=False

keep_frame_files=False

## moving_grid_dict = dict(n_lines=30, speed=1)
moving_grid_dict = None
# ================


def do_movie(ID):
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # XP Movie with theoretical curves
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    if Plots['XP']:
        tp = None
        trail_dict = None
        
        sample_dict    = dict(name='regular',n_reduce=1,n_min=1000)
        particle_names = ['Electrons']
        
        plot_xp__OF_movie(plot_module,
                          ID,
                          particle_names,
                          ylim=[-4,4],
                          of__filename=of__filename,
                          sample_dict=sample_dict,
                          tt=tt,
                          fps=fps,
                          xlim=xlim,
                          use_cell_coordinates=use_cell_coordinates,
                          show_cells=show_cells,
                          moving_grid_dict=moving_grid_dict)


if __name__ == "__main__":
    do_movie(ID)