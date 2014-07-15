from Particles.tdc_xp_data import tdc_XP_Data
import numpy as np

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
        if len(update)>0:
            self.quick_read(update)
        else: 
            return
        if len(update)<5:
            self.lin_read()
        else:
            self.bin_read()
    def quick_read(self, update):
        #checks that particles were stationary in ID list
        for key in update:
            if key == self.id[update[key][0]]:
                update.pop[key]
                print "Particle with ID %i stationary" %(key)
        if len(update)==0:
            return
        #checks that particles didn't move around much in ID list
        for key in update:
            for j in range(-5,6):
                try:
                    test_index = update[key][0]+j
                    if key == self.id[test_index]:
                        print "found ID %i near source"
                        self.select[key]=(self.id[test_index], self.x[test_index], self.p[test_index])
                        update.pop[key]
                except IndexError:
                    pass
        print update
        if len(update)>5:
            self.bin_read(update)
        elif len(update)>0:
            self.lin_read(update)                                                 
            
    def lin_read(self,update):
        """
        Reads and searches data using linear search
        """
        #checks if particles have moved indices
        for i in range(0,len(self.id)):
            for key in update:
                if key == self.id[i]:
                    update[key]=(self.id[i],self.x[i], self.p[i])
                    update.pop[key]
                    break
        print update
        if len(update)>0:
            for key in update:
                self.select[key]=(update[key], None, None)
                print "Particle " + str(update[key]) + " not found."
                update.pop[key]
        print "Final update is "
        print update
        if len(update) != 0:
            print "failed to sort using lin_read"
            
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
        
        for i in range(0,len(self.x)):
            test_dist = np.hypot(x_scaled- self.x_scale(self.x[i], x_scale),y_scaled - self.y_scale(self.p[i]))
            if test_dist<distance:
                distance = test_dist
                idx = i
                ID = self.id[i]
        return (distance,idx, ID)
        
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
        





