import gtk

from button_label_from_stock import *
from axes_panel              import *

from ATvis.Common_Data_Plot import AT_Data_Plotter

from Common_Data_Plot import tdc_Data_vs_X_Plotter
from Movie            import MovieFrames__Axes


class AxesSetupPanel(gtk.Frame):

    def __init__(self, movie_frames):
        # constructor of the base class
        gtk.Frame.__init__(self)
        self.F = movie_frames
        # size <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!
        self.set_size_request(145,50)
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!
        main_box=gtk.VBox()
        main_box.set_border_width(3)
        self.add(main_box)
        # ------------------------------------------
        # Axes setup Button: add only if Movie Frames 
        #                    have adjustable axes
        # ------------------------------------------
        if isinstance(self.F, MovieFrames__Axes):
            self.button_setup_axes=gtk.ToggleButton()
            label_box, self.button_setup_axes_label = \
                button_label_from_stock(gtk.STOCK_PAGE_SETUP,'Axes')
            self.button_setup_axes.add( label_box )
            self.button_setup_axes.modify_bg( gtk.STATE_ACTIVE, gtk.gdk.color_parse("yellow") )
            self.button_setup_axes.modify_bg( gtk.STATE_PRELIGHT, gtk.gdk.color_parse("gray85"))
            #pack to main_box
            main_box.pack_start(self.button_setup_axes, expand=False, padding=5)
            self.button_setup_axes.connect("toggled", self.axes_setup_window)

    def axes_setup_window(self,widget,data=None):
        """
        Start/Stop Axes_Setup_Window 
        """
        if widget.get_active():
            widget.modify_bg( gtk.STATE_PRELIGHT, gtk.gdk.color_parse("yellow2"))
            self.button_setup_axes_label.set_text('Axes ...')
            self.F.axes_setup_panel(self)
        else:
            widget.modify_bg( gtk.STATE_PRELIGHT, gtk.gdk.color_parse("gray85"))
            self.button_setup_axes_label.set_text('Axes')
            self.F.axes_setup_window.close_window()

    def notify_window_closed(self):
        """
        deactivate button when Axes_Setup_Window is closed
        """
        self.button_setup_axes.set_active(False)
        


