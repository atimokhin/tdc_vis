# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 15:18:52 2014

@author: Alexander
"""
import gtk
import pprint 

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
        self.x_scale = self.MovieFrame.ax[0].get_xlim()
        self.x_scale = self.x_scale[1]-self.x_scale[0]
        self.y_scale = self.MovieFrame.ax[0].get_ylim()
        self.y_scale = self.y_scale[1]
        self.names = {'Positrons': 0, 'Electrons': 1, 'Pairs' : 2, 'Protons': 3}
        
        self.MovieFrame = movie_frame
        self.set_flags_to_default_values()
        gtk.Frame.__init__(self, **kwargs)
        self.set_size_request(25, 120)
        
        #main box for packing everything        
        main_box = gtk.VBox()
        main_box.set_border_width(5)
        self.add(main_box)
        
        #box for tracking toggle
        track_box = gtk.HBox()
        main_box.pack_start(track_box)
        
        #image
        self.track_image = gtk.Image()
        self.track_image.set_from_stock(gtk.STOCK_NO, 1)
        track_box.pack_end(self.track_image)
        
        #Tracking On/Off
        self.track_button = gtk.CheckButton('Tracking')
        self.track_button.set_active(False)
        self.track_button.connect('clicked', self.set_flag)
        track_box.pack_start(self.track_button, expand = True, padding = 5)
        
        #Separator
        separator = gtk.HSeparator()
        main_box.pack_start(separator)
        
#------------------------------------------------------------------------------
#                               BUTTON FUNCTIONALITY
#------------------------------------------------------------------------------
        
        #Select/Deselect
        self.select_button = gtk.RadioButton(None, 'Select')
        self.select_button.connect('toggled', self.select_button_callback)
        self.deselect_button = gtk.RadioButton(self.select_button, 'Deselect')
        self.select_button.set_sensitive(False)
        self.deselect_button.set_sensitive(False)        
        main_box.pack_start(self.select_button)
        main_box.pack_start(self.deselect_button)
        
        #Button for direct entry
        self.entry_button = gtk.Button('Direct Entry')
        self.entry_button.connect('clicked', self.entry_show)
        main_box.pack_start(self.entry_button)
        
        #Second Separator
        separator = gtk.HSeparator()
        main_box.pack_start(separator)
        
        #Clear Button
        self.clear_button= gtk.Button('Clear All')
        self.clear_button.connect('clicked', self.clear_check)
        main_box.pack_end(self.clear_button)
#------------------------------------------------------------------------------
#                           DIRECT ENTRY FUNCTIONALITY
#------------------------------------------------------------------------------
        #Entry Dialog
        self.entry_dialog = gtk.Dialog('Direct Entry')
        
        #Particle Type Label
        self.particle_type_label = gtk.Label('Particle Type')
        self.entry_dialog.vbox.pack_start(self.particle_type_label)
        
        #Particle Type Menu
        self.entry_menu = gtk.Combo()
        names = ['Positrons', 'Electrons', 'Pairs', 'Protons']
        self.entry_menu.set_popdown_strings(names)
        self.entry_dialog.vbox.pack_start(self.entry_menu)
        
        #idts box
        self.idts_box = gtk.VBox()
        self.idts_entry = gtk.Entry()
        self.idts_box.pack_end(self.idts_entry)
        self.idts_label = gtk.Label('idts')
        self.idts_box.pack_start(self.idts_label)
        self.entry_dialog.action_area.pack_start(self.idts_box)
        
        #id box
        self.id_box = gtk.VBox()
        self.id_entry = gtk.Entry()
        self.id_box.pack_end(self.id_entry)
        self.id_label = gtk.Label('id')
        self.id_box.pack_start(self.id_label)
        self.entry_dialog.action_area.pack_start(self.id_box)
        self.id_entry.connect('activate', self.entry_callback)
                
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
        
#        #Key Press Test
#        self.MovieFrame.canvas.mpl_connect('figure_enter_event', self.key_press_callback)
#        
#    def key_press_callback(self,event):
#        print "key_press_callback called"
#        for i in range(0,len(self.MovieFrame.ax)):
#            self.MovieFrame.ax[i].cla()
#        print "MovieFrame axes cleared"
#        self.MovieFrame.redraw_flag = True
        
    def set_flag(self, widget):
        state = self.track_button.get_active()
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
    
    def entry_show(self, widget):
        self.entry_dialog.show()
        self.particle_type_label.show()
        self.entry_menu.show()
        self.id_label.show()
        self.id_entry.show()
        self.idts_label.show()
        self.idts_entry.show()
        self.id_box.show()
        self.idts_box.show()
    
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
            self.data[particle_type].deselect_particle(particle[2])
            self.fix_axes()
        self.MovieFrame.redraw_flag=True
        
    def entry_callback(self, event):
        idts = int(self.idts_entry.get_text())
        ID = int(self.id_entry.get_text())
        particle_type = self.names[self.entry_menu.entry.get_text()]
        particle = self.data[particle_type].index_search(idts, ID)
        if self.selecting:
            self.data[particle_type].select_particle(particle[2])
            self.fix_axes()
        else:
            self.data[particle_type].deselect_particle(particle[0], particle[1])
            self.fix_axes()
        self.MovieFrame.redraw_flag=True
        
        
    def select_button_callback(self,event):
        self.selecting = self.select_button.get_active()
        self.recent = []
    def clear_check(self, event):
        self.clear_dialog.show()
        self.clear_yes.show()
        self.clear_no.show()    
    def clear_hide(self, event):
        self.clear_dialog.hide()
        self.clear_yes.hide()
        self.clear_no.hide()
    def clear_callback(self, event):
        self.recent = []
        for i in range(0,len(self.data)):
            self.data[i].clear_particles()
        self.fix_axes()
        self.MovieFrame.redraw_flag=True
        self.cleared_dialog.show()
        self.cleared_ok.show()
    def cleared_callback(self, widget):
        self.cleared_dialog.hide()
        self.cleared_ok.hide()
    def fix_axes(self):
        for i in range(0,len(self.MovieFrame.ax)):
            x_scale = self.MovieFrame.ax[i].get_xlim()
            y_scale = self.MovieFrame.ax[i].get_ylim()
            self.MovieFrame.ax[i].cla()            
            self.MovieFrame.ax[i].set_xlim(x_scale[0], x_scale[1])
            self.MovieFrame.ax[i].set_ylim(y_scale[0], y_scale[1])
