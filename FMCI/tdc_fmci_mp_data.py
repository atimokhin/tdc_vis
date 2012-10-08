from Common_Data_Plot import tdc_Data
from tdc_fmci_xp_data import tdc_FMCI_XP_Data_Base


class tdc_FMCI_MP_Data(tdc_Data):
    """
    Represent FMCI_XP as a set of metaparticles:
    markersize contains the size of the metaparticle calculated 
    from the statistical weight of a metaparticle by self.setup.markersize()

    -> can change markersize
    """

    def __init__(self, fmci_xp_data, m_max, w_max):
        """
        Creates array represented particles to be plotted
        but do not adjust theit markersizes,
        after initialization all marker sizes are set to 1

        m_max -- maximum marker size
        w_max -- maximum distinguishable statistical weight
                 (particles with larger weighs will have their markersize set to m_max)
        """
        # copy plot information from fmci_xp_data
        self.name    = fmci_xp_data.name   
        self.calc_id = fmci_xp_data.calc_id
        self.fmci_xp = fmci_xp_data 
        self.m_max   = m_max
        self.w_max   = w_max
        # setup metaparticles
        self.setup_metaparticles()
        self.setup_markersize()

    @staticmethod
    def init_from_ascii(filename, m_max, w_max, **kwargs):
        """
        return tdc_FMCI_MP_Data instance initialized from ascii data file 'filename'

        m_max -- maximum marker size
        w_max -- maximum distinguishable statistical weight
                 (particles with larger weighs will have their markersize set to m_max)
        """
        return tdc_FMCI_MP_Data( tdc_FMCI_XP_Data_Base.init_from_ascii(filename), m_max, w_max) 

    def get_pure_data_copy(self):
        """
        Returns copy containing only data necessary for producing a sinle plot,
        without HDF file specific info
        Used for saving data for subsequent restoring of plot without
        accesing original data files
        """
        import copy
        data=copy.copy(self)
        data.fmci_xp = data.fmci_xp.get_pure_data_copy()
        return data

    def __repr__(self):
        s  = 'tdc_FMCI_MP_Data:\n'
        s += ' particle name : %s\n' % self.name
        s += '       calc_id : %s\n' % self.calc_id
        s += '         m_max : %g\n' % self.m_max
        s += '         w_max : %g\n' % self.w_max
        # partition 
        s += ' Contains => %s\n' % str(self.fmci_xp)
        return s

    def read(self, i_ts):
        """
        reads particles, fills fmci_XP array,
        cetups metaparticles and theit weights for already stored 
        m_max and w_max 
        """
        self.fmci_xp.read(i_ts)
        self.setup_metaparticles()
        self.setup_markersize()

    def get_time(self):
        return self.fmci_xp.get_time()
        
    def setup_metaparticles(self):
        """
        Supposed to be called after data in fmci_xp_data
        changes
        """
        self.i_ts = self.fmci_xp.i_ts   
        self.time = self.fmci_xp.time  
        # reset all lists
        n_max=self.fmci_xp.fmci_XP.size
        self.x=n_max*[0]
        self.p=n_max*[0]
        self.w=n_max*[0]
        # setup markersize
        self.markersize=n_max*[1]
        self.n=0
        # setup metaparticles
        for i,x in enumerate(self.fmci_xp.x):
            for j,p in enumerate(self.fmci_xp.p):
                w = self.fmci_xp.fmci_XP[i,j]
                if w>0:
                    self.__add_particle(x,p,w)
        # delete unused entries
        del self.x[self.n:]
        del self.p[self.n:]
        del self.w[self.n:]
        del self.markersize[self.n:]

        
    def setup_markersize(self,m_max=None,w_max=None):
        """
        m_max -- maximum markersize
        w_max -- maximum discriminated statistical weight
        """
        if m_max is not None:
            self.m_max = m_max
        if w_max is not None:
            self.w_max = w_max
        for i,w in enumerate(self.w):
            self.markersize[i] = self.m_max*min(1,float(w)/self.w_max)

    def set_m_max(self,m_max):
        self.m_max = m_max

    def set_w_max(self,w_max):
        self.w_max = w_max
            
    def __add_particle(self,x,p,w):
        """
        helper method
        """
        i=self.n
        self.x[i]=x
        self.p[i]=p
        self.w[i]=w
        self.n += 1
            

