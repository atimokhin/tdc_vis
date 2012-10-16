import gtk

from button_label_from_stock import *

class AxesPanel(gtk.Frame):

    def __init__(self,axes,axes_name):
        # local copy of controlled Axes
        self.Axes = axes
        # controlling variables --------------------
        self.x_min=0
        self.x_max=0
        self.y_min=0
        self.y_max=0
        # ==========================================
        # setup GUI elements
        # ==========================================
        # constructor of the base class
        gtk.Frame.__init__(self)
        self.set_label(axes_name)
        # size <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!
        self.set_size_request(160,290)
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!
        # -------------------------------------------
        # Y axis limits 
        # -------------------------------------------
        self.y_min_entry = gtk.Entry()
        self.y_max_entry = gtk.Entry()
        box=gtk.HBox()
        box.set_border_width(2)
        box.pack_start(self.y_min_entry,padding=2)
        box.pack_start(self.y_max_entry,padding=2)
        Y_frame=gtk.Frame('Y')
        Y_frame.set_border_width(5)
        Y_frame.add(box)
        # -------------------------------------------
        # X axis limits 
        # -------------------------------------------
        self.x_min_entry = gtk.Entry()
        self.x_max_entry = gtk.Entry()
        box=gtk.HBox()
        box.set_border_width(2)
        box.pack_start(self.x_min_entry,padding=2)
        box.pack_start(self.x_max_entry,padding=2)
        X_frame=gtk.Frame('X')
        X_frame.set_border_width(5)
        X_frame.add(box)
        # -------------------------------------------
        # REDRAW Button 
        # -------------------------------------------
        self.button_redraw=gtk.Button()
        label_box, label = button_label_from_stock(gtk.STOCK_REFRESH,'Reset Axes Limits')
        self.button_redraw.add( label_box )
        self.button_redraw.set_border_width(5)
        self.button_redraw.modify_bg( gtk.STATE_PRELIGHT, gtk.gdk.color_parse("gray85"))
        self.button_redraw.connect("clicked",  self.axes_reset_limits_callback  )
        # -------------------------------------------
        # Axes Command Entry 
        # -------------------------------------------
        self.axes_command = gtk.Entry()
        box=gtk.HBox()
        box.set_border_width(2)
        box.pack_start(self.axes_command,padding=2)
        AxC_frame=gtk.Frame('Axes Command')
        AxC_frame.set_border_width(5)
        AxC_frame.add(box)
        self.axes_command.connect("activate",  self.axes_command_callback  )
        # -------------------------------------------
        # ===========================================
        # pack everything into a VBox
        vbox=gtk.VBox()
        vbox.pack_start(Y_frame,False)
        vbox.pack_start(X_frame,False)
        vbox.pack_start(self.button_redraw,False)
        vbox.pack_start(AxC_frame,False)
        self.add(vbox)
        # ===========================================
        # set initial values of axes limits
        self.set_xlim_on_panel(self.Axes.get_xlim())
        self.set_ylim_on_panel(self.Axes.get_ylim())
        # Tie panel values to actual axes values
        self.Axes.callbacks.connect('ylim_changed', self.update_ylim_on_panel)
        self.Axes.callbacks.connect('xlim_changed', self.update_xlim_on_panel)
        # ------------------------------------------


    def update_xlim_on_panel(self,ax):
        self.set_xlim_on_panel(self.Axes.get_xlim())

    def update_ylim_on_panel(self,ax):
        self.set_ylim_on_panel(self.Axes.get_ylim())
        
    def set_xlim_on_panel(self,xlim):
        self.x_min_entry.set_text('%g' % xlim[0])
        self.x_max_entry.set_text('%g' % xlim[1])

    def set_ylim_on_panel(self,ylim):
        self.y_min_entry.set_text('%g' % ylim[0])
        self.y_max_entry.set_text('%g' % ylim[1])

    def axes_reset_limits_callback(self,widget,data=None):
        """
        Resets axes limits entered in x/y_min/max_entry widgets
        """
        try:
            self.x_min=float( self.x_min_entry.get_text())
            self.x_max=float( self.x_max_entry.get_text())
            self.y_min=float( self.y_min_entry.get_text())
            self.y_max=float( self.y_max_entry.get_text())
        except ValueError:
            # fire Error dialog window ---------------
            dialog = gtk.Dialog('Error!',
                                None,
                                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
            label = gtk.Label('Axes limits must be numbers!')
            dialog.vbox.pack_start(label)
            label.show()
            dialog.show()
            response = dialog.run()
            dialog.destroy()
        else:
            # change axes limits ---------------------
            self.Axes.set_xlim([self.x_min,self.x_max])
            self.Axes.set_ylim([self.y_min,self.y_max])
        
    def axes_command_callback(self,widget,data=None):
        """
        Executes command entered in axes_command  widget on axes
        """
        command_text=self.axes_command.get_text()
        print '>> Command:\n', command_text
        # if command text is of non-zero length try to execute it
        if len(command_text):
            try:
                command_text = 'self.Axes.'+command_text
                print '>> Evaluation results:\n', eval(command_text), '\n' 
            except:
                # fire Error dialog window ---------------
                dialog = gtk.Dialog('Error!',
                                    None,
                                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                    (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
                label = gtk.Label('Command cannot be executed!')
                dialog.vbox.pack_start(label)
                label.show()
                dialog.show()
                response = dialog.run()
                dialog.destroy()
