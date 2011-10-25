import pickle

## import Common
from Auxiliary import tdc_get_bound_index, tdc_Filenames, tdc_Timetable_Cached

import Particles
from Particles     import tdc_XP_Data

from tdc_tracked_particle   import tdc_Tracked_Particle


class tdc_TP_Data:
    """
    Members:
    --------
    Particles
       Dictionary which contains lists with tdc_Tracked_Particle
       instances for selected Particles
       i.e. Particles['Pairs'] = [ tdc_Tracked_Particle1,
                                   tdc_Tracked_Particle2,
                                   ... ]
    calc_id
       calc_id, get from Selected_Particles
    n_tracked_orig
       number of originally selected particles, i.e.
       particles in SelectedParticles used in track_particles()
       n_tracked = len(Particles['Pairs']) 
    timetable
       tdc_Timetable_Cachet instance
    time_interval
    timeshot_interval
    NB:
    ---
    All non-implemented requestst are redirected to self.Particles
    """

    def __init__(self):
        self.Particles         = dict()
        self.n_tracked_orig    = 0
        self.calc_id           = None
        self.time_interval     = []
        self.timeshot_interval = []
        self.timetable         = None
        self.i_ts              = None

    def __str__(self):
        s  = 'n=%i '          % self.get_number_of_tracked_particles()
        s += 'tt=[%g, %g] '   % (self.time_interval[0],self.time_interval[1])
        s += 'i_ts=[%g, %g] ' % (self.timeshot_interval[0],self.timeshot_interval[1])
        s += 'particles=%s'   %  str(self.keys()) 
        return s

    def __getattr__(self,attrname):
        "Redirects all requests to Particles"
        return getattr (self.Particles,attrname)

    def __repr__(self):
        s  = 'tdc_TP_Data:\n'
        s += '  original number of tracked particles: %g\n' % self.n_tracked_orig
        s += '           number of tracked particles: %g\n' % \
             self.get_number_of_tracked_particles()
        s += '  calc_id : %s\n' % self.calc_id 
        s += '  time_interval     : [%g, %g]\n' % tuple(self.time_interval)
        s += '  timeshot_interval : [%g, %g]\n' % tuple(self.timeshot_interval)
        return s

    def read(self, i_ts,**kwargs):
        self.i_ts = i_ts
        self.timetable.read_time(i_ts)

    def get_original_number_of_tracked_particles(self):
        """
        number of originally selected particles, i.e.
        particles in SelectedParticles used in track_particles()
        """
        return self.n_tracked_orig

    def get_number_of_tracked_particles(self):
        "actual number of tracked particle"
        tps = self.Particles.itervalues().next()
        return len(tps)

    def get_list_of_tracked_particle_markers(self):
        tps = self.Particles.itervalues().next()
        return sorted([ tp.marker for tp in tps ])

    def delete(self,idxs):
        "Delete tracked particles with markers in idxs"
        # check idxs
        if not isinstance(idxs, (tuple,list)): idxs = (idxs,)
        idxs = set(idxs)
        markers = self.get_list_of_tracked_particle_markers()
        if not idxs.intersection( markers ): raise IndexError
        # delete elements from all particle lists
        for name,TPs in self.Particles.items():
            self.Particles[name] = [ tp  for tp in TPs  if tp.marker not in idxs ]

    def select(self,idxs):
        "Leaves only tracked particles with markers in idxs"
        # check idxs
        if not isinstance(idxs, (tuple,list)): idxs = (idxs,)
        idxs = set(idxs)
        markers = self.get_list_of_tracked_particle_markers()
        if not idxs.intersection( markers ): raise IndexError
        # select elements from all particle lists
        for name,TPs in self.Particles.items():
            self.Particles[name] = [ tp  for tp in TPs  if tp.marker in idxs ]

    def add(self,tp1,idxs):
        """
        add tracked particles from tdc_TP_Data instance tp1 with markers idxs
        """
        if not isinstance(idxs, (tuple,list)): idxs = (idxs,)
        idxs = set(idxs)
        markers = tp1.get_list_of_tracked_particle_markers()
        if not idxs.intersection( markers ): raise IndexError
        # add particles from tp1
        for name,TPs in tp1.Particles.items():
            new_TPs = [ tp  for tp in TPs  if tp.marker in idxs ]
            i = self.n_tracked_orig
            # change markers of new particles
            for p in new_TPs:
                p.marker = i
                i += 1
            self.Particles[name].extend(new_TPs)
        # change counter of particle markers
        self.n_tracked_orig = i

    def save_to_file(self, tp_id):
        """
        Saves TP into corresponding RESULTS directory
        into file 'tp_{tp_id}.dat'
        (uses pickle to do this)
        """
        filename = 'tp_' + tp_id + '.dat'
        full_filename = tdc_Filenames().get_full_filename(self.calc_id,filename)
        pickle.dump( self, open(full_filename,'w') )

    def setup_from_file(self, calc_id, tp_id):
        """
        Reads TP data from file 'tp_{tp_id}.dat'
        in the calc_id RESULTS directory
        (uses pickle to do this)
        """
        filename = 'tp_' + tp_id + '.dat'
        full_filename = tdc_Filenames().get_full_filename(calc_id,filename)
        tp = pickle.load( open(full_filename,'r') )
        self.Particles         = tp.Particles        
        self.n_tracked_orig    = tp.n_tracked_orig        
        self.calc_id           = tp.calc_id          
        self.time_interval     = tp.time_interval    
        self.timeshot_interval = tp.timeshot_interval
        self.timetable         = tp.timetable 
        self.i_ts              = None
                
    def track_particles(self, SP, tt=None, particle_names=None):
        """
        Find parameters of selected particles in HDF files
        and store them in corresponding arrays
        SP:
           tdc_Selected_Particles class instance with IDs of
           selected particles
        Options:
        --------
        tt:
           [t1,t2] time interval where particles are tracked
           if None <default> the whole time interval
           will be searched for tracked particles
        particle_names:
           list of particles to be tracked
           if None <default> then  ['Pairs', 'Electrons', 'Positrons']
        """
        # sort selected particles according to IDTS ------
        import operator
        SP.sort(key=operator.itemgetter(0))
        # save calc_id -----------------------------------
        self.calc_id = SP.calc_id
        # save number of tracked particles ---------------
        self.n_tracked_orig = len(SP)
        # initialize particle_names ----------------------
        if particle_names:
            # if present, Pairs must be first entry in the list
            if 'Pairs' in particle_names and 'Pairs'!=particle_names[0]:
                particle_names.remove('Pairs')
                particle_names.insert(0,'Pairs')
        else:
            particle_names = ['Pairs', 'Electrons', 'Positrons']
        # initialize particle data -----------------------
        self.Particles=dict()
        for name in particle_names:
            self.Particles[name]=[]
            for i,(IDTS,ID) in enumerate(SP):
                self.Particles[name].append( tdc_Tracked_Particle(name,IDTS,ID, i) )
        # initialize timetable ---------------------------
        # use timetable from the first particles XP_Data in particle_names
        xp=tdc_XP_Data(self.calc_id, particle_names[0] )
        self.timetable = tdc_Timetable_Cached(xp.timetable)
        # ************************************************
        # Iterations over particle names 
        # ************************************************
        # NB: particle_names must be sorted in the right order
        # Pairs first!
        for  particle_name in particle_names:
            xp=tdc_XP_Data(self.calc_id, particle_name )
            # get time and timestep arrays
            time_array      =  xp.timetable.get_time_array()
            timesteps_array =  xp.timetable.get_timestep_array()
            # Set time domain ----------------------------
            # boundaries of time domain set in tt argument
            # or the whole time domain
            if tt:
                idx_tt = [ tdc_get_bound_index(t,time_array) for t in tt ]
            else:
                idx_tt = [0, len(time_array)-1]
            # index of the timestep where the first pair appears
            idx_idts_start = tdc_get_bound_index(SP[0][0],timesteps_array)
            # indexies of timesteps where particles will be searched <<<<
            idxs_ts = range( max(idx_idts_start,idx_tt[0]), idx_tt[1]+1 )
            # --------------------------------------------
            # set time and timestep intervals
            self.time_interval = [time_array[idxs_ts[0]], time_array[idxs_ts[-1]]]
            self.timeshot_interval = [idxs_ts[0]+1, idxs_ts[-1]+1]
            # print log message
            print '\nStart iterations over "%s"' % particle_name
            print ' Total number of particle IDs we are looking for : %i' % len(SP)
            print ' Timeshots to be analyzed :  [ %i : %i ], Total = %i' % \
                  (idxs_ts[0]+1, idxs_ts[-1]+1, len(idxs_ts))
            print ' t = [%.4g, %.4g]' % ( time_array[idxs_ts[0]],
                                          time_array[idxs_ts[-1]] )
            # number of particles found at previouls time step
            n_p__found_last_time = 0
            # position in SP list - start for each particle at the beginning
            i_SP = 0
            # Cache_0: particles potentially present at the current time step
            Cache_0 = _particles_Cache_0()
            # Timestep iterations ========================
            for  i_ts_iter_step,idx_ts  in  enumerate(idxs_ts):
                # timeshot number -- starts at 1!
                i_ts = idx_ts+1
                # any particles at the timestep? - if yes proceed
                if xp.any_particle_at_timeshot(i_ts):
                    log_message = ''
                    # add new particles to Chache_0:
                    # whose parent Pairs were created at the current
                    # timestep or earlier (if this is the first iteration
                    # over the timestep)
                    for i in range(i_SP,len(SP)):
                        if timesteps_array[idx_ts] >= SP[i][0]:
                            Cache_0.append(SP,i)
                            i_SP += 1
                    # Cache_1: main cache
                    #
                    # add particles to the main cache:
                    # for Pairs - add all                
                    # for Electrons/Positrons - add them only if there is
                    # no such Pair at the current time step
                    Cache_1 = _particles_Cache_1()
                    for i,(IDTS,ID,idx_sp) in enumerate(Cache_0):
                        if ( not self.Particles.get('Pairs')                     or \
                             not self.Particles['Pairs'][idx_sp]                 or \
                             self.Particles['Pairs'][idx_sp].timeshot[-1] < i_ts    \
                             ):
                            Cache_1.append(Cache_0,i)                    
                    # Cache_2: working cache
                    #
                    # add all particles from Cache_1
                    Cache_2 = _particles_Cache_2(Cache_1)
                    # log message: number of particles to be searched
                    n_p__search = len(Cache_2)
                    # get IDTS and ID arrays
                    xp.setup_dataspaces('/IDTS/'+ str(i_ts))
                    idts_array = xp.read_dataset('/IDTS/'+ str(i_ts))
                    id_array   = xp.read_dataset('/ID/'  + str(i_ts))
                    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    # looking for particles from Cache_2 
                    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    # First, for each particle try to find it at
                    # its previous position in datasets.
                    # Delete particles found in this way from Cache_2
                    Cache_2__delete_idx_list = []
                    for i_C2, (IDTS,ID,idx_C1) in enumerate(Cache_2):
                        idx_sp = Cache_1.idx_sp[idx_C1]
                        # do the rest only if such particle has been found before
                        if self.Particles[particle_name][idx_sp]:
                            i_ds = self.Particles[particle_name][idx_sp].idx_ds[-1]
                            # is the particle at the same position in the array?
                            if ( idts_array.size >= i_ds+1 and \
                                 idts_array[i_ds] == IDTS and id_array[i_ds] == ID ):
                                Cache_1.idx_ds[idx_C1] = i_ds
                                Cache_2__delete_idx_list.append(i_C2)
                    # delete found particles from Cache_2.
                    Cache_2.delete(Cache_2__delete_idx_list)
                    # -----------------------------------
                    # iterate over particles in dataset - if necessary
                    # -----------------------------------
                    # number of particles at new positions in the dataset
                    n_p__new = 0
                    if Cache_2:
                        for i_ds in range( len(idts_array) ):
                            # iterate over tracked particles in Cache_2.
                            Cache_2__delete_idx_list = []
                            for i_C2, (IDTS,ID,idx_C1) in enumerate(Cache_2):
                                if ( idts_array[i_ds] == IDTS and id_array[i_ds] == ID ):
                                    Cache_1.idx_ds[idx_C1] = i_ds
                                    Cache_2__delete_idx_list.append(i_C2)
                                    # count particles found for the first time
                                    if not self.Particles[particle_name][Cache_1.idx_sp[idx_C1]]:
                                        n_p__new += 1
                            # delete found particles from Cache_2.
                            Cache_2.delete(Cache_2__delete_idx_list)
                            # if all particles in Cache_2 have been found
                            # stop iteration over the datset
                            if not Cache_2:
                                log_message += '| stop @ i_ds = %i' % i_ds
                                break
                    else:
                        log_message += '| no dset iterations'
                    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    # particles not found in the dataset:
                    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    # Cache_1 idxs of particles not found at current time step
                    Cache_1__delete_idx_list = Cache_2.idx_C1[:]
                    # Cache_0 idxs of particles not found at current time step
                    Cache_0__delete_idx_list = [ Cache_1.idx_C0[i] \
                                                 for i in Cache_1__delete_idx_list ]
                    # delete particles from Cache_0 and Cache_1
                    Cache_0.delete( Cache_0__delete_idx_list )
                    Cache_1.delete( Cache_1__delete_idx_list )
                    # number of particles gone at the current timestep
                    n_p__gone = n_p__found_last_time - len(Cache_1) + n_p__new
                    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    # particles found in the dataset:
                    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    # do the rest only for found particles
                    if Cache_1:
                        sample_dict = dict(name='selected',idxs=Cache_1.idx_ds[:])
                        # fetch their attributes
                        xp.read(i_ts,sample_dict)
                        # store attributes in the output structure
                        for i,(idx_sp,idx_ds) in enumerate(zip(Cache_1.idx_sp,Cache_1.idx_ds)):
                            self.Particles[particle_name][idx_sp].X.append( xp.x[i] )
                            self.Particles[particle_name][idx_sp].P.append( xp.p[i] )
                            self.Particles[particle_name][idx_sp].timeshot.append( i_ts )
                            self.Particles[particle_name][idx_sp].idx_ds.append( idx_ds )
                    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    # print log message
                    print 'step=%3i (%3i) i_ts=%4i  ' % (i_ts_iter_step+1, len(idxs_ts), i_ts),
                    print 'found particles:%2i (%2i)  new:%2i  gone:%2i %s' % \
                          (len(Cache_1),
                           n_p__search,
                           n_p__new,
                           n_p__gone,
                           log_message)
                    n_p__found_last_time = len(Cache_1) 
                    # if there is no particles in Cache_1 and no particle
                    # in SP to be added later -- stop Timestep iterations
                    if i_SP==len(SP) and not Cache_1:
                        print 'no particles found @ i_ts = %i, stop timestep iterations!' % i_ts
                        break 




