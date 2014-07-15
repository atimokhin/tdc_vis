# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 15:18:52 2014

@author: Alexander
"""
import gtk

class SelectPanel(gtk.Frame):
    #controls highlighting of select button    
    def set_flags_to_default_values(self):
        self.select_flag = False
    
    
    def __init__(self, **kwargs):
        
        self.set_flags_to_default_values()
        gtk.Frame.__init__(self, **kwargs)
        #main box for packing everything        
        main_box = gtk.HBox()
        main_box.set_border_width(5)
        self.add(main_box)
        
        #select button
        self.select_button = gtk.Button('Selection')
        self.select_button.connect('clicked', self.set_flag)
        main_box.pack_start(self.select_button, expand = False, padding = 5)
        
    def set_flag(self, widget):
        self.select_flag = True
    
