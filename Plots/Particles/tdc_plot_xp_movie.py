from Common    import tdc_Data_Sequence, tdc_Data_Sequence_Initializer, tdc_Moving_Grid_Plotter

from Particles.tdc_xp_data           import tdc_XP_Data
from Particles.tdc_xps_tp_plotter    import tdc_XPs_Plotter, tdc_XPs_TP_Plotter

def tdc_plot_xp_movie(plot_module,
                      calc_ids,
                      particle_names,
                      ylim,
                      sample_dict=None,
                      xlim=None,
                      tt=None,
                      fps=None,
                      keep_frame_files=None,
                      tp=None,
                      trail_dict=None,
                      moving_grid_dict=None,
                      use_cell_coordinates=False,
                      show_cells=False,
                      time_normalization=None,
                      symlog=False,
                      linthreshy=5,
                      **kwargs):
    """
    calc_ids
       calculation id names
    particle_name
       particle names
    ylim
       Y axis limits   
    Options:
    --------
    sample_dic
       <None> dictionary with sample parameters
              sample_dict = dict(name='regular',n_reduce=10,n_min=1000)
    xlim
       <None> X axis limits
    tt
       time interval <[t1,<t2>]>
    moving_grid_dict
       <None>  if specified plot moving grid
               moving_grid_dict = dict(n_lines=20, speed=1)
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
    # tracked particles sequence
    tps = tdc_Data_Sequence(tp, tt=tt) if tp else None
    # plotter
    pp  = tdc_XPs_TP_Plotter(xps=xps, tp=tps,trail_dict=trail_dict)
    if use_cell_coordinates:
        pp.use_cell_coordinates()
    if show_cells:
        pp.show_cells_on()
    # plot moving grid if asked
    if moving_grid_dict:
        pp  = tdc_Moving_Grid_Plotter(pp,moving_grid_dict)
    # movie frames
    MF = plot_module.Movie.Single_Panel_Movie_Frames(pp, ylim=ylim, xlim=xlim)
    # movie_id - directory with the movie file
    movie_id = 'XP' + '_' + calc_ids[0]
    # -----------------------------------------
    # make movie
    plot_module.Movie.plot_movie( MF, movie_id, fps, keep_frame_files,
                                  symlog=symlog,
                                  linthreshy=linthreshy
                                  )
