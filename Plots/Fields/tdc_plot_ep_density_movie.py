from Common.tdc_filenames  import *

from Common   import tdc_Data_Sequence_Initializer, tdc_Moving_Grid_Plotter
from Fields   import tdc_Field_Data, tdc_EP_Density_Plotter

def tdc_plot_ep_density_movie(plot_module,
                              calc_ids,
                              ylim,
                              xlim=None,
                              fps=None,
                              keep_frame_files=None,
                              tt=None,
                              e_density_negative=True,
                              moving_grid_dict=None,
                              use_cell_coordinates=False,
                              show_cells=False,
                              time_normalization=None,
                              **kwargs):
    """
    calc_ids
       calculation id names
    ylim
       Y axis limits   
    Options:
    --------
    xlim
       <None> X axis limits
    tt
       <None> time interval <[t1,<t2>]>
    moving_grid_dict
       <None>  if specified plot moving grid
               moving_grid_dict = dict(n_lines=20, speed=1)
    e_density_negative,
       <True> plot electron density as negative (True) or positive (False) values
    use_cell_coordinates
       <False>
    show_cells
       <False>
    time_normalization
       <None>
    **kwargs
       go to tdc_*_Data via tdc_Data_Sequence_Initializer
    """

    # make sure calc_id is a sequence
    if not isinstance( calc_ids, (list,tuple) ):
        calc_ids = (calc_ids,)
        
    # field sequence
    fe  = tdc_Data_Sequence_Initializer( tdc_Field_Data,
                                         calc_ids=calc_ids,
                                         field_name='N',
                                         filename='prop_Electrons.h5',
                                         tt=tt,
                                         time_normalization=time_normalization,
                                         **kwargs)
    fp  = tdc_Data_Sequence_Initializer( tdc_Field_Data,
                                         calc_ids=calc_ids,
                                         field_name='N',
                                         filename='prop_Positrons.h5',
                                         tt=tt,
                                         time_normalization=time_normalization,
                                         **kwargs)
    plotter  = tdc_EP_Density_Plotter(fe,fp,e_density_negative)
    # plot moving grid if asked
    if moving_grid_dict:
        plotter  = tdc_Moving_Grid_Plotter(plotter,moving_grid_dict)
    # movie frames
    MF = plot_module.Movie.Single_Panel_Movie_Frames(plotter, ylim=ylim, xlim=xlim)
    # movie_id - directory with the movie file
    movie_id = 'EP' + '_' + calc_ids[0]
    # -----------------------------------------
    # make movie
    plot_module.Movie.plot_movie( MF, movie_id, fps, keep_frame_files)
