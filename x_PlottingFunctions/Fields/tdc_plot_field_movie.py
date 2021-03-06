from Auxiliary import tdc_Filenames

from Common_Data_Plot   import tdc_Data_Sequence
from Auxiliary_Plotters import tdc_Moving_Grid_Plotter
from Fields             import tdc_Field_Data, tdc_Fields_Plotter

def tdc_plot_field_movie(plot_module,
                         calc_ids,
                         field_name,
                         ylim,
                         xlim=None,
                         tt=None,
                         fps=None,
                         keep_frame_files=None,
                         moving_grid_dict=None,
                         use_cell_coordinates=False,
                         show_cells=False,
                         time_normalization=None,
                         xlabel=None,ylabel=None,idlabel=None,
                         fig_param=None,
                         plot_style=None,
                         **kwargs):
    """
    plot_module
       module with plot_movie function 
    calc_ids
       calculation id names
    field_name
       name of the field to be plotted
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
    use_cell_coordinates
       <False>
    show_cells
       <False>
    time_normalization
       <None>
    **kwargs
       go to tdc_*_Data via tdc_Data_Sequence.init_from_data
    """
    # make sure calc_id is a sequence ----------------
    if not isinstance( calc_ids, (list,tuple) ):
        calc_ids = (calc_ids,)        
    # field sequence ---------------------------------
    fs  = tdc_Data_Sequence.init_from_data( tdc_Field_Data,
                                            calc_ids=calc_ids,
                                            field_name=field_name,
                                            tt=tt,
                                            time_normalization=time_normalization,
                                            **kwargs)
    # field plotter
    fp  = tdc_Fields_Plotter(fs,
                             xlabel=xlabel, ylabel=ylabel, idlabel=idlabel)
    if plot_style is not None:
        fp.set_plotstyle(**plot_style)
    if use_cell_coordinates:
        fp.use_cell_coordinates()
    if show_cells:
        fp.show_cells_on()
    # plot moving grid if asked
    if moving_grid_dict:
        fp  = tdc_Moving_Grid_Plotter(fp,moving_grid_dict)
    # movie frames
    MF = plot_module.MovieFrames.Single_Panel_Movie_Frames(fp, ylim=ylim, xlim=xlim, fig_param=fig_param)
    # movie_id - directory with the movie file
    movie_id = field_name + '_' + calc_ids[0]
    # -----------------------------------------
    # make movie
    plot_module.MovieMakers.plot_movie( MF, movie_id, fps, keep_frame_files)
