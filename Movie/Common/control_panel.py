import gtk

from button_label_from_stock import *

class ControlPanel(gtk.Frame):

    def set_flags_to_default_values(self):
        self.quit_flag = False
        self.play_flag = False
        self.go_back_flag      = False
        self.go_forward_flag   = False
        self.set_iframe_flag = False
        self.record_flag = False


    def button_image_box(self, stock_icon): 
        # Create box for xpm and label
        box1 = gtk.HBox(False, 0)
        box1.set_border_width(2)

        # Now on to the image stuff
        image = gtk.Image()
        #imported from button_label_from_stock
        image.set_from_file(xpm_filename)

        # Create a label for the button
        label = gtk.Label(label_text)
        
        # Pack the pixmap and label into the box
        box1.pack_start(image, False, False, 3)
        box1.pack_start(label, False, False, 3)
        
        image.show()
        label.show()
        return box1



    def __init__(self,**kwargs):
 
        self.set_flags_to_default_values()
        
        # constructor of the base class
        gtk.Frame.__init__(self,**kwargs)
        # size <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!
        self.set_size_request(145,245)
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!
        main_box=gtk.VBox()
        main_box.set_border_width(5)
        self.add(main_box)

        #test box
        button_test = gtk.Button('Hello!')
        button_test.connect('clicked', lambda w: gtk.main_quit())
        button_test.show()
        # FRAME SpinButton -------------
        adj = gtk.Adjustment(1, 1, 50, 1, 10, 0)
        self.frame_spinner = gtk.SpinButton(adj, 0.0, 0)
        self.frame_spinner_adj=self.frame_spinner.get_adjustment()
        self.frame_spinner_adj.connect("value-changed", self.set_flag, ('set_iframe_flag',  True))
        
        button_box_frame = gtk.HBox(spacing=5)
        button_box_frame.pack_start(gtk.Label('frame #'))
        button_box_frame.pack_end(self.frame_spinner)
        # ------------------------------

        # FORWARD/BACK ----------------
        self.button_back=gtk.Button()
        img=gtk.Image()
        img.set_from_stock(gtk.STOCK_GO_BACK, gtk.ICON_SIZE_BUTTON)
        self.button_back.add(img)
        self.button_back.modify_bg( gtk.STATE_PRELIGHT, gtk.gdk.color_parse("gray85"))
        self.button_back.connect("pressed",  self.set_flag, ('go_back_flag',  True)  )
        self.button_back.connect("released", self.set_flag, ('go_back_flag',  False) )
        
        self.button_forward=gtk.Button()
        img=gtk.Image()
        img.set_from_stock(gtk.STOCK_GO_FORWARD, gtk.ICON_SIZE_BUTTON)
        self.button_forward.modify_bg( gtk.STATE_PRELIGHT, gtk.gdk.color_parse("gray85"))
        self.button_forward.add(img)
        self.button_forward.connect("pressed",  self.set_flag, ('go_forward_flag',  True)  )
        self.button_forward.connect("released", self.set_flag, ('go_forward_flag',  False) )

        button_box_bf = gtk.HBox(spacing=5)
        button_box_bf.pack_start(self.button_back)
        button_box_bf.pack_end(self.button_forward)
        # ------------------------------

        # STOP/PLAY Button
        self.button_play=gtk.ToggleButton('Play')
        self.button_play.modify_bg( gtk.STATE_ACTIVE, gtk.gdk.color_parse("green1") )
        self.button_play.modify_bg( gtk.STATE_PRELIGHT, gtk.gdk.color_parse("gray85"))

        self.button_play.connect("toggled", self.callback_play)
        # ------------------------------
 
        # RECORD Button ----------------
        self.button_record=gtk.ToggleButton()
        label_box, self.button_record_label = button_label_from_stock(gtk.STOCK_CDROM,'Record')
        self.button_record.add( label_box )
        self.button_record.modify_bg( gtk.STATE_ACTIVE, gtk.gdk.color_parse("red1") )
        self.button_record.modify_bg( gtk.STATE_PRELIGHT, gtk.gdk.color_parse("gray85"))

        self.button_record.connect("toggled", self.callback_record)
        # ------------------------------
        
        # QUIT Button
        self.button_quit=gtk.Button(stock=gtk.STOCK_QUIT)
        self.button_quit.connect("clicked", self.set_flag,('quit_flag', True) )
        self.button_quit.modify_bg( gtk.STATE_PRELIGHT, gtk.gdk.color_parse("gray85"))
        
        # pack all control element into the main box
        main_box.pack_start(button_box_frame, expand=False, padding=5)
        main_box.pack_start(button_box_bf, expand=False, padding=5)
        main_box.pack_start(self.button_play, expand=False, padding=5)
        main_box.pack_start(self.button_record, expand=False, padding=5)
        main_box.pack_end(self.button_quit, expand=False, padding=5)
        main_box.pack_start(button_test, expand = True, padding = 5)



    def set_flag(self,widget,data):
        self.__dict__[data[0]] = data[1]
        return True

    def set_flags(self,widget,data):
        for entry in data:
            self.__dict__[entry[0]] = entry[1]
        return True

    def callback_play(self,widget,data=None):
        if widget.get_active():
            widget.modify_bg( gtk.STATE_PRELIGHT, gtk.gdk.color_parse("green2"))
            widget.set_label('Playing ...')
            self.play_flag=True
        else:
            widget.modify_bg( gtk.STATE_PRELIGHT, gtk.gdk.color_parse("gray85"))
            widget.set_label('Play')
            self.play_flag=False

    def callback_record(self,widget,data=None):
        if widget.get_active():
            widget.modify_bg( gtk.STATE_PRELIGHT, gtk.gdk.color_parse("red2"))
            self.button_record_label.set_text('Recording ...')
            self.record_flag=True
        else:
            widget.modify_bg( gtk.STATE_PRELIGHT, gtk.gdk.color_parse("gray85"))
            self.button_record_label.set_text('Record')
            self.record_flag=False

    def set_frame_number(self, i_frame):
        self.frame_spinner.set_value(i_frame)
        

    def get_frame_number(self):
        return self.frame_spinner.get_value_as_int()

    def set_frame_number_limits(self, i_min=1,i_max=1):
        self.frame_spinner_adj.lower=i_min
        self.frame_spinner_adj.upper=i_max
        self.frame_spinner_adj.emit("changed")



