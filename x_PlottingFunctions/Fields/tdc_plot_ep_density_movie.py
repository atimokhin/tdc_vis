from Auxiliary import tdc_Filenames

from Common_Data_Plot   import tdc_Data_Sequence
from Auxiliary_Plotters import tdc_Moving_Grid_Plotter
from Fields import tdc_Field_Data, tdc_EP_Density_Plotter, tdc_EPG_Density_Plotter, tdc_EPGP_Density_Plotter

def tdc_plot_ep_density_movie(plot_module,
                              calc_ids,
                              ylim,
                              xlim=None,
                              tt=None,
                              e_density_negative=True,
                              fps=None,
                              keep_frame_files=None,
                              moving_grid_dict=None,
                              use_cell_coordinates=False,
                              show_cells=False,
                              time_normalization=None,
                              xlabel=None,ylabel=None,idlabel=None,
                              fig_param=None,
                              **kwargs):
    """
    calc_ids
        calculation id names
    ylim
        Y axis limits   
    Options:
    --------
    xlim
        <None> X axis limits
    tt
        <None> time interval <[t1,<t2>]>
    moving_grid_dict
        <None>  if specified plot moving grid
            moving_grid_dict = dict(n_lines=20, speed=1)
    e_density_negative,
        <True> plot electron density as negative (True) or positive (False) values
    use_cell_coordinates
        <False>
    show_cells
        <False>
    time_normalization
        <None>
    **kwargs
        go to tdc_*_Data via tdc_Data_Sequence.init_from_data
    """

    # make sure calc_id is a sequence
    if not isinstance( calc_ids, (list,tuple) ):
        calc_ids = (calc_ids,)

    # field sequence
    fe  = tdc_Data_Sequence.init_from_data( tdc_Field_Data,
                                         calc_ids=calc_ids,
                                         field_name='N',
                                         filename='prop_Electrons.h5',
                                         tt=tt,
                                         time_normalization=time_normalization,
                                         **kwargs)
    fp  = tdc_Data_Sequence.init_from_data( tdc_Field_Data,
                                         calc_ids=calc_ids,
                                         field_name='N',
                                         filename='prop_Positrons.h5',
                                         tt=tt,
                                         time_normalization=time_normalization,
                                         **kwargs)
    plotter  = tdc_EP_Density_Plotter(fe,fp,e_density_negative,
                                      xlabel=xlabel, ylabel=ylabel, idlabel=idlabel)
    # plot moving grid if asked
    if moving_grid_dict:
        plotter  = tdc_Moving_Grid_Plotter(plotter,moving_grid_dict)
    # movie frames
    MF = plot_module.MovieFrames.Single_Panel_Movie_Frames(plotter, ylim=ylim, xlim=xlim, fig_param=fig_param)
    # movie_id - directory with the movie file
    movie_id = 'EP' + '_' + calc_ids[0]
    # -----------------------------------------
    # make movie
    plot_module.MovieMakers.plot_movie( MF, movie_id, fps, keep_frame_files)


def tdc_plot_epg_density_movie(plot_module,
                               calc_ids,
                               ylim,
                               xlim=None,
                               tt=None,
                               e_density_negative=True,
                               fps=None,
                               keep_frame_files=None,
                               moving_grid_dict=None,
                               use_cell_coordinates=False,
                               show_cells=False,
                               time_normalization=None,
                               fig_param=None,
                               **kwargs):
    """
    Plots movie for number density of (e)lectrons, (p)positrons, (g)amma-rays
    as a function of the distanse n(x)
    ==> Movie is stored in  sub-directory {RESULTS_VIS}/EPG{calc_ids[0]}
    =======
    calc_ids
        calculation id names
    ylim
        Y axis limits   
    Options:
    --------
    xlim
        <None> X axis limits
    tt
        <None> time interval <[t1,<t2>]>
    moving_grid_dict
        <None>  if specified plot moving grid
            moving_grid_dict = dict(n_lines=20, speed=1)
    e_density_negative,
        <True> plot electron density as negative (True) or positive (False) values
    use_cell_coordinates
        <False>
    show_cells
        <False>
    time_normalization
        <None>
    **kwargs
        go to tdc_*_Data via tdc_Data_Sequence.init_from_data
    """

    # make sure calc_id is a sequence
    if not isinstance( calc_ids, (list,tuple) ):
        calc_ids = (calc_ids,)

    # field sequence
    fe  = tdc_Data_Sequence.init_from_data( tdc_Field_Data,
                                         calc_ids=calc_ids,
                                         field_name='N',
                                         filename='prop_Electrons.h5',
                                         tt=tt,
                                         time_normalization=time_normalization,
                                         **kwargs)
    fp  = tdc_Data_Sequence.init_from_data( tdc_Field_Data,
                                         calc_ids=calc_ids,
                                         field_name='N',
                                         filename='prop_Positrons.h5',
                                         tt=tt,
                                         time_normalization=time_normalization,
                                         **kwargs)
    fg  = tdc_Data_Sequence.init_from_data( tdc_Field_Data,
                                         calc_ids=calc_ids,
                                         field_name='N',
                                         filename='prop_Pairs.h5',
                                         tt=tt,
                                         time_normalization=time_normalization,
                                         **kwargs)
    plotter  = tdc_EPG_Density_Plotter(fe,fp,fg,e_density_negative)
    # plot moving grid if asked
    if moving_grid_dict:
        plotter  = tdc_Moving_Grid_Plotter(plotter,moving_grid_dict)
    # movie frames
    MF = plot_module.MovieFrames.Single_Panel_Movie_Frames(plotter, ylim=ylim, xlim=xlim, fig_param=fig_param)
    # movie_id - directory with the movie file
    movie_id = 'EPG' + '_' + calc_ids[0]
    # -----------------------------------------
    # make movie
    plot_module.MovieMakers.plot_movie( MF, movie_id, fps, keep_frame_files)


