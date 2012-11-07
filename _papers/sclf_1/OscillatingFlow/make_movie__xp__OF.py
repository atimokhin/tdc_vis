#!/usr/bin/python
import os

from Auxiliary         import *
from Common_Data_Plot  import *
from x_PlottingFunctions           import *
from Movie             import Movie_Interface_Selector

from plot_xp__OF_movie import *


# ============================================================
# Figure Style Parameters
# ============================================================
fig_param = paramSingleFig_Presentation
## fig_param = None
        

# ============================================================
# Directory
# ============================================================
## tdc_Filenames.set_results_dir('../RESULTS/')
tdc_Filenames.set_results_dir('../RESULTS/__TDC_2')


tdc_Filenames.set_vis_results_dir('../RESULTS_VIS/TDC_Presentation')


# ============================================================
# ID 
# ============================================================
ID=['SCLF__jm0.5_L50_X0.5_nGJ2e5_nx5e3_dt2e-3__RhoGJConst__noMC__dP5e-2_inj15_s1',
    'SCLF__jm0.5_L50_X0.5_nGJ2e5_nx5e3_dt2e-3__RhoGJConst__noMC__dP5e-2_inj15_s1__1']
## ID=['sclf_test_L50_nx2e3_jm1.0_injP_inj8_xinjII']
# ============================================================
# OF solution file 
# ============================================================
of__filename = 'OF__j05'
## of__filename = 'OF__j10'

# ============================================================
# Plots 
# ============================================================
Plots = {'XP'           : True}
# ============================================================

#-----------------
# plot limits:
# ----------------

# j= 0.5 j_GJ
xlim=[-0.5,25.5]
ylim_xp=[-3.5,3.5]
# -----------
## # j= 1.0 j_GJ
## xlim=[-2,102]
## ylim_xp=[-2,150]
## # -----------


tt=None
tt=[-1,6]

fps = 15

use_cell_coordinates=False
show_cells=False

keep_frame_files=False

## moving_grid_dict = dict(n_lines=30, speed=1)
moving_grid_dict = None
# ================


def do_movie(ID):
    # select interface
    interface = Movie_Interface_Selector()

    
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # XP Movie with theoretical curves
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    if Plots['XP']:
        tp = None
        trail_dict = None
        
        sample_dict    = dict(name='regular',n_reduce=1,n_min=1000)
        particle_names = ['Electrons']
        
        plot_xp__OF_movie(interface.movie_module,
                          ID,
                          particle_names,
                          ylim=ylim_xp,
                          of__filename=of__filename,
                          sample_dict=sample_dict,
                          tt=tt,
                          fps=fps,
                          xlim=xlim,
                          use_cell_coordinates=use_cell_coordinates,
                          show_cells=show_cells,
                          moving_grid_dict=moving_grid_dict,
                          fig_param = fig_param)


if __name__ == "__main__":
    do_movie(ID)
