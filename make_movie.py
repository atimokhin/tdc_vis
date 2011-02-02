#!/usr/bin/python

from Common import *

# ============================================================
# Interface
# ============================================================
from Plot_GUI import *
## from Plot_CMD import *

# ============================================================
# Directory
# ============================================================
tdc_set_results_dir('../RESULTS/')
## tdc_set_results_dir('../RESULTS/FreeAgent/')



# ============================================================
# IDs 
# ============================================================
IDs=['test_osc_2e']
# ============================================================



def do_movie(IDs):
    # iterate over IDs <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    for ID in IDs:
        ## moving_grid_dict = dict(n_lines=30, speed=1)
        moving_grid_dict = None

        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## # Rho
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## tdc_plot_field_movie(ID,'Rho',ylim=[-1.5,1.5],moving_grid_dict=moving_grid_dict,tt=[1,2])
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~

        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## # Phi
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## tdc_plot_field_movie(ID,'Phi',ylim=[-.5,.1],moving_grid_dict=moving_grid_dict)
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~

        # ~~~~~~~~~~~~~~~~~~~~~~~~
        # E_acc
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        tdc_plot_field_movie(ID,'E_acc',ylim=[-3e-4,3e-4],moving_grid_dict=moving_grid_dict)
        # ~~~~~~~~~~~~~~~~~~~~~~~~

        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## # Particle Number Density
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## tdc_plot_ep_density_movie(ID, ylim=[0,60],
        ##                           e_density_negative=False,
        ##                           moving_grid_dict=moving_grid_dict)
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~

        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## # XP Movie
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## tp = None
        ## tt = None    
        ## ## tp = tdc_TP_Data()
        ## ## tp.setup_from_file(ID,'p500_ts525')
        ## ## tp.delete(range(0,47,2))

        ## sample_dict    = dict(name='regular',n_reduce=1,n_min=1000)
        ## particle_names = ['Electrons','Positrons','Pairs','Protons']
        ## ## particle_names = ['Electrons']

        ## tdc_plot_xp_movie(ID, particle_names, sample_dict,
        ##                   tp=tp, trail_dict=dict(length=18,marker='numbers'),
        ##                   tt=tt,
        ##                   ylim=[-1.6e7,1.6e7],
        ##                   moving_grid_dict=moving_grid_dict)
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~


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