class _particles_Cache_Base:
    """
    Base class for particles Caches
    """
    def __init__(self):
        self.IDTS   = []
        self.ID     = []
        self._idxs  = [] # indexies used for deletion operation
    def delete(self,idxs):
        # check idxs and stire it in self.idx
        self._idxs = set( [ i if i>=0 else len(self)-1  for i in idxs ] )
        if self._idxs.difference(range(len(self))): raise IndexError
        # delete elements from lists
        self.IDTS = [ v  for i,v in enumerate(self.IDTS)  if i not in self._idxs ]
        self.ID   = [ v  for i,v in enumerate(self.ID)    if i not in self._idxs ]
    def __len__(self):
        return len(self.IDTS)

class _particles_Cache_0(_particles_Cache_Base):
    """
    Cache with IDs of particle which can be peresent at the
    current time step
    """
    def __init__(self):
        _particles_Cache_Base.__init__(self)
        self.idx_sp = []  # index in Selected_Particles array
    def append(self, SP,i_sp):
        "Append particle from tdc_Selected_Particles"
        self.IDTS.append(SP[i_sp][0])
        self.ID.append(  SP[i_sp][1])
        self.idx_sp.append(i_sp)
    def delete(self,idxs):
        _particles_Cache_Base.delete(self, idxs)
        self.idx_sp = [ v  for i,v in enumerate(self.idx_sp)  if i not in self._idxs ]
    def __getitem__(self, i):
        return (self.IDTS[i], self.ID[i], self.idx_sp[i])

