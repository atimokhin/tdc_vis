import os
import time

import subprocess

from Common.tdc_filenames import *

class Movie_File_Maker:
    """
    Make movie file
    - store_snapshot()  takes snapshot of the widget (figure canvas)
    - save_png_snapshots_to_disk() saves each snapshot into a separate file
    
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
    
    __index_filename         = 'index.txt'
    _frame_filename          = 'frame'
    _default_movie_filename  = 'animation'

    def __init__(self, movie_id, fps, keep_frame_files):
        """
        movie_id  -- subdirectorty whewre movie files will be stored
        fps       -- fps of created movie
        keep_frame_files -- whether to keep .png frame files 
        """
        # FPS
        self.fps = fps
        # movie_id
        self.movie_id = movie_id
        # directory where image and movie fiels will be saved
        self.movie_dir_name = tdc_get_vis_fielname(movie_id,'')
        ## # if directory does not exist - create it
        ## if not os.path.exists(self.movie_dir_name):
        ##     os.mkdir(self.movie_dir_name)
        # filenames (frames and index)
        self.index_filename = tdc_get_vis_fielname(self.movie_id,
                                                   self.__index_filename)
        self.set_movie_filenames(self._default_movie_filename)
        # keep_frame_files_flag
        self.set_keep_frame_files_flag(keep_frame_files)

    def setup_directory(self):
        # if directory does not exist - create it
        if not os.path.exists(self.movie_dir_name):
            os.mkdir(self.movie_dir_name)
        
    def set_movie_filenames(self,filename):
        self.movie_filename = tdc_get_vis_fielname(self.movie_id, filename+".mp4")
        self.h264_filename  = tdc_get_vis_fielname(self.movie_id, filename+".h264")
        
    def set_fps(self,fps):
        self.fps = fps

    def set_keep_frame_files_flag(self,val):
        self.keep_frame_files_flag = val

    
    def combine_frames_into_movie(self):
        """
        combines all snapshots into a single movie file
        it calls external command (mencoder) to do this
        1) mencoder combines .png files into .h264 rawvideo file
        2) MP4Box puts .h264 file into .mp4 container
        3) deletes .h264 temporaty file
        """
        # [shifruemsya na klastere] ---
        import os
        my_host = os.environ.get('MY_HOST','nohost')
        # mencoder command [shifruemsya na klastere]
        mencoder_command = 'combine.exe' if my_host=='henyey' else 'mencoder'        
        # -----------------------------
        # run mencoder which combines frames into a movie
        # mpeg4 movie
        command_string = \
                       mencoder_command + " mf://@" + self.index_filename + " " +\
                       "-o "             + self.h264_filename  + " " +\
                       "-mf fps="        + str(self.fps)       + " " +\
                       "-of rawvideo -ovc x264 -x264encopts "        +\
                       "bitrate=1500:subq=5:frameref=3:bframes=0:threads=auto" +\
                       "; " +\
                       "MP4Box -fps " + str(self.fps) + " " +\
                       "-new -add " + self.h264_filename + " " + self.movie_filename +\
                       "; " +\
                       "rm -f " + self.h264_filename

        p = subprocess.Popen(command_string, shell=True,
                             stdin  = subprocess.PIPE,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE)
        for i in p.stdout:
            print i
        status = p.wait()
        # if something went wrong - show message
        return not status
    

    def delete_frame_files(self):
        """
        Delete frame files if self.keep_frame_files_flag is not set
        """
        if not self.keep_frame_files_flag:
            # do index file exist?
            status0 = os.path.exists(self.index_filename )
            # delete frame files
            command_string = "rm -f `cat " + self.index_filename + "`"  
            p = subprocess.Popen(command_string, shell=True)
            status1 = p.wait()
            # delete index file
            p = subprocess.Popen("rm -f " + self.index_filename, shell=True)
            status2 = p.wait()
            return status0 and (not status1) and (not status2)
        else:
            return False
