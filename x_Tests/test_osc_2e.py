#!/usr/bin/python

from Common  import *
from Plots   import *

from plot_test_e_e_gauss_movie import *

# ============================================================
# Interface
# ============================================================
import Plot_GUI as plot_module
## import Plot_CMD as plot_module

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
    tt = [0,0.5]   
    ## tt = [0,4]
    xlim =  None
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # plot Electric field and difference between Gauss' and Ampere's Electric fields
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    plot_test_e_e_gauss_movie(plot_module,
                              ID,
                              ylim=[[-3e-4,3e-4],[-1e-16,1e-16]],
                              tt=tt,
                              use_cell_coordinates=False,
                              show_cells=False,
                              time_normalization = 'absolute',
                              ghost_points=True)
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    

    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## # Rho
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## tdc_plot_field_movie(plot_module,
    ##                      ID,
    ##                      'Rho',
    ##                      ylim=[-150,5],
    ##                      tt=tt,
    ##                      fps=15,
    ##                      moving_grid_dict=moving_grid_dict,
    ##                      use_cell_coordinates=True,
    ##                      ghost_points=True,
    ##                      time_normalization='absolute')
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~

    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## # J
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## tdc_plot_field_movie(ID,
    ##                      'J',
    ##                      ylim=[-0.005,0.005],
    ##                      moving_grid_dict=moving_grid_dict,
    ##                      time_normalization = 'absolute')
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # Phi
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    tdc_plot_field_movie(plot_module,
                         ID,
                         'Phi',
                         ylim=[-2e-9,2e-9],
                         tt=tt,
                         moving_grid_dict=moving_grid_dict,
                         ghost_points=True,
                         time_normalization = 'absolute')
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## # E_acc
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    ## tdc_plot_field_movie(plot_module,
    ##                      ID,
    ##                      'E_acc',
    ##                      ylim=[-3e-4,3e-4],
    ##                      tt=tt,
    ##                      moving_grid_dict=moving_grid_dict,
    ##                      ghost_points=True,
    ##                      time_normalization = 'absolute')
    ## # ~~~~~~~~~~~~~~~~~~~~~~~~
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # XP Movie
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    tp = None
    trail_dict=dict(length=18,marker='numbers')
    trail_dict = None
    
    sample_dict    = dict(name='regular',n_reduce=1,n_min=1000)
    particle_names = ['Electrons']

    tdc_plot_xp_movie(plot_module,
                      ID,
                      particle_names,
                      ## sample_dict,
                      tp=tp,
                      trail_dict=trail_dict,
                      tt=tt,
                      ylim=[-2e-4,2e-4],
                      xlim=xlim,
                      moving_grid_dict=moving_grid_dict,
                      use_cell_coordinates=True,
                      time_normalization = 'absolute')
    # ~~~~~~~~~~~~~~~~~~~~~~~~



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
