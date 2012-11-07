#!/usr/bin/python
import os

from Auxiliary        import *
from Common_Data_Plot import *
from x_PlottingFunctions          import *
from Movie            import Movie_Interface_Selector



# ============================================================
# Figure Style Parameters
# ============================================================
fig_param = paramSingleFig_Presentation
## fig_param = None


# ============================================================
# Directory
# ============================================================
# tdc_Filenames.set_results_dir('../RESULTS/WD')
tdc_Filenames.set_results_dir('../RESULTS/WD/RS')
## tdc_Filenames.set_results_dir('../RESULTS/WD/RS_2')
tdc_Filenames.set_results_dir('../RESULTS/WD/TDC_Presentation')


tdc_Filenames.set_vis_results_dir('../RESULTS_VIS/TDC_Presentation')

# ============================================================
# IDs 
# ============================================================
## ID=['RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU']
## ID=['RS__RD_jp0.95_P0.09_L0.6_nGJ5e4_nx5e3_dt4e-5_sU']
## ID=['RS__RD_jp0.5_P0.09_L0.6_nGJ5e4_nx5e3_dt4e-5_sU']

# ID=['RS__R6_jp0.5_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU']
ID=['RS__R6_jp0.5_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU__wave']


# ============================================================
# plot limits:
# ============================================================
xlims = [[-0.005,0.305],[-0.005,0.305]]

ylims_xp_e  = [[-5e8,5e8],[-.15,0.45]]


axes_commands_xp = [['set_yticks([-1e8,-1e4,0,1e4,1e8])',
                     'set_xticks([0,0.1,0.2, 0.3])',
                     'xaxis.set_ticklabels([])'],
                    ['set_yticks([0,0.2,0.4])',
                     'set_yticks([-0.1,0.1,0.3],minor=True)',
                     'set_xticks([0,0.1,0.2, 0.3])']]
## axes_commands_xp = None
## # ----------------------------------------



sample_dict = dict(name='regular',n_reduce=1,n_min=1000)
## sample_dict = dict(name='regular',n_reduce=20,n_min=3000)

particle_names = ['Positrons','Electrons','Pairs']

symlog=True
linthreshy=5

tt = None
tt = [12.253,12.633]

fps = 24
keep_frame_files=True

use_cell_coordinates=False
show_cells=False
ghost_points=False

# moving_grid_dict = None
moving_grid_dict = dict(n_lines=20, speed=1)
# ==================



def do_movie(ID):
    # select interface
    interface = Movie_Interface_Selector()
    
    tdc_plot_wave_xp_e_movie(interface.movie_module,
                             ID,
                             particle_names,
                             ylims=ylims_xp_e,
                             xlims=xlims,
                             sample_dict=sample_dict,
                             tt=tt,
                             fps=fps,
                             keep_frame_files=keep_frame_files,
                             use_cell_coordinates=use_cell_coordinates,
                             show_cells=show_cells,
                             moving_grid_dict=moving_grid_dict,
                             symlog=symlog,
                             linthreshy=linthreshy,
                             axes_commands = axes_commands_xp,
                             xlabel=None,ylabel=None,idlabel=None,
                             fig_param = fig_param)

 
if __name__ == "__main__":
    do_movie(ID)
