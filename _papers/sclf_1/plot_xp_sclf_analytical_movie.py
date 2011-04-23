#!/usr/bin/python

from Common  import *
from Plots   import *

import plot_xp_sclf_analytical as sclf_analytical



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
ID=['SCLF__jm0.5_L50_X0.5_nGJ2e5_nx5e3_dt2e-3__RhoGJConst__noMC__dP5e-2_inj15_s1']

# ============================================================
# Plots 
# ============================================================
Plots = {'XP'           : True}
# ============================================================



def do_movie(ID):
    moving_grid_dict = None

    tt = None    
    ghost_points = True  
    use_cell_coordinates=False
    show_cells=False

    xlim=[-0.05,50.05]
    

    
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # XP Movie with theoretical curves
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    if Plots['XP']:
        tp = None
        trail_dict = None
        
        sample_dict    = dict(name='regular',n_reduce=1,n_min=1000)
        particle_names = ['Electrons']
        
        sclf_analytical.plot_xp_sclf_analytical(plot_module,
                                                ID,
                                                particle_names,
                                                sample_dict=sample_dict,
                                                tt=tt,
                                                ylim=[-4,4],
                                                xlim=xlim,
                                                use_cell_coordinates=use_cell_coordinates,
                                                show_cells=show_cells,
                                                moving_grid_dict=moving_grid_dict)


if __name__ == "__main__":
    do_movie(ID)
