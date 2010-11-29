import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from Common.tdc_filenames  import *

from Common   import tdc_Data_Sequence, tdc_Data_Sequence_Initializer
from Fields   import tdc_Field_Data, tdc_Fields_Plotter

from Plot_CMD.Movie import *


def tdc_plot_field_movie_cmd(calc_ids, field_name, ylim,
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

    files=[]
    for i in range(10):  # 50 frames
        MF.animation_update(i)
        fname = '__mpl_test/_tmp%03d.png' % i
        print 'Saving frame', fname
        MF.figure.savefig(fname)
        files.append(fname)

        
