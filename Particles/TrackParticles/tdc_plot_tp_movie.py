from Common    import tdc_Data_Sequence, tdc_Moving_Grid_Plotter

from Particles.TrackParticles.tdc_tp_data       import tdc_TP_Data
from Particles.TrackParticles.tdc_tp_plotter    import tdc_TP_Plotter

def tdc_plot_tp_movie(plot_module,
                      tp,
                      ylim,
                      xlim=None,
                      fps=None,
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
        pp  = tdc_Moving_Grid_Plotter(pp,moving_grid_dict)
    # movie frames
    MF = Single_Panel_Movie_Frames(pp, ylim=ylim, xlim=xlim, **kwargs)
    # movie_id - directory with the movie file
    movie_id = 'TP' + '_' + tp.calc_id
    # -----------------------------------------
    # make movie
    plot_module.Movie.plot_movie( MF, movie_id, fps)
