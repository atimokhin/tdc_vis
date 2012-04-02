#!/usr/bin/python
import os

from Auxiliary        import *
from Common_Data_Plot import *
from Plots            import *

from x_Tests.plot_test_e_e_gauss_movie import *


# ============================================================
# Figure Style Parameters
# ============================================================
fig_param = paramSingleFig_Presentation
## fig_param = None


# ============================================================
# Directory
# ============================================================
## tdc_set_results_dir('../RESULTS/')
tdc_set_results_dir('../RESULTS/WD/RS')


# ============================================================
# IDs 
# ============================================================
IDs=['RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU']


# ============================================================
# plot limits:
# ============================================================
xlim = [-0.005,0.305]

ylim_xp  = [-1.7e5,1.7e5]
ylim_rho = [-100,100]
ylim_j   = [-100,100]
ylim_e   = [-2.001,2.001]
ylim_phi = [-0.5,0.5]


axes_commands_xp = ['set_yticks([-1e8,-1e4,0,1e4,1e8])']
## axes_commands_xp = None
## # ----------------------------------------



sample_dict    = dict(name='regular',n_reduce=1,n_min=1000)
## sample_dict    = dict(name='regular',n_reduce=20,n_min=3000)

particle_names = ['Positrons','Electrons','Pairs']

symlog=True
linthreshy=5

tt = None

fps = 9
keep_frame_files=False

use_cell_coordinates=False
show_cells=False
ghost_points=False

## moving_grid_dict = dict(n_lines=30, speed=1)
moving_grid_dict = None
# ==================



# ============================================================
# Plots 
# ============================================================

Plots = {'XP'           : True,
         'Rho'          : False,
         'J'            : False,
         'E_acc'        : False,
         'E_Gauss'      : False,
         'E__E_Gauss'   : False,
         'Phi'          : False,
         'EP'           : False,
         'EPG'          : False,
         'EPGP'         : False,
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
                              symlog=symlog,
                              linthreshy=linthreshy,
                              axes_commands = axes_commands_xp,
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
                                 ylim=ylim_j,
                                 xlim=xlim,
                                 moving_grid_dict=moving_grid_dict,
                                 tt=tt,
                                 fps=fps,
                                 keep_frame_files=keep_frame_files,
                                 use_cell_coordinates=use_cell_coordinates,
                                 show_cells=show_cells,
                                 ghost_points=True,
                                 fig_param = fig_param)
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
                                 keep_frame_files=keep_frame_files,
                                 use_cell_coordinates=use_cell_coordinates,
                                 show_cells=show_cells,
                                 ghost_points=True,
                                 fig_param = fig_param)
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
                                 keep_frame_files=keep_frame_files,
                                 use_cell_coordinates=use_cell_coordinates,
                                 show_cells=show_cells,
                                 ghost_points=True,
                                 fig_param = fig_param)
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
                                      fps=fps,
                                      keep_frame_files=keep_frame_files,
                                      use_cell_coordinates=use_cell_coordinates,
                                      show_cells=show_cells,
                                      time_normalization = 'absolute',
                                      ghost_points=True,
                                      fig_param = fig_param)
        # ~~~~~~~~~~~~~~~~~~~~~~~~

        # ~~~~~~~~~~~~~~~~~~~~~~~~
        # Phi
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        if Plots['Phi']:
            tdc_plot_field_movie(plot_module,
                                 ID,
                                 'Phi',
                                 ylim=ylim_phi,
                                 tt=tt,
                                 fps=fps,
                                 keep_frame_files=keep_frame_files,
                                 use_cell_coordinates=use_cell_coordinates,
                                 show_cells=show_cells,
                                 time_normalization = 'absolute',
                                 moving_grid_dict=moving_grid_dict,
                                 fig_param = fig_param)
        # ~~~~~~~~~~~~~~~~~~~~~~~~

        # ~~~~~~~~~~~~~~~~~~~~~~~~
        # Particle Number Density
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        if Plots['EP']:
            tdc_plot_ep_density_movie(plot_module,
                                      ID,
                                      ylim=ylim_ep,
                                      xlim=xlim,
                                      tt=tt,
                                      e_density_negative=False,
                                      fps=fps,
                                      keep_frame_files=keep_frame_files,
                                      use_cell_coordinates=use_cell_coordinates,
                                      show_cells=show_cells,
                                      time_normalization = 'absolute',
                                      moving_grid_dict=moving_grid_dict,
                                      fig_param = fig_param)
        # ~~~~~~~~~~~~~~~~~~~~~~~~

        # ~~~~~~~~~~~~~~~~~~~~~~~~
        # Particle Number Density
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        if Plots['EPG']:
            tdc_plot_epg_density_movie(plot_module,
                                       ID,
                                       ylim=ylim_ep,
                                       xlim=xlim,
                                       tt=tt,
                                       e_density_negative=False,
                                       fps=fps,
                                       keep_frame_files=keep_frame_files,
                                       use_cell_coordinates=use_cell_coordinates,
                                       show_cells=show_cells,
                                       time_normalization = 'absolute',
                                       moving_grid_dict=moving_grid_dict,
                                       fig_param = fig_param)
        # ~~~~~~~~~~~~~~~~~~~~~~~~

        # ~~~~~~~~~~~~~~~~~~~~~~~~
        # Particle Number Density
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        if Plots['EPGP']:
            tdc_plot_epgp_density_movie(plot_module,
                                        ID,
                                        ylim=ylim_ep,
                                        xlim=xlim,
                                        tt=tt,
                                        fps=fps,
                                        e_density_negative=False,
                                        keep_frame_files=keep_frame_files,
                                        use_cell_coordinates=use_cell_coordinates,
                                        show_cells=show_cells,
                                        time_normalization = 'absolute',
                                        moving_grid_dict=moving_grid_dict,
                                        fig_param = fig_param)
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
