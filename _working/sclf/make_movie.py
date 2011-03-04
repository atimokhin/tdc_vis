#!/usr/bin/python

from Common import *
from Plots  import *

from x_Tests.plot_test_e_e_gauss_movie import *

# ============================================================
# Interface
# ============================================================
import Plot_GUI as plot_module
## import Plot_CMD as plot_module

# ============================================================
# Directory
# ============================================================
## tdc_set_results_dir('../RESULTS/')
tdc_set_results_dir('../RESULTS/FreeAgent/')


# ============================================================
# IDs 
# ============================================================
IDs=['SCLF__jm0.5_Pcf1e5_L1_nGJ1e5_nx5e3_dt4e-5__RhoGJConst__noMC__dP_inj6',
     'SCLF__jm0.5_Pcf1e5_L1_nGJ1e5_nx5e3_dt4e-5__RhoGJConst__noMC__dP_inj8',
     'SCLF__jm0.5_Pcf1e5_L1_nGJ1e5_nx5e3_dt4e-5__RhoGJConst__noMC__dP_inj12',
     'SCLF__jm0.25_Pcf1e5_L1_nGJ1e5_nx5e3_dt4e-5__RhoGJConst__noMC__dP_inj6',
     'SCLF__jm0.25_Pcf1e5_L1_nGJ1e5_nx5e3_dt4e-5__RhoGJConst__noMC__dP_inj8']
# ============================================================



def do_movie(IDs):
    # iterate over IDs <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    for ID in IDs:
        ## moving_grid_dict = dict(n_lines=30, speed=1)
        moving_grid_dict = None
        tt=None
        xlim=[-0.005,1.005]

        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## # Rho
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## tdc_plot_field_movie(plot_module,
        ##                      ID,
        ##                      'Rho',
        ##                      ylim=[-3,3],
        ##                      xlim=xlim,
        ##                      moving_grid_dict=moving_grid_dict,
        ##                      tt=tt,
        ##                      ghost_points=True)
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## # J
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## tdc_plot_field_movie(plot_module,
        ##                      ID,
        ##                      'J',
        ##                      ylim=[-3,3],
        ##                      xlim=xlim,
        ##                      moving_grid_dict=moving_grid_dict,
        ##                      tt=tt,
        ##                      ghost_points=True)
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~

        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## # Phi
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## tdc_plot_field_movie(ID,'Phi',ylim=[-.5,.1],moving_grid_dict=moving_grid_dict)
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~

        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## # E_acc__E_Gauss:
        ## #  plot Electric field and difference between Gauss' and Ampere's Electric fields
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## plot_test_e_e_gauss_movie(plot_module,
        ##                           ID,
        ##                           ylim=[[-1e-2,1e-2],[-1e-2,1e-2]],
        ##                           xlim=[xlim,xlim],
        ##                           tt=tt,
        ##                           fps=15,
        ##                           use_cell_coordinates=False,
        ##                           show_cells=False,
        ##                           time_normalization = 'absolute',
        ##                           ghost_points=True)
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~

        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## # E_acc
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## tdc_plot_field_movie(plot_module,
        ##                      ID,
        ##                      'E_acc',
        ##                      ylim=[-1,1],
        ##                      xlim=xlim,
        ##                      moving_grid_dict=moving_grid_dict,
        ##                      tt=tt,
        ##                      ghost_points=True)
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~

        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## # E_Gauss
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## tdc_plot_field_movie(plot_module,
        ##                      ID,
        ##                      'E_Gauss',
        ##                      ylim=[-1,1],
        ##                      xlim=xlim,
        ##                      moving_grid_dict=moving_grid_dict,
        ##                      tt=tt,
        ##                      ghost_points=True)
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~

        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## # Particle Number Density
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~
        ## tdc_plot_ep_density_movie(ID, ylim=[0,60],
        ##                           e_density_negative=False,
        ##                           moving_grid_dict=moving_grid_dict)
        ## # ~~~~~~~~~~~~~~~~~~~~~~~~

        # ~~~~~~~~~~~~~~~~~~~~~~~~
        # XP Movie
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        tp = None
        ## tp = tdc_TP_Data()
        ## tp.setup_from_file(ID,'p500_ts525')
        ## tp.delete(range(0,47,2))

        sample_dict    = dict(name='regular',n_reduce=1,n_min=1000)
        particle_names = ['Electrons','Protons','Positrons','Pairs']
        ## particle_names = ['Electrons']

        tdc_plot_xp_movie(plot_module,
                          ID,
                          particle_names,
                          ylim=[-6,6],
                          xlim=xlim,
                          sample_dict=sample_dict,
                          tt=tt,
                          tp=tp,
                          trail_dict=dict(length=18,marker='numbers'),
                          moving_grid_dict=moving_grid_dict)
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
