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

    def __init__(self, movie_id, fps, keep_frame_files, dpi):
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
        Movie_File_Maker.__init__(self,movie_id,fps,keep_frame_files)
        self.index_file = None
        # frame counter
        self.i_frame = 0
        # dpi - use the same dpi as figure plot
        self.dpi = dpi

    def get_number_of_saved_snapshots(self):
        return self.i_frame

    def store_snapshot(self, figure):
        """
        each snapshot is a figure saved as separate png file
        """
        # name of the file where current frame will be saved
        filename = self.movie_dir_name + \
                   self._frame_filename + '_' + str(self.i_frame) + '.png'
        # create frame file, save frame there, then close the file
        # use dpi saved at class initialization
        figure.savefig(filename,dpi=self.dpi)
        # append name of the frame file to the list
        self.index_file.write(filename+'\n')
        # increment frame counter
        self.i_frame += 1
        
    def open_index_file(self):
        # setup output directory
        self.setup_directory()
        # open index file
        self.index_file = open(self.index_filename, 'w')
        # clear number of snapshots
        self.i_frame = 0

    def close_index_file(self):
        # open index file
        self.index_file.close()
        


