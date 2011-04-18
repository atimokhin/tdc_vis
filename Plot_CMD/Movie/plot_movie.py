from movie_file_maker__cmd      import Movie_File_Maker__CMD

def plot_movie( movie_frames, movie_id, fps, keep_frame_files):
    """
    plot_movie__cmd( plotter, movie_id, ylim, fps, **kwargs )
    Common function for creating movie file from the command line interface
    ------------
    params:
    ------------
    movie_frames -- MovieFrames class instance
    movie_id     -- name of directory where frames and later movie file will be stored
    fps
    """
    # movie frames
    MF = movie_frames
    # movie file maker
    MFM = Movie_File_Maker__CMD(movie_id, fps, keep_frame_files)
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
