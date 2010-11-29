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


    def __init__(self, movie_id):
        """
        movie_id  -- subdirectorty where movie files will be stored
        """
        Movie_File_Maker.__init__(self,movie_id)
        self.index_file = None

    def store_snapshot(self, i_frame, figure):
        # name of the file where current frame will be saved
        filename = self.movie_dir_name + \
                   self._frame_filename + '_' + str(i_frame) + '.png'
        # create frame file, save frame there, then close the file 
        figure.savefig(filename)
        # append name of the frame file to the list
        self.index_file.write(filename+'\n')
        
    def open_index_file(self):
        # open index file
        self.index_file = open(self.index_filename, 'w')

    def close_index_file(self):
        # open index file
        self.index_file.close()
        


