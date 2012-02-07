from Particles import tdc_XP_Data

from Auxiliary_Plotters import tdc_Moving_Grid_Plotter
from Common_Data_Plot   import tdc_Data_Sequence_Initializer


from xps_plotter__OF import XPs_Plotter__OF


def plot_xp__OF_movie(plot_module,
                      calc_ids,
                      particle_names,
                      ylim,
                      of__filename,
                      sample_dict=None,
                      xlim=None,
                      tt=None,
                      fps=None,
                      keep_frame_files=None,
                      moving_grid_dict=None,
                      use_cell_coordinates=False,
                      show_cells=False,
                      time_normalization=None,
                      fig_param=None,
                      **kwargs):
    """
    plots XP phase portrait movie on top of theoretical dependence p(x)
    for space charge limited flow
    ------------
    of__filename
       theoretical curve  p(x) for oscillation solution is in the file 'of__filename.h5'
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
                                                    tt=tt,
                                                    time_normalization=time_normalization,
                                                    **kwargs) )
    # plotter
    pp  = XPs_Plotter__OF(xps=xps, of__filename=of__filename)
    if use_cell_coordinates:
        pp.use_cell_coordinates()
    if show_cells:
        pp.show_cells_on()
    # plot moving grid if asked
    if moving_grid_dict:
        pp  = tdc_Moving_Grid_Plotter(pp,moving_grid_dict)
    # movie frames
    MF = plot_module.Movie.Single_Panel_Movie_Frames(pp, ylim=ylim, xlim=xlim, fig_param=fig_param)
    # movie_id - directory with the movie file
    movie_id = 'XP' + '_' + calc_ids[0]
    # -----------------------------------------
    # make movie
    plot_module.Movie.plot_movie( MF, movie_id, fps, keep_frame_files)
