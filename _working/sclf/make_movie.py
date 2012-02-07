#!/usr/bin/python
import os

from Auxiliary        import *
from Common_Data_Plot import *
from Plots  import *

from x_Tests.plot_test_e_e_gauss_movie import *

# ============================================================
# Figure Style Parameters
# ============================================================
fig_param = paramSingleFig_Presentation


# ============================================================
# Directory
# ============================================================
tdc_set_results_dir('../RESULTS/__TDC_2/')
## tdc_set_results_dir('../RESULTS/FreeAgent/')


# ============================================================
# IDs 
# ============================================================
## IDs=['SCLF__jm0.5_L50_X0.5_nGJ2e5_nx5e3_dt2e-3__RhoGJConst__noMC__dP5e-2_inj15_s1']

IDs=[['SCLF__jm0.5_L50_X0.5_nGJ2e5_nx5e3_dt2e-3__RhoGJConst__noMC__dP5e-2_inj15_s1',
      'SCLF__jm0.5_L50_X0.5_nGJ2e5_nx5e3_dt2e-3__RhoGJConst__noMC__dP5e-2_inj15_s1__1']]

#-----------------
# xlabel
#-----------------
xlabel_Debye=r'$x\;[\lambda_{\mathrm{D}}]$'
                              
#-----------------
# plot limits:
# ----------------
xlim = [-1,51]

## # jm0.1 ---
## ylim_xp = [-0.8,0.8]
## ylim_e  = [-1,1]
## # jm0.25 ---
## ylim_xp = [-1.5,1.5]
## ylim_e  = [-1.5,1.5]
# jm0.5 ---
ylim_xp = [-3.5,3.5]
axes_commands_xp = None
ylim_e  = [-3,3]
## # jm0.75 ---
## ylim_xp = [-10,10]
## ylim_e  = [-5,5]
## # jm0.9 ---
## ylim_xp = [-25,25]
## ylim_e  = [-7,7]
## # jm0.95 ---
## ylim_xp = [-40,40]
## ylim_e  = [-7,7]
## # jm1 ---
## ylim_xp = [-10,150]
## ylim_e  = [-10,1]

tt=None
fps = 14

use_cell_coordinates=False
show_cells=False

keep_frame_files=False

## moving_grid_dict = dict(n_lines=30, speed=1)
moving_grid_dict = None
# ==================


# ============================================================
# Plots 
# ============================================================
Plots = {'XP'           : True,
         'Rho'          : True,
         'J'            : False,
         'E_acc'        : False,
         'E_Gauss'      : False,
         'E__E_Gauss'   : False,
         'Phi'          : False,
         'EP'           : False,
         'Trajectories' : False }
# ============================================================



