from Common.tdc_filenames  import *

from Common   import tdc_Data_Sequence_Initializer
from Fields   import tdc_Field_Data, tdc_EP_Density_Plotter

from Plot_GUI.Movie import *


def tdc_plot_ep_density_movie(calc_ids, ylim,
                              e_density_negative=True,
                              moving_grid_dict=None,
                              **kwargs):
    """
    calc_ids
       calculation id names
    ylim
       Y axis limits   
    Options:
    --------
    t
       time interval <[t1,<t2>]>
    xlim
       <None> X axis limits
    moving_grid_dict
       if specified plot moving grid
       moving_grid_dict = dict(n_lines=20, speed=1)
    """

    # make sure calc_id is a sequence
    if not isinstance( calc_ids, (list,tuple) ):
        calc_ids = (calc_ids,)
        
    # field sequence
    fe  = tdc_Data_Sequence_Initializer( tdc_Field_Data, calc_ids=calc_ids,
                                         field_name='N', filename='prop_Electrons.h5', **kwargs)
    fp  = tdc_Data_Sequence_Initializer( tdc_Field_Data, calc_ids=calc_ids,
                                         field_name='N', filename='prop_Positrons.h5', **kwargs)
    f_plotter  = tdc_EP_Density_Plotter(fe,fp,e_density_negative)
    # plot moving grid if asked
    if moving_grid_dict:
        f_plotter  = tdc_Moving_Grid_Plotter(f_plotter,moving_grid_dict)
    # movie frames
    MF = Single_Panel_Movie_Frames(f_plotter, ylim=ylim, **kwargs)
    # movie file maker
    MFM = Movie_File_Maker('EP' + '_' + calc_ids[0])
    # movie maker
    MM = Movie_Maker(MF, MFM)
    # play movie
    MM.animate()
