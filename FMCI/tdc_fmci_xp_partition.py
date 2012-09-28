from  numpy import *

class tdc_FMCI_XP_Partition(object):
    """
    Base class for partition of XP domain
    stores arrays with x,p and provides fuctions for calculating indexies
    for given values of x and p
    """

    def __init__(self):
        """
        """
        self.name   = 'Base'
        self.nx     = None
        self.x      = None
        self.x_cell = None
        self.np     = None
        self.p      = None
        self.p_cell = None
        
    def setup_x_grid(self,xx):
        """
        setup spatial grid (may be supplied with infromation from data files)
        """
        pass

    def x_idx(self,x):
        """
        returns index in X array
        if value is outside of the array, return None
        """
        if x <= self.x_cell[0] or x >= self.x_cell[-1]:
            return None
        else:
            return self.x_cell.searchsorted(x) - 1

    def p_idx(self,p):
        """
        returns index in P array,
        if value is outside of the array, return None
        """
        if p <= self.p_cell[0] or p >= self.p_cell[-1]:
            print 'p value outside of p grid!\n'
            return None
        else:
            return self.p_cell.searchsorted(p) - 1

    def __repr__(self):
        s  = 'tdc_FMCI_XP_Partition__' + self.name + ' :\n'
        if self.nx:
            s += ' nx: %4d;  x_cell: [%g, %g]\n'       % (self.nx,self.x_cell[0],self.x_cell[-1])
        s += ' np: %4d;  p_cell: [%1.2e, %1.2e]\n' % (self.np,self.p_cell[0],self.p_cell[-1])
        return s
    


class tdc_FMCI_XP_Partition__LinSemiLogUniform(tdc_FMCI_XP_Partition):
    """
    X is divided in nx linear bins,
    P is divided in 2*np+1 bins: log bins [-p2,-p1], [-p1,p1], log [p1,p2]  
    --------
    Example:
    --------
    tdc_FMCI_XP_Partition__LinSemiLogUniform(x_dict=dict(n=91,xx=None),p_dict=dict(n=30,pp=[1,1e8]))
    """

    def __init__(self, x_dict, p_dict):
        """
        Example:
         x_dict=dict(n=31, xx=[0,0.3])
         p_dict=dict(n=30, pp=[5,1e8])
        """
        tdc_FMCI_XP_Partition.__init__(self)
        self.name   = 'LinSemiLogUniform'
        # dictionary for division
        self.x_dict = x_dict
        self.p_dict = p_dict
        # -------------
        # Momentum grid
        # -------------
        np = self.p_dict['n']
        pp = self.p_dict['pp']
        # setup momentum grid
        p_log = logspace(log10(pp[0]), log10(pp[1]), np)
        self.p_cell = concatenate((-p_log[::-1],p_log)) 
        p = sqrt( p_log[:-1] * p_log[1:] )
        self.p  = concatenate((-p[::-1],[0],p)) 
        self.np = self.p.size

        
    def setup_x_grid(self,xx):
        """
        setup spatial grid (may be supplied with infromation from data files)
        """
        # if space interval was not provided at initialization
        # use spatial interval in the function argument
        if not self.x_dict['xx']:
            if not isinstance( xx, (tuple,list)): 
                raise Exception('%s: non sequence provided to setup_x_grid!' % str(self) )
            self.x_dict['xx'] = xx
        # setup spatial grid    
        nx = self.x_dict['n']
        xx = self.x_dict['xx']
        self.x_cell = linspace(xx[0],xx[1],nx)
        self.x  = 0.5*( self.x_cell[:-1] + self.x_cell[1:] )
        self.nx = self.x.size
            
