from Common.tdc_filenames  import *

from Common   import tdc_Data_Sequence, tdc_Data_Sequence_Initializer, tdc_Moving_Grid_Plotter
from Fields   import tdc_Field_Data, tdc_Fields_Plotter

from Plot_CMD.Movie import *


def tdc_plot_field_movie__cmd(calc_ids, field_name, ylim,
                              moving_grid_dict=None,
                              fps=None,
                              **kwargs):
    """
    calc_ids
       calculation id names
    field_name
       name of the field to be plotted
    ylim
       Y axis limits   
    Options:
    --------
    tt
       time interval <[t1,<t2>]>
    xlim
       <None> X axis limits
    moving_grid_dict
       if specified plot moving grid
       moving_grid_dict = dict(n_lines=20, speed=1)
    fps
       fps for movie file
    """
    # make sure calc_id is a sequence
    if not isinstance( calc_ids, (list,tuple) ):
        calc_ids = (calc_ids,)
    # -----------------------------------------
    # field specific part
    # -----------------------------------------
    # field sequence 
    fs  = tdc_Data_Sequence_Initializer( tdc_Field_Data,
                                         calc_ids=calc_ids,
                                         field_name=field_name,
                                         **kwargs)
    plotter  = tdc_Fields_Plotter(fs)
    # plot moving grid if asked
    if moving_grid_dict:
        plotter  = tdc_Moving_Grid_Plotter(plotter,moving_grid_dict)
    # movie_id - directory with the movie file
    movie_id = field_name + '_' + calc_ids[0]
    # -----------------------------------------
    # make movie
    plot_movie__cmd( plotter, movie_id, ylim, fps, **kwargs)




        
