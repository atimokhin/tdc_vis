from Particles.tdc_xp_data import tdc_XP_Data
import numpy as np
from select_particle import Select_Particle
from pprint import *
from copy import deepcopy

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

        #list of Select_Particles. Key: Value :: (idts, ID): Select_Particle
        self.select = {}
    def proximity_search(self,x_plot,y_plot, x_scale, y_scale, selecting):
        """
        Returns the distance for the particle nearest to the selected position
        idx - index of the closest particle in the data array
        ID  - ID of the closest particle
        """
        distance=2**31
        idx=None
        idts=None        
        ID=None
        x_scaled = self.x_scale(x_plot, x_scale)
        y_scaled = self.y_scale(y_plot, y_scale)
        
        for i in range(0,len(self.id)):
            test_dist = np.hypot(x_scaled- self.x_scale(self.x[i], x_scale),y_scaled - self.y_scale(self.p[i]))
            if test_dist<distance:
                distance = test_dist
                idx = i
                idts = self.idts[i]
                ID = self.id[i]
        return (distance, idx, idts, ID)
        
    def index_search(self, idts, ID):
        """
        Returns index of particle with matching idts and ID.
        Returns None if no matching particle found
        """
        for i in range(0,len(self.idts)):
            if self.id[i] == ID and self.idts[i] == idts:
                return (idts, ID, i)
        print "particle with idts %i and ID %i not found" %(idts, ID)
        return None
        
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
    #controls input form of Select_Particles
    def select_particle(self, idx):
        """
        Add particle with i=idx to the list of the selected particles
        Format: key = ID, value = (index, x, p)
        """
        new_particle = Select_Particle(self.idts[idx], self.id[idx], idx, self.x[idx], self.p[idx])
        print "Adding %s," %(self.name), new_particle
        self.select[(new_particle.idts, new_particle.ID)]=new_particle
        
    def deselect_particle(self, idts, ID):
        """
        Delete particle with ID from the list of selected particles
        """
        for particle in self.select:
            if particle.idts==idts and particle.ID == ID:
                print "Deselected ", particle
                self.select.pop(particle)
                return
        print "No particle with idts %i and ID %i found in selected particles" %(idts, ID) 
        
    def clear_particles(self):
        self.select.clear()
    
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
        print "------------------------------LIN_READ-------------------------------"
        print ("Temp is")
        pprint(temp)
        for i in range(0,len(self.id)):
            for particle in update.values():
#                if particle.ID == self.id[i]:
#                    print "particle found with ID %i at index %i" %(particle.ID, i)
#                    if particle.idts == self.idts[i]:
#                        print "particle also matches idts %i" %(particle.idts)
                key = (particle.idts, particle.ID)
                if key[1] ==self.id[i] and key[0] == self.idts[i]:
                    print "match at index %i with idts %i=%i and ID %i = %i" \
                        %(i, particle.idts, self.idts[i], particle.ID, self.id[i])
                    self.select[key].update(i, self.x[i], self.p[i])
                    print "%s with key %s updated to %s " %(self.name, key, self.select[key])
                    temp.pop(key)
                    print "temp is now"
                    print temp
            if len(temp)==0:
                break
        update = temp.copy()
        #deals with destroyed particles
        if len(update)>0:
            for key in update:
                print "%s with (idts, ID) %s not found" %(self.name, str(key))
#                self.select.pop(key)
                temp.pop(key)
        if len(temp) != 0:
            print "failed to sort using lin_read"
        return temp
            
    def bin_read(self,update):
        """
        Reads and searches data using binary search
        """
        #sorts self.id
        
#if __name__ == "__main__":
#    sample = Select_Particle(10,240,1024,2491,20414)
#    print "Hey hey hey %i " %(8), sample




