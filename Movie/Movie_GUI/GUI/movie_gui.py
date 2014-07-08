import gtk

from axes_setup         import AxesSetupPanel
from display_panel      import DisplayPanel
from control_panel      import ControlPanel
from navigation_toolbar import NavigationToolbar

from button_label_from_stock import *

class MovieGUI(gtk.Window):
    """
    GTK Window with movie frame and control elements

    Members:
    
    canvas  -- MPL canvas
    ap      -- Axis panel
    dp      -- Display panel
    cp      -- Control panel
    toolbar -- Toolbar
    """

    def make_control_box(self):
        "make VBox with various control panels"
        # define various control panels
        self.ap = AxesSetupPanel(self.MovieFrames)
        self.dp = DisplayPanel()
        self.cp = ControlPanel()
        # put all panel into a *VBox
        ctrl_box=gtk.VBox()
        ctrl_box.set_border_width(3)
        ctrl_box.pack_start(self.dp,False,False,5)
        ctrl_box.pack_start(self.ap,False,False,5)
        ctrl_box.pack_end(self.cp,False,False,5)
        # return resulting VBox
        return ctrl_box        


    def __init__(self,
                 movie_frames,
                 movie_file_maker,
                 *args,**kwargs):
        """
        canvas should set size request before
        """
        self.MovieFrames = movie_frames
        # initialize base class Window
        gtk.Window.__init__(self,*args,**kwargs)
        # set main window
        movie_frames.set_main_window(self)
        # set main window
        movie_file_maker.set_main_window(self)

        # set canvas
        self.canvas  = movie_frames.canvas
        # set NavigationToolbar
        self.toolbar = NavigationToolbar(self, self.MovieFrames, movie_file_maker)
        
        # **********************************
        # Construct GUI
        # ********************************** 
        # put canvas into a frame = |canvas|
        canvas_frame = gtk.AspectFrame(xalign=0, yalign=0)
        canvas_frame.add(self.canvas)
        canvas_frame.set_border_width(3)
        # make |control box|
        ctrl_box = self.make_control_box()
        # put |canvas| and |control box| into an *HBox
        hbox = gtk.HBox()
        hbox.pack_start(canvas_frame,True,True)
        hbox.pack_start(ctrl_box,False)
        # main *VBox with |canvas|+|control box| and |navigation toolbar|
        vbox = gtk.VBox()
        vbox.pack_start(hbox,True,True,0)
        vbox.pack_start(self.toolbar,False,False,0)
        # add *VBox to the window
        self.add(vbox)
        self.connect("destroy", lambda x: gtk.main_quit())
