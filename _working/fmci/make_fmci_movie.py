#!/usr/bin/python
if __name__ == '__main__':
    import tdc_vis

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
# ------------------------------------------------------------ 
# TDC data will be read from this directory
# ------------------------------------------------------------
tdc_Filenames.set_results_dir('../RESULTS_FMCI/Crab')

# tdc_Filenames.set_vis_results_dir('../RESULTS_FMCI/__RS_2/')
tdc_Filenames.set_vis_results_dir('../RESULTS_FMCI_VIS/Crab/')


# ============================================================
# FMCI_IDs 
# ============================================================
# FMCI_ID='FMCI__RS__Crab_B1_R7_jp1_P0.033_L0.2_nGJ5e4_nx5e3_dt1e-5_sU'
# FMCI_ID='FMCI__RS__Crab_B3_R7_jp1_P0.033_L0.1_nGJ5e4_nx5e3_dt5e-6_sU'
# FMCI_ID='FMCI__RS__Crab_B3_Dipole_jp1_P0.033_L0.2_nGJ5e4_nx5e3_dt1.5e-5_sU'

# FMCI_ID='FMCI__RS__Crab_B3_Dipole_jp1_P0.033_L0.2_nGJ5e4_nx1e4_dt8e-6_sU'
# FMCI_ID='FMCI__RS__Crab_B1_Dipole_jp1_P0.033_L0.2_nGJ5e4_nx5e3_dt1.5e-5_sU__test_debug_3_MC'

# FMCI_ID='FMCI__RS__Crab_B3_Dipole_jp1_P0.033_L0.2_nGJ5e4_nx1e4_dt8e-6_sU_a'
# FMCI_ID='HiResFMCI__RS__Crab_B3_Dipole_theta0.5_jp1_P0.033_L0.2_nGJ5e4_nx1e4_dt8e-6_sU_a'

# FMCI_ID='FMCI__RS__Crab_B1_Dipole_jp1_P0.033_L0.2_nGJ5e4_nx1e4_dt8e-6_sU_a'
# FMCI_ID='FMCI__RS__Crab_B1_Dipole_theta0.5_jp1_P0.033_L0.2_nGJ5e4_nx1e4_dt8e-6_sU_a'
FMCI_ID='FMCI__SCLF__Crab_B1_Dipole_jm1.5_P0.033_Chi60_L0.3_nGJ5e4_nx1e4_dt1e-5_sU'

# ============================================================
# plot limits:
# ============================================================
xlim     = [-0.01,.21]
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
particle_names_XP = ['Positrons', 'Electrons']

Plots = {'MP' : False,
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
        for particle_name in particle_names_XP:

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
