#!/usr/bin/python
import os

from Auxiliary        import *
from Common_Data_Plot import *
from x_Plots          import *


# ============================================================
# Figure Style Parameters
# ============================================================
fig_param = paramSingleFig_Presentation

# ============================================================
# Directory
# ============================================================
## tdc_Filenames.set_results_dir('../RESULTS/FreeAgent/')


# ============================================================
# FMCI_IDs 
# ============================================================
FMCI_ID='FMCI__SCLF__jp1.5_Pcf1e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJConst__R6C_Xb0.7__dP5e-2_inj7_sU'



# ============================================================
# plot limits:
# ============================================================
xlim     = [-0.01,1.01]
ylim_mp  = [-5e8,5e8]

m_max=80
w_max=100

wlims=[1e-2,1e2]

axes_commands_mp = ['set_yticks([-1e8,-1e4,0,1e4,1e8])']
# ============================================================

ii=None
## ii=[400,420]

fps = 14

keep_frame_files=False
# ==================


# ============================================================
# Plots 
# ============================================================
Plots = {'MP' : False,
         'XP' : True }
# ============================================================



def do_movie():
    # ==========================================
    # Interface
    # ==========================================
    interface = os.environ.get('MPL_INTERFACE','GUI')
    if interface=='GUI':
        import Plot_GUI as plot_module
    else:
        import Plot_CMD as plot_module
    # ==========================================
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # MP Movie
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    if Plots['MP']:
        particle_names = ['Electrons', 'Positrons', 'Pairs']

        tdc_plot_fmci_mp_movie(plot_module,
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
        particle_name = 'Electrons'

        tdc_plot_fmci_xp_movie(plot_module,
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
                               fig_param=fig_param)
    # ~~~~~~~~~~~~~~~~~~~~~~~~


 


if __name__ == "__main__":
    do_movie()
