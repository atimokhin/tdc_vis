import gtk, gobject

import os
import time

import cStringIO
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

    __frame_filename         = 'frame'
    __index_filename         = 'index.txt'
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
        # initialize main_Window (necessary for notification window)
        self.main_Window=None


    def set_main_window(self,window):
        self.main_Window=window
        
    def set_update_number_of_recorded_frames_function(self,fun):
        self.update_number_of_recorded_frames_function=fun

    def set_movie_filenames(self,filename):
        self.movie_filename = tdc_get_vis_fielname(self.movie_id, filename+".mp4")
        self.h264_filename  = tdc_get_vis_fielname(self.movie_id, filename+".h264")
        
    def set_fps(self,fps):
        self.fps = fps

    def set_keep_frame_files_flag(self,val):
        self.keep_frame_files_flag = val

    def get_number_of_saved_snapshots(self):
        return len(self.frames_png)


    def store_snapshot(self, widget):
        """
        takes snapshot of the widget, transforms it into png format
        and stores in it in the internal list 
        """
        # get pixmap from figure's canvas [it's a widget too] (server buffer)
        x,y,w,h = widget.allocation
        pm=widget.get_snapshot()
        # transform pixmap into a pixbuf (client buffer)
        pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, w, h)
        pb.get_from_drawable(pm, pm.get_colormap(), 0, 0, 0, 0, -1, -1)
        # transform pixbuf into png format  and store it in RAM
        io = cStringIO.StringIO()
        pb.save_to_callback(io.write, 'png')
        self.frames_png.append( io.getvalue() )
        io.close()
        # update #of recorded frames in GUI
        self.update_number_of_recorded_frames_function(len(self.frames_png))


    def make_movie_file(self):
        """
        Pops up parameter window and passes control to it
        """
        mfm_params_window = Movie_File_Maker_Params(self)
        


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
                           self.__frame_filename + '_' + str(idx) + '.png'
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
        



