#!/usr/bin/python
import os

from ATvis.Common_Data_Plot import *

from Auxiliary           import *
from Common_Data_Plot    import *
from x_PlottingFunctions import *
from Movie               import Movie_Interface_Selector


# ============================================================
# Figure Style Parameters
# ============================================================
fig_param    = paramSingleFig_Work
fig_param_xp = paramSingleFig_FMCI_XP_Presentation

# ============================================================
# Directory
# ============================================================
tdc_Filenames.set_vis_results_dir('../RESULTS_VIS/__RS_2/')


# ============================================================
# FMCI_IDs 
# ============================================================
# FMCI_ID='FMCI__RS__RD_jp0.5_P0.09_L0.6_nGJ5e4_nx5e3_dt4e-5_sU'
# FMCI_ID='FMCI__RS__RD_jp0.25_P0.09_L0.6_nGJ5e4_nx5e3_dt4e-5_sU'
FMCI_ID='FMCI__RS__RD_jp0.95_P0.09_L0.6_nGJ5e4_nx5e3_dt4e-5_sU'

# ============================================================
# plot limits:
# ============================================================
xlim     = [-0.01,.61]
ylim_mp  = [-5e8,5e8]

m_max=200
w_max=10

wlims=[5e-2,5e1]

axes_commands_mp = ['set_yticks([-1e8,-1e4,0,1e4,1e8])']
# ============================================================

ii=None
## ii=[400,405]

fps = 5

keep_frame_files=False
# ==================


# ============================================================
# Plots 
# ============================================================
Plots = {'MP' : True,
         'XP' : True }
# ============================================================



def do_movie():
    # select interface
    interface = Movie_Interface_Selector()
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # MP Movie
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    if Plots['MP']:
        particle_names = ['Electrons', 'Positrons', 'Pairs']

        tdc_plot_fmci_mp_movie(interface.movie_module,
                               FMCI_ID,
                               particle_names,
                               ylim=ylim_mp,
                               xlim=xlim,
                               m_max=m_max,
                               w_max=w_max,
                               ii=ii,
                               fps=fps,
                               keep_frame_files=keep_frame_files,
                               symlog=True,
                               linthreshy=5,
                               axes_commands=axes_commands_mp,
                               fig_param=fig_param)
    # ~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # XP Movie
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    if Plots['XP']:
        particle_name = 'Positrons'

        tdc_plot_fmci_xp_movie(interface.movie_module,
                               FMCI_ID,
                               particle_name,
                               ylim=ylim_mp,
                               xlim=xlim,
                               wlims=wlims,
                               ii=ii,
                               fps=fps,
                               keep_frame_files=keep_frame_files,
                               symlog=True,
                               linthreshy=5,
                               axes_commands=axes_commands_mp,
                               fig_param=fig_param_xp)
    # ~~~~~~~~~~~~~~~~~~~~~~~~


 


if __name__ == "__main__":
    do_movie()