class _particles_Cache_1(_particles_Cache_0):
    """
    Cache with IDs for particles found at each timerstep 
    """
    def __init__(self):
        _particles_Cache_0.__init__(self)
        self.idx_ds = [] # index in HDF file datasets
        self.idx_C0 = [] # index in particles_Cache_0
    def append(self, Cache_0,i_C0):
        "Append particle from particles_Cache_0"
        self.IDTS.append( Cache_0.IDTS[i_C0] )
        self.ID.append(   Cache_0.ID[i_C0]  )
        self.idx_sp.append( Cache_0.idx_sp[i_C0] )
        self.idx_ds.append(None)
        self.idx_C0.append(i_C0)
    def delete(self,idxs):
        _particles_Cache_0.delete(self, idxs)
        self.idx_ds = [ v  for i,v in enumerate(self.idx_ds)  if i not in self._idxs ]
        self.idx_C0 = [ v  for i,v in enumerate(self.idx_C0)  if i not in self._idxs ]
    def __getitem__(self, i):
        return (self.IDTS[i],self.ID[i],self.idx_sp[i],self.idx_ds[i],self.idx_C0)

class _particles_Cache_2(_particles_Cache_Base):
    """
    Cache with particles' IDs used during actual particle search;
    it shrinks when particle is found
    """
    def __init__(self, Cache_1):
        "Initialize from particles_Cache_1"
        _particles_Cache_Base.__init__(self)
        self.IDTS   = Cache_1.IDTS[:]
        self.ID     = Cache_1.ID[:]
        self.idx_C1 = range(len(Cache_1)) # index in particles_Cache_1            
    def delete(self,idxs):
        _particles_Cache_Base.delete(self, idxs)
        self.idx_C1 = [ v  for i,v in enumerate(self.idx_C1)  if i not in self._idxs ]
    def __getitem__(self, i):
        return (self.IDTS[i], self.ID[i], self.idx_C1[i])