class Movie_File_Maker_Params:
    """
    This class is responsible for the window with
    Movie_File_Maker parameters
    """

    def __init__(self, mfm):
        # store default parameter values
        self.MFM = mfm
        # Main Window -----------------
        self.window=gtk.Window()
        self.window.set_title('Movie File Settings')
        self.window.set_transient_for(self.MFM.main_Window)
        self.window.set_modal(True)
        self.window.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        # Main VBox -------------------
        vbox = gtk.VBox()
        self.window.add(vbox)
        # movie fielname Entry --------
        filename_box = gtk.HBox()
        vbox.pack_start(filename_box, True, True, 10)
        # label
        filename_label = gtk.Label("Movie filename:")
        filename_box.pack_start(filename_label,  False, False, 10)
        filename_label.show()
        # entry
        self.filename_entry = gtk.Entry()
        self.filename_entry.set_text(self.MFM._default_movie_filename)
        self.filename_entry.select_region(0, len(self.filename_entry.get_text()))
        filename_box.pack_start(self.filename_entry,  False, False, 10)
        self.filename_entry.connect("changed", self.filename_callback, self.filename_entry)
        self.filename_entry.show()
        # -----------------------------
        # Keep files Buttons ----------
        keep_files_box = gtk.HBox()
        vbox.pack_start(keep_files_box, True, True, 10)
        # label
        keep_files_label = gtk.Label("Keep movie frames?")
        keep_files_box.pack_start(keep_files_label,  False, False, 10)
        keep_files_label.show()
        # button y
        self.keep_files_button_Y = gtk.RadioButton(None, "Yes")
        keep_files_box.pack_start(self.keep_files_button_Y, False, False, 5)
        self.keep_files_button_Y.show()
        # button no
        self.keep_files_button_N = gtk.RadioButton(self.keep_files_button_Y, "No")
        self.keep_files_button_N.set_active(True)
        keep_files_box.pack_start(self.keep_files_button_N, False, False, 5)
        self.keep_files_button_N.connect("clicked",
                                         self.dont_keep_files_callback,
                                         self.keep_files_button_N)
        self.keep_files_button_N.show()
        # -----------------------------
        # FPS SpinButton -------------
        fps_box = gtk.HBox()
        vbox.pack_start(fps_box, True, True, 10)
        # label
        fps_label = gtk.Label("fps:")
        fps_box.pack_start(fps_label,  False, False, 10)
        fps_label.show()
        # spin button
        adj = gtk.Adjustment(self.MFM._default_fps, 1, 50, 1, 1, 0)
        self.fps_spinner = gtk.SpinButton(adj, 0.0, 0)
        self.fps_spinner_adj=self.fps_spinner.get_adjustment()
        self.fps_spinner_adj.connect("value-changed",
                                     self.fps_callback,
                                     self.fps_spinner_adj)
        fps_box.pack_start(self.fps_spinner,  False, False, 10)
        self.fps_spinner.show()
        # ------------------------------
        # Separator ====================
        separator = gtk.HSeparator()
        vbox.pack_start(separator, True, True, 10)
        # ==============================
        # Frame Buttons ----------------
        frames_button_box = gtk.HBox()
        vbox.pack_start(frames_button_box, True, True, 10)
        # Dump Frames
        dump_frames_button=gtk.Button('Dump Frames')
        frames_button_box.pack_start(dump_frames_button,  True, True, 10)
        dump_frames_button.connect("clicked", self.dump_frames_callback)
        dump_frames_button.show()
        # Clear Frames
        clear_frames_button=gtk.Button('Clear Frames')
        frames_button_box.pack_start(clear_frames_button,  True, True, 10)
        clear_frames_button.connect("clicked", self.clear_frames_callback)
        clear_frames_button.show()
        # ------------------------------
        # Make Movie Button ------------
        movie_button_box = gtk.HBox()
        vbox.pack_start(movie_button_box, True, True, 10)
        make_movie_button=gtk.Button('Make Movie')
        movie_button_box.pack_start(make_movie_button,  True, True, 10)
        make_movie_button.connect("clicked", self.make_movie_callback)
        make_movie_button.show()
        # ------------------------------
        # Separator ====================
        separator = gtk.HSeparator()
        vbox.pack_start(separator, True, True, 10)
        # ==============================
        # Control Buttons --------------
        control_button_box = gtk.HBox()
        vbox.pack_start(control_button_box, True, True, 10)
        # Set Default
        set_default_button=gtk.Button('Set Default')
        control_button_box.pack_start(set_default_button,  False, False, 10)
        set_default_button.connect("clicked",self.set_default_callback)
        set_default_button.show()
        # OK
        ok_button=gtk.Button(stock=gtk.STOCK_OK)
        control_button_box.pack_end(ok_button,  False, False, 10)
        ok_button.connect("clicked", self.close_callback )
        ok_button.show()
        # ------------------------------
        self.window.show_all()


    def filename_callback(self, widget, entry):
        entry_text = entry.get_text()
        self.MFM.set_movie_filenames(entry_text)

    def dont_keep_files_callback(self, widget, button):
        if button.get_active():
            self.MFM.set_keep_frame_files_flag(False)
        else:
            self.MFM.set_keep_frame_files_flag(True)

    def fps_callback(self,widget,adjustment):
        fps = adjustment.get_value()
        self.MFM.set_fps(fps)

    def dump_frames_callback(self,widget):
        notification=self.notification_window('Saving files')
        self.MFM.save_png_snapshots_to_disk()
        notification.destroy()
        
    def clear_frames_callback(self,widget):
        # create notification window
        dialog = gtk.Dialog(title='Confirmation',
                            parent=self.window,
                            flags=0,
                            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                                     gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        label = gtk.Label('Clear Frames?')
        dialog.vbox.pack_start(label)
        label.show()
        # get response
        response = dialog.run()
        dialog.destroy()
        # do clear frames
        if response == gtk.RESPONSE_ACCEPT:
            notification=self.notification_window('Clearing frames')
            self.MFM.clear_frame_buffer()
            # delete frame files -------------
            status=self.MFM.delete_frame_files()
            if not status:
                self.error_window('Have not deleted frame files!')
            # --------------------------------
            notification.destroy()

    def make_movie_callback(self,widget):
        notification=self.notification_window('Making movie')
        self.MFM.save_png_snapshots_to_disk()
        # combine frames into movie file
        status = self.MFM.combine_frames_into_movie()
        if not status:
            self.error_window('Could not combine frames into a movie file!')
        # ------------------------------
        self.MFM.delete_frame_files()
        notification.destroy()


    def set_default_callback(self,widget):
        self.filename_entry.set_text(self.MFM._default_movie_filename)
        self.keep_files_button_N.set_active(True)
        self.fps_spinner_adj.set_value(self.MFM._default_fps)

    def close_callback(self,widget):
        self.window.destroy()
        return True


    def notification_window(self, message):
        notification = gtk.MessageDialog(parent=self.window,
                                         flags=0,
                                         type=gtk.MESSAGE_INFO,
                                         buttons=gtk.BUTTONS_NONE,
                                         message_format=None)
        notification.set_markup(message)
        notification.show()
        while gtk.events_pending():
            gtk.main_iteration()        
        return notification



    def error_window(self,message):
        dialog = gtk.Dialog(title='Error!',
                            parent=self.window,
                            flags=0,
                            buttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        label = gtk.Label(message)
        dialog.vbox.pack_start(label)
        label.show()
        # get response
        response = dialog.run()
        dialog.destroy()
