import gtk

from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg 

from button_label_from_stock            import *


class NavigationToolbar(NavigationToolbar2GTKAgg):
    
    def __init__(self, window, movie_frames, movie_file_maker):
        # set MPL NavigationToolbar
        NavigationToolbar2GTKAgg.__init__(self, movie_frames.canvas, window)
        # ===================================
        # movie file maker
        # ===================================
        self.mfm = movie_file_maker
        self.mfm.set_update_number_of_recorded_frames_function(self.update_saved_frames_numer)
        # Make Movie Button -----------------
        self.button_make_movie=gtk.ToolButton(gtk.STOCK_CDROM)
        self.button_make_movie.set_tooltip_text("Make movie file")
        # callback
        self.button_make_movie.connect("clicked",self.make_movie_callback)
        # pack button into tollbar
        self.insert(gtk.SeparatorToolItem(),8)
        self.insert(self.button_make_movie,9)
        # -----------------------------------
        # number of saved frames ------------
        self.saved_frames_label=gtk.Label('0')
        self.saved_frames_label.set_width_chars(4)
        # hbox with labels
        hbox=gtk.HBox()
        hbox.pack_start(gtk.Label('recorded:'),False,padding=3)
        hbox.pack_start(self.saved_frames_label,False)
        # tool item -- wrapper for hbox
        toolitem=gtk.ToolItem()
        toolitem.add(hbox)
        # pack them into tollbar
        self.insert(toolitem,10)
        self.insert(gtk.SeparatorToolItem(),11)       
        # -----------------------------------
        
    def update_saved_frames_numer(self, n):
        self.saved_frames_label.set_text(str(n))
    def make_movie_callback(self,widget,data=None):
        self.mfm.make_movie_file()
        
