from movie_file_maker__gui import Movie_File_Maker__GUI
from movie_maker import Movie_Maker

def plot_movie( movie_frames, movie_id, fps, keep_frame_files ):
    """
    plot_movie( movie_frames, movie_id, fps )
    Common function for creating movie -- specific for GUI
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
    MFM = Movie_File_Maker__GUI(movie_id, fps, keep_frame_files)
    # movie maker
    MM = Movie_Maker(MF, MFM)
    # play movie
    MM.animate()
