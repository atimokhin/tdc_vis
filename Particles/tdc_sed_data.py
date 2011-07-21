import numpy as np
import h5py
import math

from Common         import tdc_Mesh, tdc_Setup_Props
from tdc_xp_data    import tdc_XP_Data

class tdc_SED_Data:
    """
    This class contains data for single particle specie SED
    It calculated dN/dlogP dX: nomalized to n_GJ
    X and P are dimensionless quantities

    NB: redirects all non-defined requests to XP class
    -----------
    Attributes:
    -----------
    xp
       tdc_XP_Data
    W0
       GJ normalization parameter
    xx_default
       default space interval
    xx
       current space interval
    p_bins
       current 4-momentum bins in form (Pmin,Pmax,nP)
    
    P_bins
       4-momentum bins
    dN_dlogPdX_u
       SED for particles moving UP
    dN_dlogPdX_d
       SED for particles moving DOWN

    plasma_properties
       dictionary with plasma properties
    """

    def __init__(self, calc_id, particle_name, p_bins, xx=None):
        """
        - opens particle HDF5 file, 
        - setup 4-momentum bins,
        - setup default space interval
        NB: Reads setup_properties.h5
        ---------
        Parameters:
        ---------
        calc_id
        particle_name
        p_bins = (Pmin,Pmax,nP)
        ---------
        Options:
        ---------
        xx     = (x1,x2)
            <None> by default the whole domain will be used
        """
        # name and calc_id
        self.name    = particle_name
        self.calc_id = calc_id
        # setup XP_Data
        sample_dict = dict(name='regular', n_reduce=1, n_min=1)
        self.xp = tdc_XP_Data(calc_id, particle_name, sample_dict, get_weight=True)
        # interface to timetable
        self.timetable = self.xp.timetable
        # set 4-momentum bins
        self.set_momentum_bins(p_bins)
        # set default space interval
        self.set_xx_default(xx)
        # initialize xx
        self.xx = self.xx_default
        # normalization parameters
        setup_props = tdc_Setup_Props(calc_id)
        self.W0 = setup_props.get_papam('FMPProps/W0')

    def get_pure_data_copy(self):
        """
        Returns copy containing only data necessary for producing a sinle plot,
        without HDF file specific info
        Used for saving data for subsequent restoring of plot without
        accesing original data files
        """
        import copy
        data=copy.copy(self)
        data.xp=data.xp.get_pure_data_copy() 
        return data

    ## def __getattr__(self,attrname):
    ##     "Redirect non-implemented requests to XP_Data self.xp"
    ##     return getattr(self.xp, attrname)
    
    def __repr__(self):
        s  = 'tdc_SED_Data:\n'
        s += ' particle name : %s\n' % self.name
        s += '       calc_id : %s\n' % self.calc_id
        s += '          i_ts : %g\n' % self.xp.i_ts
        s += '        p_bins = [%g, %g, %g]\n' % tuple(self.p_bins)
        s += '            xx = [%g, %g]\n'     % tuple(self.xx)
        return s

    def read(self, i_ts, xx=None, **kwargs):
        """
        Read particle data for timeshot i_ts and calculate SED for
        specified space interval xx, or if xx==None for the default
        one
        """
        self.read_particles(i_ts)
        self.calculate_sed(xx)

    def read_particles(self, i_ts):
        "Read particles data for timeshot i_ts"
        print 'Reading data   "%s" ... ' % self.xp.name
        self.xp.read(i_ts)
        
    def calculate_sed(self, xx=None):
        """
        Calculate SED for current timeshot,
        also sets current xx
        Options:
        --------
        xx     = (x1,x2) <None> by default domain given
                 at initilaization domain will be used
        """
        # change current space interval
        if xx:
            self.xx = xx
        else:
            self.xx = self.xx_default
        # set distributions to zero
        self.dN_dlogPdX_u *=0
        self.dN_dlogPdX_d *=0
        # iterate over particles ----------------------
        print 'Iterating over "%s" ... ' % self.xp.name
        for  x,p,w  in zip(self.xp.x,self.xp.p,self.xp.w):
            # only count particles in the selected domain
            if x>=self.xx[0] and x<=self.xx[1]:
                abs_p = abs(p)
                # |p| > p[0]
                if self.P_bins[0] <= abs_p:
                    # all particles with |p| > p[-1] go into the last bin
                    if abs_p < self.P_bins[-1]:
                        j = np.floor( np.log10(abs_p/self.P_bins[0])/self.dlogP )
                    else:
                        j = -1
                    # Up and Down distributions counted separately
                    if p>=0:
                        self.dN_dlogPdX_u[j] += w
                    else:
                        self.dN_dlogPdX_d[j] += w
        # ---------------------------------------------
        # normalize spectrum
        f_norm = self.W0/( self.dlogP*(self.xx[1]-self.xx[0]) ) 
        self.dN_dlogPdX_u *= f_norm
        self.dN_dlogPdX_d *= f_norm


    def get_omega2(self):
        """
        Calculates normalized \omega_pl^2
        NB: Particles SED must be calculated before
            For Pairs returns 0
        """
        # for pairs return 0
        if self.name=='Pairs':
            return 0
        # \gamma^3
        gamma3 = pow(self.P_bins**2+1,1.5)
        omega2 = ( (self.dN_dlogPdX_u+self.dN_dlogPdX_d)/gamma3 ).sum() * self.dlogP 
        return omega2
        
    
    def get_number_of_particles(self, pp=None):
        """
        Return dictionary with number of particles
        in the 4-momentum range pp = (P1,P2)
        ------------        
        n_p['UP']     : # of particles moving UP   
        n_p['DOWN']   : # of particles moving DOWN
        n_p['TOTAL']  : total number of particles
        n_p['pp']     : momentum range
        """
        if not pp:
            idxs = np.r_[0:len(self.P_bins)]
        else:
            idxs = np.intersect1d( np.where(self.P_bins>=pp[0])[0],
                                   np.where(self.P_bins<=pp[1])[0] )
        if not len(idxs):
            print 'Wrong momentum range :', pp
        n_p=dict()
        n_p['pp']    = [ self.P_bins[idxs[0]],  self.P_bins[idxs[-1]] ]
        n_p['UP']    = self.dN_dlogPdX_u[idxs].sum()*self.dlogP*(self.xx[1]-self.xx[0])
        n_p['DOWN']  = self.dN_dlogPdX_d[idxs].sum()*self.dlogP*(self.xx[1]-self.xx[0])
        n_p['TOTAL'] = n_p['UP']+n_p['DOWN']
        return n_p


    def get_particle_energy(self, pp=None):
        """
        Return dictionary with total energy of particles
        in the 4-momentum range pp = (P1,P2)
        ------------
        e_p['UP']     : # of particles moving UP   
        e_p['DOWN']   : # of particles moving DOWN
        e_p['TOTAL']  : total number of particles
        e_p['pp']     : momentum range
        """
        if not pp:
            idxs = np.r_[0:len(self.P_bins)]
        else:
            idxs = np.intersect1d( np.where(self.P_bins>=pp[0])[0],
                                   np.where(self.P_bins<=pp[1])[0] )
        if not len(idxs):
            print 'Wrong momentum range :', pp
        e_p=dict()
        e_p['pp']    = [ self.P_bins[idxs[0]],  self.P_bins[idxs[-1]] ]
        e_p['UP']    = (self.dN_dlogPdX_u[idxs]*self.P_bins[idxs]).sum()*self.dlogP*(self.xx[1]-self.xx[0])
        e_p['DOWN']  = (self.dN_dlogPdX_d[idxs]*self.P_bins[idxs]).sum()*self.dlogP*(self.xx[1]-self.xx[0])
        e_p['TOTAL'] = e_p['UP']+e_p['DOWN']
        return e_p


    def set_momentum_bins(self,p_bins):
        """
        Set 4-momentum bins for spectrum calculation
        NB: 4-momentum bins can be changed only by this fuction
        Arguments:
        ---------
        p_bins
           (Pmin,Pmax,nP) 4-momentum bins
        """
        # store current 4-momentum bins info
        self.p_bins = p_bins
        (Pmin,Pmax,nP) = self.p_bins
        self.P_bins = np.logspace(np.log10(Pmin),np.log10(Pmax),nP+1)
        self.dlogP  = np.log10(self.P_bins[1]/self.P_bins[0])
        self.dN_dlogPdX_u = np.zeros_like(self.P_bins)
        self.dN_dlogPdX_d = np.zeros_like(self.P_bins)


    def set_xx_default(self,xx=None):
        """
        Set **default** space interval for which particle spectrum
        will be calculated
        NB: Reads mesh.h5 !
        xx
          (x1,x2), if None [default] use whole computational domain
        """
        if xx:
            self.xx_default = xx
        else:
            # read Mesh <=== !
            mesh = tdc_Mesh(self.xp.calc_id)
            self.xx_default = (mesh.xmin,mesh.xmax)