def tdc_plot_epgp_density_movie(plot_module,
                                calc_ids,
                                ylim,
                                xlim=None,
                                tt=None,
                                e_density_negative=True,
                                fps=None,
                                keep_frame_files=None,
                                moving_grid_dict=None,
                                use_cell_coordinates=False,
                                show_cells=False,
                                time_normalization=None,
                                fig_param=None,
                                **kwargs):
    """
    Plots movie for number density of (e)lectrons, (p)positrons, (g)amma-rays, (p)rotons
    as a function of the distanse n(x)
    ==> Movie is stored in  sub-directory {RESULTS_VIS}/EPGP{calc_ids[0]}
    =======
    calc_ids
        calculation id names
    ylim
        Y axis limits   
    Options:
    --------
    xlim
        <None> X axis limits
    tt
        <None> time interval <[t1,<t2>]>
    moving_grid_dict
        <None>  if specified plot moving grid
            moving_grid_dict = dict(n_lines=20, speed=1)
    e_density_negative,
        <True> plot electron density as negative (True) or positive (False) values
    use_cell_coordinates
        <False>
    show_cells
        <False>
    time_normalization
        <None>
    **kwargs
        go to tdc_*_Data via tdc_Data_Sequence.init_from_data
    """

    # make sure calc_id is a sequence
    if not isinstance( calc_ids, (list,tuple) ):
        calc_ids = (calc_ids,)

    # field sequence
    fe  = tdc_Data_Sequence.init_from_data( tdc_Field_Data,
                                            calc_ids=calc_ids,
                                            field_name='N',
                                            filename='prop_Electrons.h5',
                                            tt=tt,
                                            time_normalization=time_normalization,
                                            **kwargs)
    fp  = tdc_Data_Sequence.init_from_data( tdc_Field_Data,
                                            calc_ids=calc_ids,
                                            field_name='N',
                                            filename='prop_Positrons.h5',
                                            tt=tt,
                                            time_normalization=time_normalization,
                                            **kwargs)
    fg  = tdc_Data_Sequence.init_from_data( tdc_Field_Data,
                                            calc_ids=calc_ids,
                                            field_name='N',
                                            filename='prop_Pairs.h5',
                                            tt=tt,
                                            time_normalization=time_normalization,
                                            **kwargs)
    fpr = tdc_Data_Sequence.init_from_data( tdc_Field_Data,
                                            calc_ids=calc_ids,
                                            field_name='N',
                                            filename='prop_Protons.h5',
                                            tt=tt,
                                            time_normalization=time_normalization,
                                            **kwargs)
    plotter  = tdc_EPGP_Density_Plotter(fe,fp,fg,fpr,e_density_negative)
    # plot moving grid if asked
    if moving_grid_dict:
        plotter  = tdc_Moving_Grid_Plotter(plotter,moving_grid_dict)
    # movie frames
    MF = plot_module.MovieFrames.Single_Panel_Movie_Frames(plotter, ylim=ylim, xlim=xlim, fig_param=fig_param)
    # movie_id - directory with the movie file
    movie_id = 'EPGP' + '_' + calc_ids[0]
    # -----------------------------------------
    # make movie
    plot_module.MovieMakers.plot_movie( MF, movie_id, fps, keep_frame_files)
