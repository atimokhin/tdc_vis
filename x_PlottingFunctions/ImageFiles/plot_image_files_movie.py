from ImageFiles import Image_Data, Image_Plotter, Image_Sequence

def plot_image_files_movie(plot_module,
                           image_id,
                           ii=None,
                           fps=None,
                           keep_frame_files=None,
                           **kwargs):
    """
    plot_module
       module with plot_movie function 
    image_id
       image id (directory with image files)
    --------
    Options:
    --------
    ii
       i_ts index interval <[i1,<i2>]>           
    **kwargs
       go to tdc_*_Data via Image_Sequence.init_from_data
    """
    # image sequence ---------------------------------
    im_seq  = Image_Sequence.init_from_data(Image_Data, image_id, ii=ii, **kwargs)
    # field plotter
    im_plt  = Image_Plotter(im_seq)
    # movie frames
    MF = plot_module.MovieFrames.Image_Single_Panel_Movie_Frames(im_plt)
    # movie_id - directory with the movie file
    movie_id = 'IM: ' + image_id
    # -----------------------------------------
    # make movie
    plot_module.MovieMakers.plot_movie( MF, movie_id, fps, keep_frame_files)
