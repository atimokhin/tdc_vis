# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 15:18:52 2014

@author: Alexander
"""
import gtk 

class SelectPanel(gtk.Frame):
    #controls highlighting of select button    
    def set_flags_to_default_values(self):
        self.tracking_flag = True
        self.tracking_changed = False
    
    
    def __init__(self, movie_frame,**kwargs):
        #controls selecting or deselecting       
        self.selecting = True        
        self.MovieFrame = movie_frame
        self.data = self.MovieFrame.seq_plotter[0].data
        self.recent = []
        #used for conversions
        x_scale = self.MovieFrame.ax[0].get_xlim()
        self.x_scale = x_scale[1]-x_scale[0]
        y_scale = self.MovieFrame.ax[0].get_ylim()
        self.y_scale = y_scale[1]
        self.names = {'Positrons': 0, 'Electrons': 1, 'Pairs' : 2, 'Protons': 3}
        
        self.set_flags_to_default_values()
        gtk.Frame.__init__(self, **kwargs)
        self.set_size_request(25, 150)
        
        #main box for packing everything        
        main_box = gtk.VBox()
        main_box.set_border_width(5)
        self.add(main_box)
#------------------------------------------------------------------------------
#                                TRACKING BUTTON
#------------------------------------------------------------------------------
        #box for tracking toggle
        track_box = gtk.HBox()
        main_box.pack_start(track_box)
        
        #image
        self.track_image = gtk.Image()
        self.track_image.set_from_stock(gtk.STOCK_NO, 1)
        track_box.pack_end(self.track_image)
        
        #Tracking On/Off
        track_button = gtk.CheckButton('Tracking')
        track_button.set_active(False)
        track_button.connect('clicked', self.track_callback)
        track_box.pack_start(track_button, expand = True, padding = 5)
        
        #Separator
        separator = gtk.HSeparator()
        main_box.pack_start(separator)
        
#------------------------------------------------------------------------------
#                               Marker Size
#------------------------------------------------------------------------------
        # Marker Spin Button
        adj = gtk.Adjustment(20, 1, 100, 1, 10, 0)
        marker_spinner = gtk.SpinButton(adj, 0.0, 0)
        marker_spinner_adj=marker_spinner.get_adjustment()
        marker_spinner_adj.connect("value-changed", self.marker_callback)
        
        marker_box= gtk.HBox(spacing=5)
        #pack label and spinner
        marker_box.pack_start(gtk.Label('marker size'))
        marker_box.pack_end(marker_spinner)
        main_box.pack_start(marker_box)
#------------------------------------------------------------------------------
#                                SELECT/DESELECT BUTTONS
#------------------------------------------------------------------------------
        
        #Select/Deselect
        self.select_button = gtk.RadioButton(None, 'Select')
        self.select_button.connect('toggled', self.select_button_callback)
        self.deselect_button = gtk.RadioButton(self.select_button, 'Deselect')
        self.select_button.set_sensitive(False)
        self.deselect_button.set_sensitive(False)        
        main_box.pack_start(self.select_button)
        main_box.pack_start(self.deselect_button)
#------------------------------------------------------------------------------
#                                DIRECT ENTRY BUTTON
#------------------------------------------------------------------------------
        
        #Button for direct entry
        self.entry_button = gtk.Button('Direct Entry')
        self.entry_button.connect('clicked', self.entry_check)
        self.entry_button.set_sensitive(False)
        main_box.pack_start(self.entry_button)
        
        #Second Separator
        separator = gtk.HSeparator()
        main_box.pack_start(separator)
#------------------------------------------------------------------------------
#                           SAVE AND CLEAR ALL BUTTONS AND BOX
#------------------------------------------------------------------------------
        #box for save and clear buttons
        data_box = gtk.HBox()
        main_box.pack_start(data_box)
        
        #Save Button
        save_button = gtk.Button('Save')
        save_button.connect('clicked', self.save_check)
        data_box.pack_end(save_button)
        #Clear Button
        clear_button= gtk.Button('Clear All')
        clear_button.connect('clicked', self.clear_check)
        data_box.pack_end(clear_button)
        
#------------------------------------------------------------------------------
#                                SAVE INFORMATION DIALOG
#------------------------------------------------------------------------------
        #Save Dialog
        self.save_dialog = gtk.Dialog('Save Particles')
        self.save_dialog.hide()
        #Filename label
        self.filename_label = gtk.Label('Filename')
        self.save_dialog.vbox.pack_start(self.filename_label)
        #Filename
        self.filename_entry = gtk.Entry()
        self.filename_entry.connect('changed', self.filename_callback)
        self.save_dialog.vbox.pack_start(self.filename_entry)
        #Cancel Button
        self.save_cancel= gtk.Button('Cancel')
        self.save_cancel.connect('clicked', lambda w: self.save_dialog.destroy)
        self.save_dialog.action_area.pack_start(self.save_cancel)
        #Save Button
        self.save = gtk.Button('Save')
        self.save.connect('clicked', self.save_callback)
        self.save_dialog.action_area.pack_start(self.save)
#------------------------------------------------------------------------------
#                                CLEAR CONFIRMATION DIALOG
#------------------------------------------------------------------------------
                
        #Clear Dialog
        self.clear_dialog = gtk.MessageDialog(flags = gtk.DIALOG_MODAL,type = gtk.MESSAGE_WARNING)
        self.clear_dialog.set_markup('Are you sure you want to clear all selected particles?')        
        self.clear_yes = gtk.Button('Yes')
        self.clear_yes.connect('clicked', self.clear_callback)
        self.clear_yes.connect('clicked', self.clear_hide)
        self.clear_dialog.action_area.pack_start(self.clear_yes)
        self.clear_no = gtk.Button('No')
        self.clear_no.connect('clicked', self.clear_hide)
        self.clear_dialog.action_area.pack_start(self.clear_no)
        
        #Cleared Dialog
        self.cleared_dialog = gtk.MessageDialog(flags = gtk.DIALOG_MODAL, type = gtk.MESSAGE_INFO)
        self.cleared_dialog.set_markup('Selected particles cleared')
        self.cleared_ok = gtk.Button("OK")
        self.cleared_ok.connect('clicked', self.cleared_callback)
        self.cleared_dialog.action_area.pack_start(self.cleared_ok)
        
    #Controls sensitivity when tracking option is on/off
    def track_callback(self, widget):
        state = widget.get_active()
        if state:
            self.tracking_flag = True
            self.pick_id = self.MovieFrame.canvas.mpl_connect('pick_event', self.pick_callback)
            self.track_image.set_from_stock(gtk.STOCK_YES, 1)
        else:
            self.tracking_flag = False
            self.track_image.set_from_stock(gtk.STOCK_NO, 1)
            self.MovieFrame.canvas.mpl_disconnect(self.pick_id)
        self.select_button.set_sensitive(state)
        self.deselect_button.set_sensitive(state)
        self.entry_button.set_sensitive(state)
#------------------------------------------------------------------------------
#                           DIRECT ENTRY DIALOG
#------ ------------------------------------------------------------------------
    #Shows entry box
    def entry_check(self, widget):

        #Entry Dialog
        entry_dialog = gtk.Dialog('Direct Entry')
        entry_dialog.show()
        
        #Particle Type Label
        particle_type_label = gtk.Label('Particle Type')
        entry_dialog.vbox.pack_start(particle_type_label)
        particle_type_label.show()
        
        #Particle Type Menu
        entry_menu = gtk.Combo()
        names = ['Positrons', 'Electrons', 'Pairs', 'Protons']
        entry_menu.set_popdown_strings(names)
        entry_dialog.vbox.pack_start(entry_menu)
        entry_menu.show()
        
        #idts box
        idts_box = gtk.VBox()
        idts_box.show()
        idts_entry = gtk.Entry()
        idts_entry.show()
        idts_box.pack_end(idts_entry)
        idts_label = gtk.Label('idts')
        idts_label.show()
        idts_box.pack_start(idts_label)
        entry_dialog.action_area.pack_start(idts_box)
        
        #id box
        id_box = gtk.VBox()
        id_box.show()
        id_entry = gtk.Entry()
        id_entry.show()
        id_box.pack_end(id_entry)
        id_label = gtk.Label('id')
        id_label.show()
        id_box.pack_start(id_label)
        entry_dialog.action_area.pack_start(id_box)
        id_entry.connect('activate', self.entry_callback, idts_entry, entry_menu)
    #Selects particle entered into direct entry
    def entry_callback(self, widget, idts_entry, entry_menu):
        idts = int(idts_entry.get_text())
        ID = int(widget.get_text())
        particle_type = self.names[entry_menu.entry.get_text()]
        particle = self.data[particle_type].index_search(idts, ID)
        if self.selecting:
            self.data[particle_type].select_particle(particle[2])
            self.fix_axes()
        else:
            self.data[particle_type].deselect_particle(particle[0], particle[1])
            self.fix_axes()
        self.MovieFrame.redraw_flag=True
        
    #Finds nearest particle for pick event
    def pick_callback(self, event):
        x_plot = event.mouseevent.xdata
        y_plot = event.mouseevent.ydata
        
        #deals with duplication problem
        if (x_plot, y_plot) in self.recent:
            return
        self.recent.append((x_plot, y_plot))
        print "-------------------PICK---------EVENT------------"
        print "called point with coordinates \n " + str((x_plot, y_plot))
        bound = len(self.MovieFrame.seq_plotter[0].data)
        possible= []
        particle_type = None
        
        #generates one of each type of particle closest to pick_event
        for i in range(0,bound):
            particle = self.data[i].proximity_search(x_plot, y_plot, self.x_scale, self.y_scale, self.selecting)
            possible.append(particle)
       
        mindist = 2**31
        particle=None
        
        #finds closest particle 
        for i in range(0,len(possible)):
            if possible[i][0]<mindist:
                mindist = possible[i][0]
                particle = possible[i]
                particle_type=i
        try:
            print "picked %s with idts %i ID %i" %(self.data[particle_type].name, particle[2], particle[3])
        except TypeError:
            print "No particles to deselect!"
        #Button Functionality
        if self.selecting:
            self.data[particle_type].select_particle(particle[1])
            self.fix_axes()
        else:
            self.data[particle_type].deselect_particle(particle[2], particle[3])
            self.fix_axes()
        self.MovieFrame.redraw_flag=True
    #Adjusts marker size
    def marker_callback(self,widget):
        marker_size = widget.get_value()
        for i in range(0,len(self.MovieFrame.seq_plotter)):
            self.MovieFrame.seq_plotter[i].resize_marker(self.MovieFrame.ax[0], marker_size)
    #Clears recent list when switching between select and deselect    
    def select_button_callback(self,widget):
        self.selecting = widget.get_active()
        self.recent = []
    def save_check(self, widget):
        self.save_dialog.show()
        self.save_cancel.show()
        self.filename_entry.show()
        self.filename_label.show()
        self.save.show()
    #Save particles
    def filename_callback(self, widget):
        self.filename = widget.get_text()
    def save_callback(self, widget):
        if len(self.filename)>0:
            for i in range(0,len(self.data)):
                self.data[i].save_particles(self.filename)
        else:
            print "Invalid filename!"
    #Shows confirmation
    def clear_check(self, event):
        self.clear_dialog.show()
        self.clear_yes.show()
        self.clear_no.show()  
    #Hides confirmation
    def clear_hide(self, event):
        self.clear_dialog.hide()
        self.clear_yes.hide()
        self.clear_no.hide()
    #Clears particles
    def clear_callback(self, event):
        self.recent = []
        for i in range(0,len(self.data)):
            self.data[i].clear_particles()
        self.fix_axes()
        self.MovieFrame.redraw_flag=True
        self.cleared_dialog.show()
        self.cleared_ok.show()
    #hides dialog after cleared
    def cleared_callback(self, widget):
        self.cleared_dialog.hide()
        self.cleared_ok.hide()
    #Preserves axes scale when clearing
    def fix_axes(self):
        for i in range(0,len(self.MovieFrame.ax)):
            x_scale = self.MovieFrame.ax[i].get_xlim()
            y_scale = self.MovieFrame.ax[i].get_ylim()
            self.MovieFrame.ax[i].cla()            
            self.MovieFrame.ax[i].set_xlim(x_scale[0], x_scale[1])
            self.MovieFrame.ax[i].set_ylim(y_scale[0], y_scale[1])
