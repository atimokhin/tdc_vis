from Common_Data_Plot import tdc_Data_Sequence_Initializer
from Fields           import tdc_Field_Data, tdc_Fields_Diff_Data, tdc_Fields_Plotter


def plot_test_e_e_gauss_movie(plot_module,
                              calc_ids,
                              ylim,
                              xlim=[None,None],
                              tt=None,
                              fps=None,
                              moving_grid_dict=None,
                              use_cell_coordinates=False,
                              show_cells=False,
                              time_normalization=None,
                              **kwargs):
    """
    Plots movie with two panels: E_acc and E_acc-E_Gauss
    -------
    Params:
    -------
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
       go to tdc_*_Data via tdc_Data_Sequence_Initializer
    """
    # make sure calc_id is a sequence ----------------
    if not isinstance( calc_ids, (list,tuple) ):
        calc_ids = (calc_ids,)        
    # field sequences ---------------------------------
    fs1  = tdc_Data_Sequence_Initializer( tdc_Field_Data,
                                          calc_ids=calc_ids,
                                          field_name='E_acc',
                                          tt=tt,
                                          time_normalization=time_normalization,
                                          **kwargs)
    # field sequences ---------------------------------
    fs2  = tdc_Data_Sequence_Initializer( tdc_Fields_Diff_Data,
                                          calc_ids=calc_ids,
                                          field1_name='E_acc',
                                          field2_name='E_Gauss',
                                          tt=tt,
                                          time_normalization=time_normalization,
                                          **kwargs)
    # field plotter
    fp1 = tdc_Fields_Plotter(fs1)
    fp2 = tdc_Fields_Plotter(fs2)
    if use_cell_coordinates:
        fp1.use_cell_coordinates()
        fp2.use_cell_coordinates()
    if show_cells:
        fp1.show_cells_on()
        fp2.show_cells_on()
    # movie frames
    MF = plot_module.Movie.Double_Panel_Movie_Frames( (fp1,fp2), ylim=ylim, xlim=xlim, **kwargs)
    # movie_id - directory with the movie file
    movie_id = 'E__E_Gauss__' + calc_ids[0]
    # -----------------------------------------
    # make movie
    plot_module.Movie.plot_movie( MF, movie_id, fps)
