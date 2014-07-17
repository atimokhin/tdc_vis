from Particles.tdc_xp_data  import      tdc_XP_Data
from select_particle        import      Select_Particle
from particle_search        import      *
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
        if len(update)>0:
            update = self.quick_read(update)
        if len(update)>0 and len(update)<10:
            self.lin_read(update)
        else:
            self.bin_read(update)
        if len(self.select)>0:
            print "Final update of %s is " %(self.name)
            pprint(self.select)
                
    def quick_read(self, update):
        print "--------------------------QUICK---READ--------------------------"
        index_list = quick_search(self.idts, self.id, update, self.select)
        for key in index_list:
            if index_list[key]!=-1:
                index = index_list[key]
                self.select[key].update(index, self.x[index], self.p[index])
                update.remove(key)
        return update
            
    def lin_read(self,update):
        """
        Reads and searches data using linear search
        """
        print "------------------------------LIN_READ-------------------------------"
        index_list = lin_search(self.idts, self.id, update)
        self.update(index_list)
        
    def bin_read(self,update):
        """
        Reads and searches data using binary search
        """
        index_list = bin_search(self.idts, self.id, update)
        self.update(index_list)
        
    def update(self, index_list):
        for key in index_list:
            index = index_list[key]
            if index ==-1:
                self.select.pop(key)
            else:
                self.select[key].update(index, self.x[index], self.p[index])
            
        
        
        
        



