from Particles.tdc_xp_data  import      tdc_XP_Data
from select_particle        import      Select_Particle
import numpy as np
from pprint import *
from operator import itemgetter


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
        self.select[(self.idts[idx], self.id[idx])]=new_particle
        
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
        update = self.select.keys()
#        if len(update)>0:
#            update = self.quick_read(update)
#        if len(update)<10:
#            self.lin_read(update)
#        else:
        self.bin_read(update)
        if len(self.select)>0:
            print "Final update of %s is " %(self.name)
            pprint(self.select)
                
    def quick_read(self, update):
        print "--------------------------QUICK---READ--------------------------"
        #checks that particles were stationary in ID list
        temp = update[:]
        print "temp is "
        pprint(temp)
        for key in update:
            try:
                test_index = self.select[key].index
                if self.select[key].ID == self.id[test_index] and self.select[key].idts == self.idts[test_index]:
                    self.select[key].update(test_index, self.x[test_index], self.p[test_index])
                    temp.remove(key)
                    print self.name + " with identifier " + str(key) + " found with static quick_read."
            except IndexError:
                pass
        update = temp[:]
        if len(update)>0:
            #checks that particles didn't move around much in ID list
            for key in update:
                for k in range(-5,6):
                    try:
                        test_index = self.select[key].index+k
                        if self.select[key].ID == self.id[test_index] and self.select[key].idts == self.idts[test_index]:
                            print self.name +  "with indentifier " + str(key) + "found with local quick_read."
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
        temp = update[:]
        print "------------------------------LIN_READ-------------------------------"
        print ("Temp is")
        pprint(temp)
        for i in range(0,len(self.id)):
            for key in update:
                if key[1] == self.id[i] and key[0] == self.idts[i]:
                    print "match at index %i with idts %i=%i and ID %i = %i" \
                            %(i, key[0], self.idts[i], key[1], self.id[i])
                    self.select[key].update(i, self.x[i], self.p[i])
                    print "%s with key %s updated to %s " %(self.name, key, self.select[key])
                    temp.remove(key)
                    print "temp is now", temp
            if len(temp)==0:
                break
        update = temp[:]
        #deals with destroyed particles
        if len(update)>0:
            for key in update:
                print "%s with (idts, ID) %s not found" %(self.name, str(key))
#                self.select.pop(key)
                temp.remove(key)
        if len(temp) != 0:
            print "failed to sort using lin_read"
        return temp
            
    def bin_read(self,update):
        """
        Reads and searches data using binary search
        """
        #sorts self.id first
        sort_array = zip(self.id, self.idts, range(0,len(self.id)))
        sorted(sort_array, key = itemgetter(0))
        for key in update:
            self.bin_search(sort_array,key)
        
    def bin_search(self, sort_array, key):
        print "length of possibles is now ", len(sort_array)
        if len(sort_array) == 0:
            print str(self.name) + "with ID " + str(key[1]) + "not found"
            return
        test_index = len(sort_array)/2
        if key[1]==sort_array[test_index][0] and key[0] == sort_array[test_index][1]:
            true_index = sort_array[test_index][2]
            self.select[key].update(true_index, self.x[true_index], self.p[true_index])
            print str(self.name) + "with ID " + str(key) + "updated using bin_read"
            return
        elif key[1]<sort_array[test_index][0]:
            self.bin_search(sort_array[0:test_index], key)
        else:
            self.bin_search(sort_array[test_index+1:], key)
        return
            
        
        
        
        



