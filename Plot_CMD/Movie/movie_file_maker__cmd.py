from Movie import Movie_File_Maker

class Movie_File_Maker__CMD(Movie_File_Maker):
    """
    Make movie file
    - store_snapshot()  takes snapshot of the widget (figure canvas)
    - open_index_file()
    - close_index_file()
    
    Members:
    --------
    movie_filename
       name of the created movie file
    fps
       fps of created movie file
    keep_frame_files_flag
       whether to keep png frame files after creating movie
       default - False
    """

    # default value for fps in CMD interface
    __default_fps = 7

    def __init__(self, movie_id, fps=None):
        """
        movie_id  -- subdirectorty where movie files will be stored
        """
        # set fps to default value if it is not given in function call
        if not fps:
            fps = self.__default_fps
        # setup base class
        Movie_File_Maker.__init__(self,movie_id,fps)
        self.index_file = None
        # frame counter
        self.i_frame = 0

    def get_number_of_saved_snapshots(self):
        return self.i_frame

    def store_snapshot(self, figure):
        # name of the file where current frame will be saved
        filename = self.movie_dir_name + \
                   self._frame_filename + '_' + str(self.i_frame) + '.png'
        # create frame file, save frame there, then close the file 
        figure.savefig(filename)
        # append name of the frame file to the list
        self.index_file.write(filename+'\n')
        # increment frame counter
        self.i_frame += 1
        
    def open_index_file(self):
        # open index file
        self.index_file = open(self.index_filename, 'w')
        # clear number of snapshots
        self.i_frame = 0

    def close_index_file(self):
        # open index file
        self.index_file.close()
        


