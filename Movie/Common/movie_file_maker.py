import os
import re
import glob
import subprocess

from Auxiliary import tdc_Filenames

class Movie_File_Maker:
    """
    Base class for making movie file
    
    This class only provides methods for: 
    - combining already existing frame files into a movie:
       (all files listed in the index file) 
    - deleting frame and index files
    - setting file names, fps, flags

    Methods for *making frame files* (saving them to disk)
    must be provided in child classes!

    --------
    Members:
    --------
    movie_filename
       name of the created movie file
    fps
       fps of created movie file
    keep_frame_files_flag
       whether to keep png frame files after creating movie
       <False>
    """

    __default_frame_filename_format = 'frame_%05d.png'
    __default_index_filename        = 'index.txt'
        
    _default_movie_file_basename    = 'animation'

    def __init__(self, 
                 movie_id, 
                 fps, 
                 keep_frame_files=True, 
                 movie_file_basename=None,
                 frame_filename_format=None):
        """
        movie_id  -- subdirectorty whewre movie files will be stored
        fps       -- fps of created movie
        ---------
        Options
        ---------
        keep_frame_files
           <True>             whether to keep [.png] frame files 
        movie_file_basename
           <None>
        frame_filename_format
           <None>
        """
        # FPS
        self.fps = fps
        # movie_id
        self.movie_id = movie_id
        # directory where image and movie files will be saved
        self.movie_dir_name = tdc_Filenames.get_full_vis_filename(movie_id,'')
        # index filename
        self.index_filename = \
          tdc_Filenames.get_full_vis_filename(self.movie_id, self.__default_index_filename)
        # frame filename format
        self.frame_filename_format = \
          self.__default_frame_filename_format if frame_filename_format is None else frame_filename_format
        # movie filenames
        if movie_file_basename is None:
            movie_file_basename = self._default_movie_file_basename
        self.set_movie_filenames(movie_file_basename)
        # keep_frame_files_flag
        self.set_keep_frame_files_flag(keep_frame_files)
        # frame counter
        self.i_saved_frame = 0
        # index_file
        self.index_file = None

    def setup_directory(self):
        """
        if directory does not exist - create it
        """
        if not os.path.exists(self.movie_dir_name):
            os.makedirs(self.movie_dir_name)
                
    def open_index_file(self):
        # open index file
        self.index_file = open(self.index_filename, 'w')
        # set saved frames counter to 0
        self.i_saved_frame = 0

    def add_filename_to_index_file(self, filename):
        # append name of the frame file to the list
        self.index_file.write(filename+'\n')
        # increment frame counter
        self.i_saved_frame += 1

    def close_index_file(self):
        self.index_file.close()

    def get_frame_filename(self,idx):
        return os.path.join(self.movie_dir_name, self.frame_filename_format % idx)

    def get_number_of_saved_frames(self):
        return self.i_saved_frame

    def set_movie_filenames(self,filename_base):
        self.movie_filename = tdc_Filenames.get_full_vis_filename(self.movie_id, filename_base+".mp4")
        self.h264_filename  = tdc_Filenames.get_full_vis_filename(self.movie_id, filename_base+".h264")

    def set_fps(self,fps):
        self.fps = fps

    def set_keep_frame_files_flag(self,val):
        self.keep_frame_files_flag = val
    
    def combine_frames_into_movie(self):
        """
        combines all snapshots into a single movie file
        *all parameters must be already set*
        it calls external command (mencoder) to do this
        1) mencoder combines .png files into .h264 raw video file
        2) MP4Box puts .h264 file into .mp4 container
        3) deletes .h264 temporaty file
        """
        # [shifruemsya na klastere] ---
        import os
        # my_host = os.environ.get('MY_HOST','nohost')
        # # mencoder command [shifruemsya na klastere]
        # encoder_command = 'combine.exe' if my_host=='henyey' else 'mencoder'        
        # -----------------------------
        # run mencoder which combines frames into a movie
                       # "bitrate=1500:subq=5:frameref=3:bframes=0:threads=auto" 
        # mpeg4 movie
        # command_string = \
        #                encoder_command + " mf://@" + self.index_filename + " " +\
        #                "-o "             + self.h264_filename  + " " +\
        #                "-mf fps="        + str(self.fps)       + " " +\
        #                "-of rawvideo -ovc x264 -x264encopts "        +\
        #                "bitrate=1500:subq=5:frameref=3:bframes=3:threads=auto" +\
        #                "; " +\
        #                "MP4Box -fps " + str(self.fps) + " " +\
        #                "-new -add " + self.h264_filename + " " + self.movie_filename +\
        #                "; " +\
        #                "rm -f " + self.h264_filename

        encoder_command = 'ffmpeg'
        command_string = \
            "rm -f %s; " % self.movie_filename +\
            encoder_command + " -r %d " % self.fps +\
            "-i %s " % os.path.join(self.movie_dir_name, self.frame_filename_format ) +\
            "-vcodec libx264 -x264opts keyint=%d " % self.fps +\
            self.movie_filename

        p = subprocess.Popen(command_string, 
                             shell=True,
                             stdin  = subprocess.PIPE,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE)
        # print stdout of mencoder command
        for i in p.stdout:
            print i
        status = p.wait()
        # print summary of the created movie
        print '\nMovie file: %s \n' % self.movie_filename
        print '\nMovie file properties: fps = %d, frames = %d \n' % (self.fps, self.get_number_of_saved_frames())
        return not status
    
    def delete_frame_files(self, force_delete=False):
        """
        Delete index and frame files 
        *only if self.keep_frame_files_flag is False*

        returns True if any files have been deleted
        """
        if not self.keep_frame_files_flag or force_delete:
            # wildcard for framefiles
            framefile_wildcard = re.sub(r'%.*\.','*.',self.frame_filename_format)
            # list of files to be deleted
            file_list = glob.glob(self.movie_dir_name + framefile_wildcard) 
            file_list.extend( glob.glob( self.index_filename ) )
            status= ( len(file_list)>0 )
            # delete files
            try:
                for f in file_list:
                    os.remove(f)
            except OSError:
                status=False
            return status
        else:
            return False
