import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from Common.tdc_filenames  import *

from Common   import tdc_Data_Sequence, tdc_Data_Sequence_Initializer, tdc_Moving_Grid_Plotter
from Fields   import tdc_Field_Data, tdc_Fields_Plotter

from Plot_CMD.Movie import *


def tdc_plot_field_movie__cmd(calc_ids, field_name, ylim,
                              moving_grid_dict=None,
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
    fs  = tdc_Data_Sequence_Initializer( tdc_Field_Data,
                                         calc_ids=calc_ids,
                                         field_name=field_name,
                                         **kwargs)
    fp  = tdc_Fields_Plotter(fs)
    # plot moving grid if asked
    if moving_grid_dict:
        fp  = tdc_Moving_Grid_Plotter(fp,moving_grid_dict)
    # movie frames
    MF = Single_Panel_Movie_Frames(fp, ylim=ylim, **kwargs)    
    # movie file maker
    MFM = Movie_File_Maker__CMD(field_name + '_' + calc_ids[0])
    # write frames ----------
    MFM.open_index_file()
    for i in range(MF.i_frame_min, MF.i_frame_max):
        MF.animation_update(i)
        print 'Saving frame %4d (out of %d)' % (i,MF.i_frame_max)  
        MFM.store_snapshot(i,MF.figure)
    MFM.close_index_file()
    # create movie file
    MFM.combine_frames_into_movie()
    MFM.delete_frame_files()

        
