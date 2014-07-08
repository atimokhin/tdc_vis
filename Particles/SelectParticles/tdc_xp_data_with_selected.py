from Particles.tdc_xp_data import tdc_XP_Data

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
                 time_normalization=None): 
        """
        """
        tdc_XP_Data.__init__(self,
                             calc_id=calc_id,
                             particle_name=particle_name,
                             sample_dict=sample_dict,
                             get_weight=get_weight,
                             time_normalization=time_normalization)

        self.select_x=[]
        self.select_y=[]
        self.select_ID=[]

    def get_distance_idx_ID(self,x_plot,y_plot):
        """
        Returns the distance for the particle nearest to the selected position
        idx - index of the closest particle in the data array
        ID  - ID of the closest particle
        """
        distance=0
        idx=None
        ID=None
        return (distance,idx, ID)
        
    def select_particle(self, idx):
        """
        Add particle with i=idx to the list of the selected particles
        """
        pass

    def deselect_particle(self, ID):
        """
        Delete particle with ID from the list of selected particles
        """
        pass





