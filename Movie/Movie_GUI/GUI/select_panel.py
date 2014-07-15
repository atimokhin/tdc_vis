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
        self.x_scale = self.MovieFrame.ax[0].get_xlim()
        self.x_scale = self.x_scale[1]-self.x_scale[0]
        self.y_scale = self.MovieFrame.ax[0].get_ylim()
        self.y_scale = self.y_scale[1]
        
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
        
        #Select/Deselect
        self.select_button = gtk.RadioButton(None, 'Select')
        self.select_button.connect('toggled', self.select_button_callback)
        self.deselect_button = gtk.RadioButton(self.select_button, 'Deselect')
        self.select_button.set_sensitive(False)
        self.deselect_button.set_sensitive(False)        
        main_box.pack_start(self.select_button)
        main_box.pack_start(self.deselect_button)
        
        #Clear
        self.clear_button= gtk.Button('Clear All')
        self.clear_button.connect('clicked', self.clear_check)
        main_box.pack_end(self.clear_button)
        
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
    #must rewrite possible attributes for ID tags; using index for now
    def pick_callback(self, event):
        x_plot = event.mouseevent.xdata
        y_plot = event.mouseevent.ydata
        
        #deals with duplication problem
        if (x_plot, y_plot) in self.recent:
            return
        else:
            self.recent.append((x_plot, y_plot))
        print "-------------------PICK---------EVENT------------"
        print "called point with coordinates \n " + str((x_plot, y_plot))
        bound = len(self.MovieFrame.seq_plotter[0].data)
        possible= []
        particle_type = None
        
        #generates one of each type of particle closest to pick_event
        for i in range(0,bound):
            particle = self.data[i].get_distance_idx_ID(x_plot, y_plot, self.x_scale, self.y_scale, self.selecting)
            possible.append(particle)
       
        mindist = 2**31
        particle=None
        
        #finds closest particle 
        for i in range(0,len(possible)):
            if possible[i][0]<mindist:
                mindist = possible[i][0]
                particle= possible[i]
                particle_type=i
        try:
            print "picked %s with ID %i" %(self.data[particle_type].name, particle[2])
        except TypeError:
            print "No particles to deselect!"
#--------------BUTTON-FUNCTIONALITY---------------------------------
        if self.selecting:
            self.data[particle_type].select_particle(particle[1])
            self.MovieFrame.ax[0].cla()
        else:
            self.data[particle_type].deselect_particle(particle[2])
#            self.MovieFrame.ax[0].cla()
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
            self.MovieFrame.ax[i].cla()
            self.MovieFrame.ax[i].set_xlim((0,self.x_scale))
            self.MovieFrame.ax[i].set_ylim((-self.y_scale,self.y_scale))
