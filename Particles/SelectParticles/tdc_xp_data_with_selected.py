from Particles.tdc_xp_data import tdc_XP_Data
import numpy as np
from pprint import *

class tdc_XP_Data_with_Selected(tdc_XP_Data):
    """
    Child class of tdc_XP_Data
    it ads the ability to select particles and keep their parameters in lists
    """
    
    def __init__(self,
                 calc_id,
                 particle_name,
                 sample_dict=None,
                 get_weight=False,
                 get_id=False,
                 time_normalization=None): 
        """
        """
        tdc_XP_Data.__init__(self,
                             calc_id=calc_id,
                             particle_name=particle_name,
                             sample_dict=sample_dict,
                             get_weight=get_weight,
                             get_id=get_id,
                             time_normalization=time_normalization)

        #dict containing selected particles with key = ID, value = (index, x, y)
        #maybe should be a new class
        self.select = {}
    
    def read(self, i_ts, sample_dict = None, **kwargs):
        """
        Invokes superclass read method to update particle positions. 
        Also updates x and p of selected particle arrays
        """
        tdc_XP_Data.read(self,i_ts, sample_dict, **kwargs)
        #running list of selected particles that need to be updated
        update = self.select.copy()
#        if len(update)>0:
#            update = self.quick_read(update)
        if len(update)>0:
            self.lin_read(update)
        print "Final update of %s is " %(self.name)
        pprint(self.select)
                
    def quick_read(self, update):
        #checks that particles were stationary in ID list
        temp = update.copy()
        for j,key in enumerate(update):
            try:
                test_index = update[key][0]
                if key == self.id[test_index]:
                    self.select[key]= (test_index,self.x[test_index], self.p[test_index])
                    temp.pop(key)
                    print "%s with ID %i found with static quick_read" %(self.name, key)
            except IndexError:
                pass
        update = temp.copy()
        if len(update)==0:
            return update
        #checks that particles didn't move around much in ID list
        for j,key in enumerate(update):
            for k in range(-5,6):
                try:
                    test_index = update[key][0]+k
                    if key == self.id[test_index]:
                        print "%s with ID %i found with local quick_read" %(self.name,key)
                        self.select[key]=(test_index, self.x[test_index], self.p[test_index])
                        temp.pop(key)
                        break
                except IndexError:
                    pass
        return temp
            
    def lin_read(self,update):
        """
        Reads and searches data using linear search
        """
        temp = update.copy()
        print "--------------LIN_READ---------------------\n Temp is \n", temp
        for i in range(0,len(self.id)):
            for j,key in enumerate(update):
                if key == self.id[i]:
                    print "key = self.id at %i = %i with index %i" %(key, self.id[i], i)
                    self.select[key]=(i,self.x[i], self.p[i])
                    print "%s with ID %i updated to %s " %(self.name, key, str(self.select[key]))
                    temp.pop(key)
                    print "temp is now"
                    print temp
            if len(temp)==0:
                break
        update = temp.copy()
        #deals with destroyed particles
        if len(update)>0:
            for j,key in enumerate(update):
                print "%s %i not found" %(self.name, key)
                self.select.pop(key)
                temp.pop(key)
        if len(temp) != 0:
            print "failed to sort using lin_read"
        return temp
            
    def bin_read(self,update):
        """
        Reads and searches data using binary search
        """
        #sorts self.id

    def get_distance_idx_ID(self,x_plot,y_plot, x_scale, y_scale, selecting):
        """
        Returns the distance for the particle nearest to the selected position
        idx - index of the closest particle in the data array
        ID  - ID of the closest particle
        """
        distance=2**31
        idx=None
        ID=None
        x_scaled = self.x_scale(x_plot, x_scale)
        y_scaled = self.y_scale(y_plot, y_scale)
        
        for i in range(0,len(self.id)):
            test_dist = np.hypot(x_scaled- self.x_scale(self.x[i], x_scale),y_scaled - self.y_scale(self.p[i]))
            if test_dist<distance:
                distance = test_dist
                idx = i
                ID = self.id[i]
        return (distance, idx, ID)
        
    def x_scale(self, x_plot, x_scale=.31):
        """
        Returns x-coordinate normalized to (-1,1) coordinates
        """
        return 2*float(x_plot)/x_scale-1
    def y_scale(self, y_plot, y_scale=5e8):
        """
        Returns y-coordinate normalized to (-1,1) coordinates
        for semilog components and (-1,1) range individually
        """
        if abs(y_plot)<=1:
            return y_plot
        elif y_plot>1:
            return np.log10(y_plot)/np.log10(y_scale)
        else:
            return -np.log10(abs(y_plot))/np.log10(y_scale)        
        
    def select_particle(self, idx):
        """
        Add particle with i=idx to the list of the selected particles
        Format: key = ID, value = (index, x, p)
        """
        self.select[self.id[idx]]=(idx,self.x[idx],self.p[idx])
        
    def deselect_particle(self, ID):
        """
        Delete particle with ID from the list of selected particles
        """
        try:
            self.select.pop(ID)
        except: 
            print "No particle with ID %i found in selected particles" %(ID) 
        
    def clear_particles(self):
        self.select.clear()
        