class Axes_Setup_Window:
    """
    This class is responsible for the window with Axes setup
    """
    
    def __init__(self, movie_frames, plotter_list, axes_list, parent_widget):
        # -----------------------------
        # parent widget - i.e the button which starts this window
        # need to notify it when the window is closed
        self.ParentWidget = parent_widget
        # MovieFrames - the whole thing with all panels
        self.MovieFrames = movie_frames 
        # list of plotters
        if not isinstance( plotter_list, (tuple,list)):
            plotter_list=(plotter_list,)
        self.Plotters = plotter_list
        # list of axes
        if not isinstance( axes_list, (tuple,list)):
            axes_list=(axes_list,)
        self.Axes = axes_list
        # check that they have the same dimension
        if len(self.Plotters) != len(self.Axes):
            raise Exception, 'Plotters and Axes lists have different lengths'
        # Main Window =================
        self.window=gtk.Window()
        self.window.set_title('Coordinates')
        self.window.set_transient_for(self.MovieFrames.main_Window)
        self.window.set_destroy_with_parent(True)
        self.window.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        # Main VBox -------------------
        vbox = gtk.VBox()
        self.window.add(vbox)
        self.window.set_border_width(5)
        # setup lists
        self.AP=[]
        self.use_cell_coords_button_Y=[]
        self.use_cell_coords_button_N=[]
        self.show_cells_button_Y=[]
        self.show_cells_button_N=[]
        # -------------------------------------
        # for each plotter setup control panels
        # -------------------------------------
        for i,plotter in enumerate(self.Plotters):
            # ===============================================
            # Axes panel only plotters supporting it
            # ===============================================
            if isinstance(plotter, AT_Data_Plotter):
                # -----------------------------
                # Axes Panel 
                # -----------------------------
                self.AP.append(AxesPanel(self.Axes[i],'Panel %i' % i))
                vbox.pack_start(self.AP[i], False, False, 5)
                # Table with checkboxes <<<<<<<
                table = gtk.Table(2, 3, False)
                table.set_col_spacings(10)
                vbox.pack_start(table, True, True, 1)
                # ===============================================
                # Cell coordinates only for plotters supporting it
                # ===============================================
                if isinstance(plotter, tdc_Data_vs_X_Plotter):
                    # -----------------------------
                    # Use Cell Coordinates Buttons 
                    # -----------------------------
                    # label
                    use_cell_coords_label = gtk.Label("Use Cell Coordinates ? ")
                    use_cell_coords_label.set_alignment(1,.5)
                    table.attach(use_cell_coords_label,  0,1,0,1)
                    use_cell_coords_label.show()
                    # button Yes
                    self.use_cell_coords_button_Y.append( gtk.RadioButton(None, "Yes") )
                    table.attach(self.use_cell_coords_button_Y[i], 1,2,0,1)
                    self.use_cell_coords_button_Y[i].show()
                    # button No
                    self.use_cell_coords_button_N.append( gtk.RadioButton(self.use_cell_coords_button_Y[i], "No") )
                    self.use_cell_coords_button_N[i].set_active(not plotter.use_cell_coordinates_flag)
                    table.attach(self.use_cell_coords_button_N[i], 2,3,0,1)
                    self.use_cell_coords_button_N[i].connect("clicked",
                                                             self.dont_use_cell_coords_callback,
                                                             (self.use_cell_coords_button_N[i], i) )
                    self.use_cell_coords_button_N[i].show()
                    # -----------------------------
                    # Show Cells Buttons 
                    # -----------------------------
                    # label
                    show_cells_label = gtk.Label("Show Cells ? ")
                    show_cells_label.set_alignment(1,.5)
                    table.attach(show_cells_label, 0,1,1,2)
                    show_cells_label.show()
                    # button Yes
                    self.show_cells_button_Y.append( gtk.RadioButton(None, "Yes") )
                    table.attach(self.show_cells_button_Y[i], 1,2,1,2)
                    self.show_cells_button_Y[i].show()
                    # button No
                    self.show_cells_button_N.append( gtk.RadioButton(self.show_cells_button_Y[i], "No") )
                    self.show_cells_button_N[i].set_active(not plotter.show_cells_flag)
                    table.attach(self.show_cells_button_N[i], 2,3,1,2)
                    self.show_cells_button_N[i].connect("clicked",
                                                        self.dont_show_cells_callback,
                                                        (self.show_cells_button_N[i], i) )
                    self.show_cells_button_N[i].show()
        # -----------------------------
        # Separator
        separator = gtk.HSeparator()
        vbox.pack_start(separator, True, True, 10)
        # ==============================
        # Control Buttons :  "Set Default" and "OK"
        # ==============================
        control_button_box = gtk.HBox()
        vbox.pack_start(control_button_box, True, True, 5)
        # Set Default - sets Cell Options to default
        set_default_button=gtk.Button('Set Default')
        control_button_box.pack_start(set_default_button,  False, False, 10)
        set_default_button.connect("clicked",self.set_default_callback,len(self.Plotters))
        set_default_button.show()
        # OK
        ok_button=gtk.Button(stock=gtk.STOCK_OK)
        control_button_box.pack_end(ok_button,  False, False, 10)
        ok_button.connect("clicked", self.close_callback )
        ok_button.show()
        # ------------------------------
        self.window.show_all()

    def close_window(self):
        self.window.destroy()

    def set_default_callback(self,widget,n):
        # set cell buttons to default position
        for b1,b2 in zip(self.show_cells_button_N,self.use_cell_coords_button_N):
            b1.set_active(True)
            b2.set_active(True)

    def close_callback(self,widget):
        self.close_window()
        self.ParentWidget.notify_window_closed()
        return True

    def dont_show_cells_callback(self, widget, callback_data):
        button, i = callback_data
        if button.get_active():
            self.Plotters[i].show_cells_off()
        else:
            self.Plotters[i].show_cells_on()
        self.MovieFrames.redraw_flag=True

    def dont_use_cell_coords_callback(self, widget, callback_data):
        button, i = callback_data
        if button.get_active():
            self.Plotters[i].to_x_coordinates(self.Axes[i])
        else:
            self.Plotters[i].to_cell_coordinates(self.Axes[i])
        self.MovieFrames.redraw_flag=True
