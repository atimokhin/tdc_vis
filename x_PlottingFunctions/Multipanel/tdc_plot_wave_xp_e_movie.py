from Common_Data_Plot   import tdc_Data_Sequence
from Auxiliary_Plotters import tdc_Moving_Grid_Plotter

from Particles import tdc_XP_Data, tdc_XPs_Plotter, tdc_XPs_TP_Plotter
from Fields             import tdc_Field_Data, tdc_Fields_Plotter

def tdc_plot_wave_xp_e_movie(plot_module,
                             calc_ids,
                             particle_names,
                             ylims,
                             sample_dict=None,
                             xlims=None,
                             tt=None,
                             fps=None,
                             keep_frame_files=None,
                             moving_grid_dict=None,
                             use_cell_coordinates=False,
                             show_cells=False,
                             time_normalization=None,
                             symlog=False,
                             linthreshy=5,
                             axes_commands=None,
                             xlabel=None,ylabel=None,idlabel=None,
                             fig_param=None,
                             plot_style=None,
                             **kwargs):
    """
    calc_ids
       calculation id names
    particle_name
       particle names
    ylims
       Y axis limits: must be a list with 2 entries   
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
    axes_commands
       <None>
    **kwargs
       go to tdc_*_Data via tdc_Data_Sequence.init_from_data
    """
    # make sure calc_id is a sequence
    if not isinstance( calc_ids, (list,tuple) ):
        calc_ids = (calc_ids,)

    # make sure particle_names is a sequence
    if not isinstance( particle_names, (list,tuple) ):
        particle_names = (particle_names,)
        
    # particles sequence
    xps = [ tdc_Data_Sequence.init_from_data( tdc_XP_Data,
                                              calc_ids=calc_ids,
                                              particle_name=pname,
                                              sample_dict=sample_dict,
                                              tt=tt,
                                              time_normalization=time_normalization,
                                              **kwargs) for pname in particle_names ]
    # plotter
    xps_pp = tdc_XPs_Plotter(xps=xps,
                             xlabel=xlabel, ylabel=ylabel, idlabel=idlabel)

    # field sequence ---------------------------------
    fs  = tdc_Data_Sequence.init_from_data( tdc_Field_Data,
                                            calc_ids=calc_ids,
                                            field_name='E_acc',
                                            tt=tt,
                                            time_normalization=time_normalization,
                                            **kwargs)
    # field plotter
    e_pp  = tdc_Fields_Plotter(fs,
                               xlabel=xlabel, ylabel=ylabel, idlabel=idlabel)
    if plot_style is not None:
        xps_pp.set_plotstyle(**plot_style)
        e_pp.set_plotstyle(**plot_style)
    if use_cell_coordinates:
        xps_pp.use_cell_coordinates()
        e_pp.use_cell_coordinates()
    if show_cells:
        xps_pp.use_cell_coordinates()
        e_pp.show_cells_on()
    # plot moving grid if asked
    if moving_grid_dict:
        xps_pp = tdc_Moving_Grid_Plotter(xps_pp,moving_grid_dict)
        e_pp = tdc_Moving_Grid_Plotter(e_pp,moving_grid_dict)
    # movie frames
    MF = plot_module.MovieFrames.Double_Panel_Movie_Frames( (xps_pp, e_pp),
                                                            ylims=ylims,
                                                            xlims=xlims,
                                                            axes_commands=axes_commands,
                                                            fig_param=fig_param)
    # movie_id - directory with the movie file
    movie_id = 'Wave__XP_Eacc_%s' %  calc_ids[0]
    # -----------------------------------------
    # make movie
    plot_module.MovieMakers.plot_movie( MF, movie_id, fps, keep_frame_files,
                                        symlog=symlog,
                                        linthreshy=linthreshy )
