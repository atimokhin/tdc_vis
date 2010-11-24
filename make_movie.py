#!/usr/bin/python

import matplotlib
matplotlib.use('GTKAgg')

import pickle

from Common    import *
from Fields    import *
from Particles import *


## tdc_set_results_dir('../RESULTS/')
tdc_set_results_dir('../RESULTS/FreeAgent/')

## ID='test_osc_2e'

ID='SCLF_jp1.0_P0.2_L0.5_nGJ1e4_nx1e3_dt1e-4__RhoLin2_A-1_X0.5_noLPT'
ID='SCLF_jp1.0_P0.2_L0.5_nGJ1e4_nx1e3_dt1e-4__RhoLin2_A1_X0.5'


## ID='SCLF_2_jm0.5_L100_nGJ2e4_nx1e3_dt2.5e-2__tst'
## ID='SCLF_2_jm1_L1_nGJ2e4_nx1e3_dt2.5e-4__tst'
## ID='SCLF_2_jm0.5_L10_nGJ2e4_nx1e3_dt2.5e-3__tst'

## ID='SCLF_2_jm1_L1_nGJ1e4_nx1e3_dt2.5e-4_m1'
## ID='SCLF_1_jp1_L1_nGJ1e4_nx1e3_dt2.5e-4_m1'

## ID=['RS_1_R6_jp1.0_P0.2_L0.3_nGJ2.5e4_nx2.5e3_dt4e-5_s1',
##     'RS_1_R6_jp1.0_P0.2_L0.3_nGJ2.5e4_nx2.5e3_dt4e-5_s1__1']

## ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ1.25e4_nx2.5e3_dt4e-5_s1'
## ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ2.5e4_nx2.5e3_dt4e-5_sU'

## ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU'
## ID='RS_1_R6_jp0.5_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU'
## ID='RS_1_R6_jp1.5_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU'

## ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU__3d_cycle'
#ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU__3d_cycle_no_smoothing'
#ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU__3d_cycle__on_the_spot'

## ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU__tst'
## ID='SCLF_1_jp1_P0.2_L0.5_nGJ1e4_nx1.5e3_dt2.5e-5_m1'
## ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ1.25e4_nx2.5e3_dt4e-5_s1'

## ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU__wave_break__no_pairs__start_590'
## ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU__pairs_reduced_0.25__start_590'
## ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU__pairs_reduced_0.25__start_592'

##ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU__wave_break__no_pairs__start_591'
##ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU__wave_break__no_pairs__start_594'
## ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU__wave_break__no_pairs__start_598'
## ID='RS_1_R6_jp1.0_P0.2_L0.3_nGJ5e4_nx5e3_dt2e-5_sU__wave_decay__no_pairs__start_601'



def do_movie():

    moving_grid_dict = dict(n_lines=30, speed=1)
    moving_grid_dict = None

    ## tdc_plot_field_movie(ID,'Rho',ylim=[-5,5],moving_grid_dict=moving_grid_dict)

    ## tdc_plot_field_movie(ID,'Phi',ylim=[-.5,.1],moving_grid_dict=moving_grid_dict)

    tdc_plot_field_movie(ID,'E_acc',ylim=[-1,1],moving_grid_dict=moving_grid_dict)

    ## tdc_plot_ep_density_movie(ID, ylim=[0,60],
    ##                           e_density_negative=False,
    ##                           moving_grid_dict=moving_grid_dict)



    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## # XP Movie
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## tp = None
    ## tt = None    
    ## ## tp = tdc_TP_Data()
    ## ## tp.setup_from_file(ID,'p500_ts525')

    ## ## tp.delete(range(0,47,2))

    ## sample_dict    = dict(name='regular',n_reduce=1,n_min=1000)
    ## particle_names = ['Electrons','Positrons','Pairs']
    ## ## particle_names = ['Electrons','Positrons']
        
    ## tdc_plot_xp_movie(ID, particle_names, sample_dict,
    ##                   tp=tp, trail_dict=dict(length=18,marker='numbers'),
    ##                   tt=tt,
    ##                   ylim=[-1.6e7,1.6e7],
    ##                   moving_grid_dict=moving_grid_dict)

    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # particles trajectories
    # ~~~~~~~~~~~~~~~~~~~~~~~~
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

if __name__ == "__main__":
    do_movie()