def do_movie(IDs):
    # ==========================================
    # Interface
    # ==========================================
    interface = os.environ.get('MPL_INTERFACE','GUI')
    if interface=='GUI':
        import Plot_GUI as plot_module
    else:
        import Plot_CMD as plot_module
    # ==========================================

    # iterate over IDs <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    for ID in IDs:

        # ~~~~~~~~~~~~~~~~~~~~~~~~
        # XP Movie
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        if Plots['XP']:
            tp = None
            ## tp = tdc_TP_Data()
            ## tp.setup_from_file(ID,'p500_ts525')
            ## tp.delete(range(0,47,2))
            
            sample_dict    = dict(name='regular',n_reduce=1,n_min=1000)
            ## particle_names = ['Electrons','Protons']
            particle_names = ['Electrons']

            tdc_plot_xp_movie(plot_module,
                              ID,
                              particle_names,
                              ylim=ylim_xp,
                              xlim=xlim,
                              sample_dict=sample_dict,
                              tt=tt,
                              fps=fps,
                              keep_frame_files=keep_frame_files,
                              use_cell_coordinates=use_cell_coordinates,
                              show_cells=show_cells,
                              tp=tp,
                              trail_dict=dict(length=18,marker='numbers'),
                              moving_grid_dict=moving_grid_dict,
                              axes_commands = axes_commands_xp,
                              xlabel = xlabel_Debye,
                              fig_param = fig_param)
        # ~~~~~~~~~~~~~~~~~~~~~~~~


        # ~~~~~~~~~~~~~~~~~~~~~~~~
        # Rho
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        if Plots['Rho']:
            tdc_plot_field_movie(plot_module,
                                 ID,
                                 'Rho',
                                 ylim=[-3,3],
                                 xlim=xlim,
                                 moving_grid_dict=moving_grid_dict,
                                 tt=tt,
                                 fps=fps,
                                 use_cell_coordinates=use_cell_coordinates,
                                 show_cells=show_cells,
                                 ghost_points=True,
                                 xlabel = xlabel_Debye,
                                 fig_param = fig_param)
        # ~~~~~~~~~~~~~~~~~~~~~~~~

        # ~~~~~~~~~~~~~~~~~~~~~~~~
        # J
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        if Plots['J']:
            tdc_plot_field_movie(plot_module,
                                 ID,
                                 'J',
                                 ylim=[-3,3],
                                 xlim=xlim,
                                 moving_grid_dict=moving_grid_dict,
                                 tt=tt,
                                 fps=fps,
                                 use_cell_coordinates=use_cell_coordinates,
                                 show_cells=show_cells,
                                 ghost_points=True,
                                 xlabel = xlabel_Debye)
        # ~~~~~~~~~~~~~~~~~~~~~~~~

        # ~~~~~~~~~~~~~~~~~~~~~~~~
        # E_acc
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        if Plots['E_acc']:
            tdc_plot_field_movie(plot_module,
                                 ID,
                                 'E_acc',
                                 ylim=ylim_e,
                                 xlim=xlim,
                                 moving_grid_dict=moving_grid_dict,
                                 tt=tt,
                                 fps=fps,
                                 use_cell_coordinates=use_cell_coordinates,
                                 show_cells=show_cells,
                                 ghost_points=True,
                                 xlabel = xlabel_Debye)
        # ~~~~~~~~~~~~~~~~~~~~~~~~

        # ~~~~~~~~~~~~~~~~~~~~~~~~
        # E_Gauss
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        if Plots['E_Gauss']:
            tdc_plot_field_movie(plot_module,
                                 ID,
                                 'E_Gauss',
                                 ylim=ylim_e,
                                 xlim=xlim,
                                 moving_grid_dict=moving_grid_dict,
                                 tt=tt,
                                 fps=fps,
                                 use_cell_coordinates=use_cell_coordinates,
                                 show_cells=show_cells,
                                 ghost_points=True,
                                 xlabel = xlabel_Debye)
        # ~~~~~~~~~~~~~~~~~~~~~~~~


        # ~~~~~~~~~~~~~~~~~~~~~~~~
        # E__E_Gauss
        #  plot Electric field and difference between Gauss' and Ampere's Electric fields
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        if Plots['E__E_Gauss']:
            plot_test_e_e_gauss_movie(plot_module,
                                      ID,
                                      ylim=[ylim_e,[-1e-2,1e-2]],
                                      xlim=[xlim,xlim],
                                      tt=tt,
                                      fps=15,
                                      use_cell_coordinates=use_cell_coordinates,
                                      show_cells=show_cells,
                                      time_normalization = 'absolute',
                                      ghost_points=True,
                                      xlabel = xlabel_Debye,
                                      fig_param = fig_param)
        # ~~~~~~~~~~~~~~~~~~~~~~~~


        # ~~~~~~~~~~~~~~~~~~~~~~~~
        # Phi
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        if Plots['Phi']:
            tdc_plot_field_movie(plot_module,
                                 ID,
                                 'Phi',
                                 ylim=[-.5,.1],
                                 moving_grid_dict=moving_grid_dict)
        # ~~~~~~~~~~~~~~~~~~~~~~~~

        # ~~~~~~~~~~~~~~~~~~~~~~~~
        # Particle Number Density
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        if Plots['EP']:
            tdc_plot_ep_density_movie(plot_module,
                                      ID,
                                      ylim=[0,60],
                                      e_density_negative=False,
                                      moving_grid_dict=moving_grid_dict,
                                      xlabel = xlabel_Debye)
        # ~~~~~~~~~~~~~~~~~~~~~~~~


        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## # particles trajectories
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## tp.setup_from_file(ID,'p1e7_ts90_ignition')
        ## tp.select([0,3,12,19,25])

        ## ## #tp.setup_from_file(ID,'p1e3_ts70_tail')
        ## ## #tp.select([15,18,7,29,33])

        ## ## #tp.setup_from_file(ID,'p1e3_ts70_tail_1')

        ## tp.setup_from_file(ID,'p1e3_ts70_tail_2')
        ## #tp.delete([5,33,27,29,25,44])
        ## e_list = [13,19,18,41,8,49,54,28,24]
        ## p_list = [56,45,52,2,40,42,14,57,48,4,39,38,34]
        ## tp.select(e_list[:-1:3]+p_list[:-1:3])
        ## # ------------------------

        ## tt=tp.time_interval
        ## tdc_plot_tp_movie(tp, ylim=[-1e4,1e4],
        ##                   trail_dict=dict(length=50,marker='numbers'),
        ##                   tt=tt,
        ##                   moving_grid_dict=moving_grid_dict )
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~



if __name__ == "__main__":
    do_movie(IDs)
