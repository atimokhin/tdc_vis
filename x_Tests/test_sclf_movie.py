#!/usr/bin/python

from Common  import *
from Plots   import *

import x_Tests.sclf as sclf

from plot_test_e_e_gauss_movie import *

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
ID=['sclf_test_jm1.0']
# ============================================================



def do_movie(ID):
    ## moving_grid_dict = dict(n_lines=30, speed=1)
    moving_grid_dict = None
    tt = None    
    ghost_points=True  
    xlim=[-0.05,1.05]

    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## # Rho
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## tdc_plot_field_movie(plot_module,
    ##                      ID,
    ##                      'Rho',
    ##                      ylim=[-15,15],
    ##                      xlim=xlim,
    ##                      tt=tt,
    ##                      fps=15,
    ##                      moving_grid_dict=moving_grid_dict,
    ##                      ghost_points=ghost_points)
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~

    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## # J
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## tdc_plot_field_movie(plot_module,
    ##                      ID,
    ##                      'J',
    ##                      ylim=[-2,2],
    ##                      moving_grid_dict=moving_grid_dict,
    ##                      ghost_points=ghost_points)
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## # Phi
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## tdc_plot_field_movie(plot_module,
    ##                      ID,
    ##                      'Phi',
    ##                      ylim=[-4,4],
    ##                      moving_grid_dict=moving_grid_dict,
    ##                      ghost_points=True,
    ##                      time_normalization = 'absolute')
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## # E_acc
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## tdc_plot_field_movie(plot_module,
    ##                      ID,
    ##                      'E_acc',
    ##                      ylim=[-1,1],
    ##                      xlim=xlim,
    ##                      tt=tt,
    ##                      moving_grid_dict=moving_grid_dict,
    ##                      ghost_points=ghost_points)
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## # E_acc Gauss
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## tdc_plot_field_movie(plot_module,
    ##                      ID,
    ##                      'E_Gauss',
    ##                      ylim=[-1,1],
    ##                      xlim=xlim,
    ##                      tt=tt,
    ##                      moving_grid_dict=moving_grid_dict,
    ##                      ghost_points=ghost_points)
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~

    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## # plot Electric field and difference between Gauss' and Ampere's Electric fields
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## plot_test_e_e_gauss_movie(plot_module,
    ##                           ID,
    ##                           ylim=[[-4,4],[-1e-1,1e-1]],
    ##                           xlim=[xlim,xlim],
    ##                           tt=tt,
    ##                           fps=15,
    ##                           use_cell_coordinates=False,
    ##                           show_cells=False,
    ##                           time_normalization = 'absolute',
    ##                           ghost_points=True)
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # XP Movie with theoretical curves
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    tp = None
    trail_dict=dict(length=18,marker='numbers')
    trail_dict = None
    
    sample_dict    = dict(name='regular',n_reduce=1,n_min=1000)
    particle_names = ['Protons','Electrons']

    sclf.plot_test_sclf_xp_movie(plot_module,
                                 ID,
                                 particle_names,
                                 sample_dict=sample_dict,
                                 tt=tt,
                                 ylim=[-0.5,1e3],
                                 xlim=xlim,
                                 use_cell_coordinates=False,
                                 show_cells=False,
                                 moving_grid_dict=moving_grid_dict)


if __name__ == "__main__":
    do_movie(ID)
