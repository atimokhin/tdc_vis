#!/usr/bin/python

# import ATbase module
import sys
sys.path.append('/home/atim/WORK/C++/ATbase2/lib_python/')
sys.path.append('/home/atim/WORK/PULSARS/TDC/tdc_vis/')
import ATbase as AT

from Common  import *
from Plots   import *

# ============================================================
# Interface
# ============================================================
## import Plot_GUI as plot_module
import Plot_CMD as plot_module

# ============================================================
# Directory
# ============================================================
tdc_set_results_dir('../RESULTS/')
## tdc_set_results_dir('../RESULTS/FreeAgent/')


# ============================================================
# ID 
# ============================================================
ID=['test_osc_2e']
# ============================================================



def do_movie(ID):
    ## moving_grid_dict = dict(n_lines=30, speed=1)
    moving_grid_dict = None
    
    ## plot_test_E_acc(ID,
    ##                 ylim=[[-150,5],[-1e-3,1e-3]],
    ##                 use_cell_coordinates=False,
    ##                 show_cells=False,
    ##                 time_normalization = 'absolute')

    ## plot_test_E_acc_cmd(ID,
    ##                     ylim=[[-150,5],[-1e-3,1e-3]],
    ##                     use_cell_coordinates=False,
    ##                     show_cells=False,
    ##                     time_normalization = 'absolute')

    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # Rho
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    tdc_plot_field_movie(plot_module,
                         ID,
                         'Rho',
                         ylim=[-150,5],
                         tt = [0,.4],
                         fps=15,
                         moving_grid_dict=moving_grid_dict,
                         use_cell_coordinates = True,
                         time_normalization = 'absolute')
    # ~~~~~~~~~~~~~~~~~~~~~~~~

    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## # J
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## tdc_plot_field_movie(ID,
    ##                      'J',
    ##                      ylim=[-0.005,0.005],
    ##                      moving_grid_dict=moving_grid_dict,
    ##                      time_normalization = 'absolute')
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    
    ## ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## ## # Phi
    ## ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## ## tdc_plot_field_movie(ID,'Phi',ylim=[-.5,.1],moving_grid_dict=moving_grid_dict)
    ## ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## # E_acc
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## tdc_plot_field_movie(ID,
    ##                      'E_acc',
    ##                      ylim=[-3e-4,3e-4],
    ##                      moving_grid_dict=moving_grid_dict,
    ##                      time_normalization = 'absolute')
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## # XP Movie
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## tp = None
    ## tt = None    
    ## tt = [0,.4]

    ## sample_dict    = dict(name='regular',n_reduce=1,n_min=1000)
    ## particle_names = ['Electrons']

    ## tdc_plot_xp_movie(plot_module,
    ##                   ID, particle_names, sample_dict,
    ##                   tp=tp, trail_dict=dict(length=18,marker='numbers'),
    ##                   tt=tt,
    ##                   ylim=[-2e-4,2e-4],
    ##                   moving_grid_dict=moving_grid_dict,
    ##                   time_normalization = 'absolute')
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~



## def plot_test_E_acc(calc_ids,
##                     ylim,
##                     xlim=[None,None],
##                     fps=None,
##                     use_cell_coordinates=False,
##                     show_cells=False,
##                     **kwargs):
##     """
##     calc_ids
##        calculation id names
##     field_name
##        name of the field to be plotted
##     ylim
##        Y axis limits   
##     Options:
##     --------
##     tt
##        time interval <[t1,<t2>]>
##     xlim
##        <None> X axis limits
##     moving_grid_dict
##        if specified plot moving grid
##        moving_grid_dict = dict(n_lines=20, speed=1)
##     """

##     # make sure calc_id is a sequence ----------------
##     if not isinstance( calc_ids, (list,tuple) ):
##         calc_ids = (calc_ids,)        
##     # field sequences ---------------------------------
##     fs1  = tdc_Data_Sequence_Initializer( tdc_Field_Data,
##                                           calc_ids=calc_ids,
##                                           field_name='Rho',
##                                           **kwargs)
##     # field sequences ---------------------------------
##     fs2  = tdc_Data_Sequence_Initializer( tdc_Field_Data,
##                                           calc_ids=calc_ids,
##                                           field_name='E_acc',
##                                           **kwargs)
##     # field plotter
##     fp1 = tdc_Fields_Plotter(fs1)
##     fp2 = tdc_Fields_Plotter(fs2)
##     if use_cell_coordinates:
##         fp1.use_cell_coordinates()
##         fp2.use_cell_coordinates()
##     if show_cells:
##         fp1.show_cells_on()
##         fp2.show_cells_on()
##     # movie frames
##     MF = Double_Panel_Movie_Frames( (fp1,fp2), ylim=ylim, xlim=xlim, **kwargs)
##     # movie file maker
##     MFM = Movie_File_Maker__GUI('E_acc_Rho' + '_' + calc_ids[0], fps)
##     # movie maker
##     MM = Movie_Maker(MF, MFM)
##     # play movie
##     MM.animate()


## def plot_test_E_acc_cmd(calc_ids,
##                         ylim,
##                         xlim=[None,None],
##                         fps=None,
##                         use_cell_coordinates=False,
##                         show_cells=False,
##                         **kwargs):
##     """
##     calc_ids
##        calculation id names
##     field_name
##        name of the field to be plotted
##     ylim
##        Y axis limits   
##     Options:
##     --------
##     tt
##        time interval <[t1,<t2>]>
##     xlim
##        <None> X axis limits
##     moving_grid_dict
##        if specified plot moving grid
##        moving_grid_dict = dict(n_lines=20, speed=1)
##     """

##     # make sure calc_id is a sequence ----------------
##     if not isinstance( calc_ids, (list,tuple) ):
##         calc_ids = (calc_ids,)        
##     # field sequences ---------------------------------
##     fs1  = tdc_Data_Sequence_Initializer( tdc_Field_Data,
##                                           calc_ids=calc_ids,
##                                           field_name='Rho',
##                                           **kwargs)
##     # field sequences ---------------------------------
##     fs2  = tdc_Data_Sequence_Initializer( tdc_Field_Data,
##                                           calc_ids=calc_ids,
##                                           field_name='E_acc',
##                                           **kwargs)
##     # field plotter
##     fp1 = tdc_Fields_Plotter(fs1)
##     fp2 = tdc_Fields_Plotter(fs2)
##     if use_cell_coordinates:
##         fp1.use_cell_coordinates()
##         fp2.use_cell_coordinates()
##     if show_cells:
##         fp1.show_cells_on()
##         fp2.show_cells_on()
##     # movie frames
##     MF = Double_Panel_Movie_Frames( (fp1,fp2), ylim=ylim, xlim=xlim, **kwargs)
##     # movie_id - directory with the movie file
##     movie_id = 'E_acc_Rho' + '_' + calc_ids[0]
##     # -----------------------------------------
##     # make movie
##     plot_movie__cmd( MF, movie_id, fps)


if __name__ == "__main__":
    do_movie(ID)
