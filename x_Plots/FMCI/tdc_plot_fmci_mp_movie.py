from FMCI import tdc_FMCI_Sequence, tdc_FMCI_MP_Plotter, tdc_FMCI_MP_Data

def tdc_plot_fmci_mp_movie(plot_module,
                           fmci_id,
                           particle_names,
                           ylim,
                           xlim,
                           m_max,
                           w_max,
                           ii=None,
                           fps=None,
                           keep_frame_files=None,
                           symlog=True,
                           linthreshy=5,
                           axes_commands=None,
                           xlabel=None,ylabel=None,idlabel=None,
                           fig_param=None,
                           **kwargs):
    """
    fmci_id
       root dir with FMCI ascii data files
    particle_names
       particle names
    ylim
       Y axis limits   
    xlim
       X axis limits   
    m_max
       maximum marker size
    w_max
       maximum distinguishable statistical weight
       (particles with larger weighs will have their markersize set to m_max)
    --------
    Options:
    --------
    ii
       i_ts index interval <[i1,<i2>]>
    axes_commands
       <None>
    **kwargs
       go to tdc_*_Data via tdc_Data_Sequence_Initializer
    """
    # make sure particle_names is a sequence
    if not isinstance( particle_names, (list,tuple) ):
        particle_names = (particle_names,)
    # particles sequence
    fmci_MPs=[ tdc_FMCI_Sequence.init_from_data(tdc_FMCI_MP_Data, 
                                                fmci_id, 
                                                pname,
                                                m_max = m_max,
                                                w_max = w_max,
                                                ii = ii ) for pname in particle_names ]
    # plotter
    pp  = tdc_FMCI_MP_Plotter(fmci_MPs=fmci_MPs,
                              xlabel=xlabel, ylabel=ylabel, idlabel=idlabel)
    # movie frames
    MF = plot_module.Movie.Single_Panel_Movie_Frames( pp,
                                                      ylim=ylim,
                                                      xlim=xlim,
                                                      axes_commands=axes_commands,
                                                      fig_param=fig_param)
    # movie_id - directory with the movie file
    movie_id = 'FMCI_MP__' + fmci_id
    # -----------------------------------------
    # make movie
    plot_module.Movie.plot_movie( MF, movie_id, fps, keep_frame_files,
                                  symlog=symlog,
                                  linthreshy=linthreshy)
