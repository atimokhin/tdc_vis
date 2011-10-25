from Auxiliary import tdc_get_bound_index

class tdc_Data_Sequence:
    """
    Members:
    array__time       - array with continuous time of all ids
    array__i_calc_id  - contains id of the corresponding sequence index
    array__i_timeshot - contains number of local to the curresponding id timeshot number

    data - array with data (single class instance for each individual id)

    start_seq_idx
    end_seq_idx  

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
        if not isinstance( data, (tuple,list)): data=(data,)
        self.array__data = data[:]
        # ------------------------------------------
        # initialize array__time  and  array__i_calc_id
        for i_calc_id,data_entry in enumerate(self.array__data):
            timearray = data_entry.timetable.get_time_array()
            self.array__i_calc_id.extend(  [ i_calc_id for i in timearray ] )
            self.array__i_timeshot.extend( range(1,len(timearray)+1,1)      )
            self.array__time.extend(       timearray                        )
        # --------------------------------------------
        # initialize start_timeshot and end_timeshot        
        self.start_seq_idx = 0
        self.end_seq_idx   = len(self.array__i_timeshot)-1
        # if time argument is given
        if tt!=None:
            # be sure t is tuple or list
            if not isinstance( tt, (list,tuple) ): tt = (tt,)
            # for non-default t set limits
            if len(tt) == 1:
                self.start_seq_idx = tdc_get_bound_index( tt[0], self.array__time )
            elif len(tt) == 2:
                self.start_seq_idx = tdc_get_bound_index( tt[0], self.array__time )
                self.end_seq_idx   = tdc_get_bound_index( tt[1], self.array__time )
        # -------------------------------------------
        # CURRENT data ------------------------------
        self.current_data = self.array__data[0]
        self.i_calc_id = None
        self.i_ts      = None
        # -------------------------------------------


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
                           self.get_data_id_timeshot__for_i_seq(i_seq)
        self.current_data.read(self.i_ts, **kwargs)


    def get__i_id(self):
        "()=>id  current"
        return self.i_calc_id

    def get__i_timeshot(self):
        "()=>i_timeshot current"
        return self.i_ts

    def get_sequence_length(self):
        return self.end_seq_idx-self.start_seq_idx+1


    def get_data_id_timeshot__for_i_seq(self,i_seq):
        """
        for given position in the squence i_seq:
        () => data, calc_id, timeshot
        """
        seq_idx    = self.start_seq_idx + i_seq - 1
        i_calc_id  = self.array__i_calc_id[seq_idx]
        i_timeshot = self.array__i_timeshot[seq_idx]
        return self.array__data[i_calc_id], i_calc_id, i_timeshot


class tdc_Data_Sequence_Initializer(tdc_Data_Sequence):
    """
    Provides all tdc_Data_Sequence functionality
    but intialized data from list of calc_ids and tdc_*_Data class
    """

    def __init__(self, data_class, calc_ids, tt=None, **kwargs):
        """
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
        data = []
        for calc_id in calc_ids:
            data.append( data_class(calc_id, **kwargs) )
        # initialize base class
        tdc_Data_Sequence.__init__(self,data,tt=tt)

