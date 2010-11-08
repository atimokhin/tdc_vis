
class tdc_Tracked_Particle:
    """
    Stores information about single tracked particle
    
    Members:
    --------
    name
      particle name
    IDTS   
    ID     
    marker
      # of marker for showing this particle
      (unique identifier of particle family with the same ID/IDTS)
    idx_ds
      position of particle in the datased for each timestep
    timeshot
      array with timeshots where the particle is present
      and tracked
    X
      array with particle coordinates
    P
      array with particle momenta
    """
    def __init__(self, name, IDTS, ID, marker):
        self.name     = name
        self.IDTS     = IDTS
        self.ID       = ID
        self.marker   = marker
        self.idx_ds   = []
        self.timeshot = []
        self.X        = []
        self.P        = []

    def __len__(self):
        return len(self.X)

    def __eq__(self,other):
        return self.name     == other.name     and \
               self.IDTS     == other.IDTS     and \
               self.ID       == other.ID       and \
               self.marker   == other.marker   and \
               self.idx_ds   == other.idx_ds   and \
               self.timeshot == other.timeshot and \
               self.X        == other.X        and \
               self.P        == other.P

    def __repr__(self):
        s  = 'tdc_Tracked_Particle:\n'
        s += '   name = %s\n' % self.name
        s += '   IDTS = %g\n' % self.IDTS
        s += '     ID = %g\n' % self.ID
        s += ' marker = %g\n' % self.marker
        s += '   idx_ds : %s\n' % str(self.idx_ds)
        s += ' timeshot : %s\n' % str(self.timeshot)
        s += '        X : %s\n' % str(self.X)
        s += '        P : %s\n' % str(self.P)
        return s
        
