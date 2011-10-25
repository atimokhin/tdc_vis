#!/usr/bin/python

from Auxiliary        import *
from Common_Data_Plot import *
from Plots            import *

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
ID=['test_2stream_ymax']
# ============================================================



def do_movie(ID):
    ## moving_grid_dict = dict(n_lines=30, speed=1)
    moving_grid_dict = None
    tt = None    
    #tt = [0,4]
    ghost_points=True  
    xlim=None

    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## # Rho
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## tdc_plot_field_movie(plot_module,
    ##                      ID,
    ##                      'Rho',
    ##                      ylim=[-5,5],
    ##                      xlim=xlim,
    ##                      tt=tt,
    ##                      fps=15,
    ##                      moving_grid_dict=moving_grid_dict,
    ##                      ghost_points=ghost_points)
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~

    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## # J
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## tdc_plot_field_movie(ID,
    ##                      'J',
    ##                      ylim=[-0.005,0.005],
    ##                      moving_grid_dict=moving_grid_dict,
    ##                      time_normalization = 'absolute')
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
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # E_acc
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    tdc_plot_field_movie(plot_module,
                         ID,
                         'E_acc',
                         ylim=[-1,1],
                         xlim=xlim,
                         tt=tt,
                         moving_grid_dict=moving_grid_dict,
                         ghost_points=ghost_points)
    # ~~~~~~~~~~~~~~~~~~~~~~~~
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

    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # plot Electric field and difference between Gauss' and Ampere's Electric fields
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    plot_test_e_e_gauss_movie(plot_module,
                              ID,
                              ylim=[[-1,1],[-1e-13,1e-13]],
                              xlim=[xlim,xlim],
                              tt=tt,
                              fps=15,
                              use_cell_coordinates=False,
                              show_cells=False,
                              time_normalization = 'absolute',
                              ghost_points=True)
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # XP Movie
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    tp = None
    trail_dict = None
    
    sample_dict    = dict(name='regular',n_reduce=1,n_min=1000)
    particle_names = ['Electrons','Positrons']

    tdc_plot_xp_movie(plot_module,
                      ID,
                      particle_names,
                      sample_dict=sample_dict,
                      tp=tp,
                      trail_dict=trail_dict,
                      tt=tt,
                      ylim=[-4,4],
                      xlim=xlim,
                      moving_grid_dict=moving_grid_dict)
    # ~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":
    do_movie(ID)
