import gtk

class Coords_Panel_Window:
    """
    This class is responsible for the window with
    Movie_File_Maker parameters
    """

    def __init__(self, movie_frames):
        self.F = movie_frames
        # Main Window -----------------
        self.window=gtk.Window()
        self.window.set_title('Coordinates')
        ## self.window.set_transient_for(self.MFM.main_Window)
        ## self.window.set_modal(True)
        ## self.window.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        # Main VBox -------------------
        vbox = gtk.VBox()
        self.window.add(vbox)
        self.window.set_border_width(5)
        # movie fielname Entry --------
        table = gtk.Table(2, 3, False)
        table.set_col_spacings(10)
        vbox.pack_start(table, True, True, 10)
        # ==============================
        # Show Cells Buttons ----------
        # ==============================
        # label
        use_cell_coords_label = gtk.Label("Use Cell Coordinates ? ")
        use_cell_coords_label.set_alignment(1,.5)
        table.attach(use_cell_coords_label,  0,1,0,1)
        use_cell_coords_label.show()
        # button y
        self.use_cell_coords_button_Y = gtk.RadioButton(None, "Yes")
        table.attach(self.use_cell_coords_button_Y, 1,2,0,1)
        self.use_cell_coords_button_Y.show()
        # button no
        self.use_cell_coords_button_N = gtk.RadioButton(self.use_cell_coords_button_Y, "No")
        self.use_cell_coords_button_N.set_active(True)
        table.attach(self.use_cell_coords_button_N, 2,3,0,1)
        self.use_cell_coords_button_N.connect("clicked",
                                         self.dont_use_cell_coords_callback,
                                         self.use_cell_coords_button_N)
        self.use_cell_coords_button_N.show()
        # -----------------------------
        # ==============================
        # Show Cells Buttons ----------
        # ==============================
        # label
        show_cells_label = gtk.Label("Show Cells ? ")
        show_cells_label.set_alignment(1,.5)
        table.attach(show_cells_label, 0,1,1,2)
        show_cells_label.show()
        # button y
        self.show_cells_button_Y = gtk.RadioButton(None, "Yes")
        table.attach(self.show_cells_button_Y, 1,2,1,2)
        self.show_cells_button_Y.show()
        # button no
        self.show_cells_button_N = gtk.RadioButton(self.show_cells_button_Y, "No")
        self.show_cells_button_N.set_active(True)
        table.attach(self.show_cells_button_N, 2,3,1,2)
        self.show_cells_button_N.connect("clicked",
                                         self.dont_show_cells_callback,
                                         self.show_cells_button_N)
        self.show_cells_button_N.show()
        # -----------------------------
        # Separator ====================
        separator = gtk.HSeparator()
        vbox.pack_start(separator, True, True, 5)
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


    ## def filename_callback(self, widget, entry):
    ##     entry_text = entry.get_text()
    ##     self.MFM.set_movie_filenames(entry_text)

    ## def dont_show_cells_callback(self, widget, button):
    ##     if button.get_active():
    ##         self.MFM.set_keep_frame_files_flag(False)
    ##     else:
    ##         self.MFM.set_keep_frame_files_flag(True)
    def dont_show_cells_callback(self, widget, button):
        if button.get_active():
            print "do not show cells"
        else:
            print "SHOW CELLS"

    def dont_use_cell_coords_callback(self, widget, button):
        if button.get_active():
            print "do not USE cells"
        else:
            print "USE CELLS"

    def set_default_callback(self,widget):
        self.show_cells_button_N.set_active(True)
        self.use_cell_coords_button_N.set_active(True)

    def close_callback(self,widget):
        self.window.destroy()
        return True

