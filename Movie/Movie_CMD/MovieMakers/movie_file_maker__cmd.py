from Movie import Movie_File_Maker

class Movie_File_Maker__CMD(Movie_File_Maker):
    """
    Make movie file
    - store_snapshot()  store each figure as a separate png file
    - open_index_file()
    - close_index_file()
    --------
    Members:
    --------
    movie_filename
       name of the created movie file
    fps
       fps of created movie file
    keep_frame_files_flag
       [True/False] whether to keep png frame files after creating movie
    dpi
       dpi for figure.savefig()
       resolution of png files saved for each frame
       NB: this member is absent in __GUI version! 
    """

    def __init__(self, 
                 movie_id, 
                 fps, 
                 keep_frame_files, 
                 dpi,
                 movie_file_basename=None,
                 frame_filename_format=None):
        """
        movie_id
           subdirectorty where movie files will be stored
        fps
           fps of created movie file
        keep_frame_files_flag
           [True/False] whether to keep png frame files after creating movie
        dpi
           dpi for figure.savefig()
         """
        # setup base class
        Movie_File_Maker.__init__(self,
                                  movie_id,
                                  fps,
                                  keep_frame_files, 
                                  movie_file_basename=movie_file_basename,
                                  frame_filename_format=frame_filename_format)
        # dpi - use the same dpi as figure plot
        self.dpi = dpi

    def store_snapshot(self, figure):
        """
        each snapshot is a figure saved as separate png file
        """
        # name of the file where current frame will be saved
        filename = self.get_frame_filename(self.i_saved_frame+1)
        # create frame file, save frame there, then close the file
        # use dpi saved at class initialization
        figure.savefig( filename, dpi=self.dpi )
        # append name of the frame file to the list
        self.add_filename_to_index_file(filename)
        
        


