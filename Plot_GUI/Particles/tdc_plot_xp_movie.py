from Common    import tdc_Data_Sequence, tdc_Data_Sequence_Initializer

from Particles.tdc_xp_data           import tdc_XP_Data
from Particles.tdc_xps_tp_plotter    import tdc_XPs_TP_Plotter

from Plot_GUI.Movie import *


def tdc_plot_xp_movie(calc_ids,
                      particle_names,
                      sample_dict,
                      ylim,
                      tp=None,trail_dict=None,
                      moving_grid_dict=None,
                      **kwargs):
    """
    calc_ids
       calculation id names
    particle_name
       particle names
    sample_dic
       dictionary with sample parameters
       sample_dict = dict(name='regular',n_reduce=10,n_min=1000)
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
    """
    # make sure calc_id is a sequence
    if not isinstance( calc_ids, (list,tuple) ):
        calc_ids = (calc_ids,)

    # make sure particle_names is a sequence
    if not isinstance( particle_names, (list,tuple) ):
        particle_names = (particle_names,)
        
    # particles sequence
    xps=[]
    for pname in particle_names:
        xps.append(  tdc_Data_Sequence_Initializer( tdc_XP_Data,
                                                    calc_ids=calc_ids,
                                                    particle_name=pname,
                                                    sample_dict=sample_dict,
                                                    **kwargs) )
    # tracked particles sequence
    tps = tdc_Data_Sequence( tp, **kwargs) if tp else None
    # plotter
    pp  = tdc_XPs_TP_Plotter(xps=xps, tp=tps,trail_dict=trail_dict)
    # plot moving grid if asked
    if moving_grid_dict:
        pp  = tdc_Moving_Grid_Plotter(pp,moving_grid_dict)
    # movie frames
    MF = Single_Panel_Movie_Frames(pp, ylim=ylim, **kwargs)
    # movie file maker
    MFM = Movie_File_Maker__GUI('XP' + '_' + calc_ids[0])
    # movie maker
    MM = Movie_Maker(MF, MFM)
    # play movie
    MM.animate()
