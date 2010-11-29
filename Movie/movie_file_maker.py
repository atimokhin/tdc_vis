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
    main_Window
       main window - necessary for showing pop-up windows
    update_number_of_recorded_frames_function
       function which updated # of recorded frames shown in GUI
    """

    __index_filename         = 'index.txt'
    _frame_filename          = 'frame'
    _default_movie_filename  = 'animation'
    _default_fps             = 24

    def __init__(self, movie_id):
        """
        movie_id  -- subdirectorty whewre movie files will be stored
        """
        # FPS
        self.set_fps(self._default_fps)
        # movie_id
        self.movie_id = movie_id
        # directory where image and movie fiels will be saved
        self.movie_dir_name = tdc_get_vis_fielname(movie_id,'')
        # if directory does not exist - create it
        if not os.path.exists(self.movie_dir_name):
            os.mkdir(self.movie_dir_name)
        # filenames (frames and index)
        self.index_filename = tdc_get_vis_fielname(self.movie_id,
                                                   self.__index_filename)
        self.set_movie_filenames(self._default_movie_filename)
        # keep_frame_files_flag
        self.set_keep_frame_files_flag(False)
        # initialize internal list with frames in png format
        self.frames_png = []


    def set_movie_filenames(self,filename):
        self.movie_filename = tdc_get_vis_fielname(self.movie_id, filename+".mp4")
        self.h264_filename  = tdc_get_vis_fielname(self.movie_id, filename+".h264")
        
    def set_fps(self,fps):
        self.fps = fps

    def set_keep_frame_files_flag(self,val):
        self.keep_frame_files_flag = val

    def get_number_of_saved_snapshots(self):
        return len(self.frames_png)


    def save_png_snapshots_to_disk(self):
        """
        saves all PNGs on to the disk as separate files
        if frame buffer is not empty
        """
        if len(self.frames_png):
            # open index file
            index_file = open(self.index_filename, 'w')
            print 'total # of stored frames', len(self.frames_png)
            # save individual frames
            for idx,frame in enumerate(self.frames_png):
                # name of the file where current frame will be saved
                filename = self.movie_dir_name + \
                           self._frame_filename + '_' + str(idx) + '.png'
                # create frame file, save frame there, then close the file 
                frame_file = open(filename,"w")
                frame_file.write(frame)
                frame_file.close
                # append name of the frame file to the list
                index_file.write(filename+'\n')
            # close index file
            index_file.close()
            # clear frame buffer
            self.clear_frame_buffer()
            return True
        else:
            return False


    def combine_frames_into_movie(self):
        """
        combines all snapshots into a single movie file
        it calls external command (mencoder) to do this
        1) mencoder combines .png files into .h264 rawvideo file
        2) MP4Box puts .h264 file into .mp4 container
        3) deletes .h264 temporaty file
        """
        # run mencoder which combines frames into a movie
        # mpeg4 movie
        command_string = \
                       "mencoder mf://@" + self.index_filename + " " +\
                       "-o "             + self.h264_filename  + " " +\
                       "-mf fps="        + str(self.fps)       + " " +\
                       "-of rawvideo -ovc x264 -x264encopts "        +\
                       "subq=6:partitions=all:me=umh:frameref=5:bframes=0:weight_b" +\
                       ";" +\
                       "MP4Box -fps " + str(self.fps) + " " +\
                       "-new -add " + self.h264_filename + " " + self.movie_filename +\
                       ";" +\
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
    


    def clear_frame_buffer(self):
        "clear self.frames_png list"
        self.frames_png = []
        # update #of recorded frames in GUI
        self.update_number_of_recorded_frames_function(len(self.frames_png))

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

        
    def store_snapshot(self, snapshot):
        """
        takes snapshot of and stores in it in the internal list 
        must be implemented in children classes
        """
        pass


    def make_movie_file(self):
        """
        main function
        must be implemented in children classes
        """
        mfm_params_window = Movie_File_Maker_Params(self)
