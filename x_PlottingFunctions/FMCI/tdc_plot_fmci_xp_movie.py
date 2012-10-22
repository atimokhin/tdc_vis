from FMCI import tdc_FMCI_Sequence, tdc_FMCI_XP_Plotter, tdc_FMCI_XP_Data

def tdc_plot_fmci_xp_movie(plot_module,
                           fmci_id,
                           particle_name,
                           ylim,
                           xlim,
                           wlims,
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

    *NB* This move takes a lot of time to make in interactive mode,
         it is impractical to do so, it should be make in command line mode
    """
    # FMCI_XP sequence
    fmci_XPs = tdc_FMCI_Sequence.init_from_data(tdc_FMCI_XP_Data, 
                                                fmci_id, 
                                                particle_name,
                                                ii = ii )
    # plotter
    pp  = tdc_FMCI_XP_Plotter(fmci_XPs = fmci_XPs,
                              wlims=wlims,
                              xlabel=xlabel, ylabel=ylabel, idlabel=idlabel)
    # movie frames
    MF = plot_module.MovieFrames.Single_Panel_Movie_Frames( pp,
                                                            ylim=ylim,
                                                            xlim=xlim,
                                                            axes_commands=axes_commands,
                                                            fig_param=fig_param)
    # movie_id - directory with the movie file
    movie_id = 'FMCI_XP__' + fmci_id
    # -----------------------------------------
    # make movie
    plot_module.MovieMakers.plot_movie( MF, movie_id, fps, keep_frame_files,
                                        symlog=symlog,
                                        linthreshy=linthreshy)
