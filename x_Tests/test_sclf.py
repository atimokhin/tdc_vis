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
ID=['sclf_test_nx2e3_jm1.0_injP']

# ============================================================
# Plots 
# ============================================================
Plots = {'Rho'          : True,
         'J'            : True,
         'E_acc'        : True,
         'E_Gauss'      : True,
         'E__E_Gauss'   : True,
         'Phi'          : True,
         'XP'           : True}
# ============================================================



def do_movie(ID):
    moving_grid_dict = None

    tt = None    
    ghost_points = True  
    use_cell_coordinates=False
    show_cells=False

    xlim=[-0.05,1.05]
    ylim=[-0.5,12]

    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # Rho
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    if Plots['Rho']:
        tdc_plot_field_movie(plot_module,
                             ID,
                             'Rho',
                             ylim=[-5,5],
                             xlim=xlim,
                             tt=tt,
                             fps=15,
                             use_cell_coordinates=use_cell_coordinates,
                             show_cells=show_cells,
                             ghost_points=ghost_points)
    # ~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # J
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    if Plots['J']:
        tdc_plot_field_movie(plot_module,
                             ID,
                             'J',
                             ylim=[-2,2],
                             xlim=xlim,
                             use_cell_coordinates=use_cell_coordinates,
                             show_cells=show_cells,
                             ghost_points=ghost_points)
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # E_acc
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    if Plots['E_acc']:
        tdc_plot_field_movie(plot_module,
                             ID,
                             'E_acc',
                             ylim=[-4,1],
                             xlim=xlim,
                             tt=tt,
                             use_cell_coordinates=use_cell_coordinates,
                             show_cells=show_cells,
                             ghost_points=ghost_points)
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # E_acc Gauss
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    if Plots['E__E_Gauss']:
        tdc_plot_field_movie(plot_module,
                             ID,
                             'E_Gauss',
                             ylim=[-4,1],
                             xlim=xlim,
                             tt=tt,
                             use_cell_coordinates=use_cell_coordinates,
                             show_cells=show_cells,
                             ghost_points=ghost_points)
    # ~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # plot Electric field and difference between Gauss' and Ampere's Electric fields
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    if Plots['E__E_Gauss']:
        plot_test_e_e_gauss_movie(plot_module,
                                  ID,
                                  ylim=[[-4,1],[-1e-1,1e-1]],
                                  xlim=[xlim,xlim],
                                  tt=tt,
                                  use_cell_coordinates=use_cell_coordinates,
                                  show_cells=show_cells,
                                  time_normalization = 'absolute',
                                  ghost_points=True)
    # ~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # Phi
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    if Plots['Phi']:
        tdc_plot_field_movie(plot_module,
                             ID,
                             'Phi',
                             ylim=[-1.1,1.1],
                             xlim=xlim,
                             use_cell_coordinates=use_cell_coordinates,
                             show_cells=show_cells,
                             ghost_points=True,
                             time_normalization = 'absolute')
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # XP Movie with theoretical curves
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    if Plots['XP']:
        tp = None
        trail_dict = None
        
        sample_dict    = dict(name='regular',n_reduce=1,n_min=1000)
        particle_names = ['Protons','Electrons']
        
        sclf.plot_test_sclf_xp_movie(plot_module,
                                     ID,
                                     particle_names,
                                     sample_dict=sample_dict,
                                     tt=tt,
                                     ylim=ylim,
                                     xlim=xlim,
                                     use_cell_coordinates=use_cell_coordinates,
                                     show_cells=show_cells,
                                     moving_grid_dict=moving_grid_dict)


if __name__ == "__main__":
    do_movie(ID)
