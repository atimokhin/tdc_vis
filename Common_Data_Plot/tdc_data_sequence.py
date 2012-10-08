from Auxiliary import tdc_get_bound_index

from tdc_sequence import tdc_Sequence

class tdc_Data_Sequence(tdc_Sequence):
    """
    Members:
    array__time       - array with continuous time of all ids
    array__i_calc_id  - contains id of the corresponding sequence index
    array__i_timeshot - contains number of local to the curresponding id timeshot number

    data - array with data (single class instance for each individual id)

    idx_seq__start
    idx_seq__end

    all non-implemented methods/members are redirected to the CURRENT data!
    current data are set after call to read(iseq)
    """

    def __init__(self, data, tt=None):
        """
        data
           sequence with tdc_*_Data class instances 
        tt
           time interval <[t1,<t2>]>
        """
        # arrays for sequence information storage --
        self.array__data       = []
        self.array__time       = []
        self.array__i_calc_id  = []
        self.array__i_timeshot = []
        # ------------------------------------------
        # data class instances ---------------------
        if not isinstance( data, (tuple,list)): 
            data=(data,)
        self.array__data = data[:]
        # ------------------------------------------
        # initialize array__time  and  array__i_calc_id
        for i_calc_id,data_entry in enumerate(self.array__data):
            timearray = data_entry.timetable.get_time_array()
            self.array__i_calc_id.extend(  [ i_calc_id for i in timearray ] )
            self.array__i_timeshot.extend( range(1,len(timearray)+1,1)      )
            self.array__time.extend(       timearray                        )
        # --------------------------------------------
        # initialize start and end sequence indexies
        self.idx_seq__start = 0
        self.idx_seq__end   = len(self.array__i_timeshot)-1
        # if time argument is given
        if tt is not None:
            # be sure t is tuple or list
            if not isinstance( tt, (list,tuple) ): tt = (tt,)
            # for non-default t set limits
            if len(tt) == 1:
                self.idx_seq__start = tdc_get_bound_index( tt[0], self.array__time )
            elif len(tt) == 2:
                self.idx_seq__start = tdc_get_bound_index( tt[0], self.array__time )
                self.idx_seq__end   = tdc_get_bound_index( tt[1], self.array__time )
        # -------------------------------------------
        # CURRENT data ------------------------------
        self.current_data = self.array__data[0]
        self.i_calc_id = None
        self.i_ts      = None
        # -------------------------------------------

    @staticmethod
    def init_from_data(data_class, calc_ids, tt=None, **kwargs):
        """
        Intialized data sequence from list of calc_ids and tdc_*_Data class

        data_class
           tdc_*_Data class for data intialization
        calc_ids
           calculation ids
        tt
           time interval <[t1,<t2>]>

        data class for each id is initialized as data_class(*args, **kwargs)
        """
        # initialize data classes ------------------
        if not isinstance( calc_ids, (list,tuple) ):
            calc_ids = (calc_ids,)
        data = [ data_class(calc_id, **kwargs) for calc_id in calc_ids ]
        # initialize base class
        return tdc_Data_Sequence(data,tt=tt)
                
    def __getattr__(self,attrname):
        "Redirects all non-mplemented requests to the current data class"
        return getattr(self.current_data,attrname)

    def read(self,i_seq, **kwargs):
        """
        Perform read operation for the data corresponding to the
        desired i_seq

        and set current data according to i_seq
        """
        self.current_data, self.i_calc_id, self.i_ts = \
                           self._get_data_id_timeshot__for_i_seq(i_seq)
        self.current_data.read(self.i_ts, **kwargs)


    def get__id(self):
        "()=>id  current"
        return self.i_calc_id

    def get__i_ts(self):
        "()=>i_timeshot current"
        return self.i_ts

    def get_sequence_length(self):
        return self.idx_seq__end-self.idx_seq__start+1


    def _get_data_id_timeshot__for_i_seq(self,i_seq):
        """
        for given position in the squence i_seq:
        () => data, calc_id, timeshot
        """
        seq_idx    = self.idx_seq__start + i_seq - 1
        i_calc_id  = self.array__i_calc_id[seq_idx]
        i_timeshot = self.array__i_timeshot[seq_idx]
        return self.array__data[i_calc_id], i_calc_id, i_timeshot

