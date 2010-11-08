from Common    import *
import Common
from Common    import tdc_Data_Sequence

from tdc_tp_data       import tdc_TP_Data
from tdc_tp_plotter    import tdc_TP_Plotter

from Movie.single_panel_movie_frames import Single_Panel_Movie_Frames
from Movie.movie_maker               import Movie_Maker
from Movie.movie_file_maker          import Movie_File_Maker
from Movie.moving_grid_plotter       import Moving_Grid_Plotter


def tdc_plot_tp_movie(tp,
                      ylim,
                      trail_dict=None,
                      moving_grid_dict=None,
                      **kwargs):
    """
    tp
       TP_Data class instance(s)
    ylim
       Y axis limits   
    Options:
    --------
    tt
       time interval <[t1,<t2>]>
    xlim
       <None> X axis limits
    trail_dict
       dictionary with trail plot properties
       dict( length=3, style='color', marker='symbols', markersize=10 )
    moving_grid_dict
       if specified plot moving grid
       moving_grid_dict = dict(n_lines=20, speed=1)
    """
    # particles sequence
    tps = tdc_Data_Sequence( tp, **kwargs) 
    pp  = tdc_TP_Plotter(tp=tps,trail_dict=trail_dict)
    # plot moving grid if asked
    if moving_grid_dict:
        pp  = Moving_Grid_Plotter(pp,moving_grid_dict)
    # movie frames
    MF = Single_Panel_Movie_Frames(pp, ylim=ylim, **kwargs)
    # movie file maker
    MFM = Movie_File_Maker('TP' + '_' + tp.calc_id)
    # movie maker
    MM = Movie_Maker(MF, MFM)
    # play movie
    MM.animate()
