# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 15:18:52 2014

@author: Alexander
"""
import gtk
import numpy as np

class SelectPanel(gtk.Frame):
    #controls highlighting of select button    
    def set_flags_to_default_values(self):
        self.tracking_flag = True
        self.tracking_changed = False
    
    
    def __init__(self, movie_frame,**kwargs):
        self.MovieFrame = movie_frame
        self.set_flags_to_default_values()
        gtk.Frame.__init__(self, **kwargs)
        self.set_size_request(25, 60)
        #main box for packing everything        
        main_box = gtk.HBox()
        main_box.set_border_width(5)
        self.add(main_box)
        #image
        self.track_image = gtk.Image()
        self.track_image.set_from_stock(gtk.STOCK_NO, 1)
        main_box.pack_end(self.track_image)
        #select button
        self.select_button = gtk.CheckButton('Tracking')
        self.select_button.set_active(False)
        self.select_button.connect('clicked', self.set_flag)
        main_box.pack_start(self.select_button, expand = True, padding = 5)
        #stores chosen particles
        self.selected = []
        # TEST
        for dat in self.MovieFrame.seq_plotter[0].data:
            print dat.name

        
        
    def set_flag(self, widget):
        if self.select_button.get_active():
            self.tracking_flag = True
            self.pick_id = self.MovieFrame.canvas.mpl_connect('pick_event', self.pick_callback)
            self.track_image.set_from_stock(gtk.STOCK_YES, 1)
        else:
            self.tracking_flag = False
            self.track_image.set_from_stock(gtk.STOCK_NO, 1)
            self.MovieFrame.canvas.mpl_disconnect(self.pick_id)
        print "Tracking flag is now " + str(self.tracking_flag)
        return self.flip_tracking_changed()
    #changes value of tracking_changed (used here and in movie_engine)
    
    def flip_tracking_changed(self):
        self.tracking_changed = not self.tracking_changed

    def pick_callback(self, event):
        print "pick_callback called"
        xdata = event.mouseevent.xdata
        ydata = event.mouseevent.ydata
        #minpoint = mindist(xdata, ydata, particles)
        #stores data in list

        for dat in self.MovieFrame.seq_plotter[0].data:
            print dat.name

        
        if (xdata, ydata) in self.selected:
            self.selected.remove((xdata, ydata))
            print "particle removed"
        else:
            self.selected.append((xdata, ydata))
            print "particle added"
        print "stored array is now" + str(self.selected)
        self.MovieFrame.seq_plotter[0].plot_trace(self.MovieFrame.ax[0])
        #call highlighting function?
                
        #store data in array
        
#    #searches for nearest particle tag
#    def mindist(self, xdata, ydata, particles):
#        minpoint = None
#        mindist = 2**31
#        for particle in particles:
#            testdist = np.hypot(particle.x-xdata, particle.y-ydata)
#            if testdist<mindist:
#                mindist = testdist
#                minpoint = particle
#        return minpoint
    
