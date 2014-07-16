# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 03:45:08 2014

@author: Alexander
"""

class Select_Particle(object):
    """
    Class to keep track of all the different variables associated with selecting and tracking particles.
    Can be expanded to include particle history.
    """
    def __init__(self, idts, ID, index, x, p):
        self.idts = idts
        self.ID = ID
        self.index = index
        self.x = x
        self.p = p
    def get_coordinates(self):
        return (self.x, self.p)
    