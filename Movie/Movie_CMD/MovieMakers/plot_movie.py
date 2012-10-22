from movie_file_maker__cmd      import Movie_File_Maker__CMD

def plot_movie( movie_frames, movie_id, fps, keep_frame_files, **kwargs):
    """
    plot_movie( plotter, movie_id, ylim, fps, **kwargs )
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
    MFM = Movie_File_Maker__CMD(movie_id, fps, keep_frame_files, dpi=MF.MFS.dpi)
    # write frames ----------------------------
    MFM.setup_directory()
    # force to delete all frame files
    MFM.delete_frame_files(force_delete=True)
    MFM.open_index_file()
    for i in range(MF.i_frame_min, MF.i_frame_max):
        # ====> here keyword parameters go to the plotter's plot method <=====
        MF.animation_update(i+1,**kwargs)
        print 'Saving frame %4d (out of %d)' % (i+1,MF.i_frame_max)  
        MFM.store_snapshot(MF.figure)
    MFM.close_index_file()
    # create movie file -----------------------
    MFM.combine_frames_into_movie()
    MFM.delete_frame_files()
