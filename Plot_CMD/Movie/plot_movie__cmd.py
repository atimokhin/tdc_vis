from single_panel_movie_frames  import Single_Panel_Movie_Frames
from movie_file_maker__cmd      import Movie_File_Maker__CMD


def plot_movie__cmd( plotter, movie_id, fps, ylim, xlim=None, **kwargs ):
    """
    plot_movie__cmd( plotter, movie_id, ylim, fps, **kwargs )
    Common function for creating movie file from the command line interface
    plotter
    movie_id  -- name of directory where frames and later movie file will be stored
    ylim
    fps
    **kwargs  -- goes to Single_Panel_Movie_Frames
    """
    # movie frames
    MF = Single_Panel_Movie_Frames(plotter, ylim=ylim, **kwargs)    
    # movie file maker
    MFM = Movie_File_Maker__CMD(movie_id, fps)
    # write frames ----------------------------
    MFM.open_index_file()
    for i in range(MF.i_frame_min, MF.i_frame_max):
        MF.animation_update(i)
        print 'Saving frame %4d (out of %d)' % (i,MF.i_frame_max)  
        MFM.store_snapshot(MF.figure)
    MFM.close_index_file()
    # create movie file -----------------------
    MFM.combine_frames_into_movie()
    print 'Movie file created: fps = %d, frames = %d ' % (MFM.fps, MFM.get_number_of_saved_snapshots())
    MFM.delete_frame_files()
