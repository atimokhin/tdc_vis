import numpy as np

from tdc_field_data import tdc_Field_Data

class tdc_Fields_Diff_Data:
    
    __default_Filename = 'fields.h5'

    def __init__(self,
                 calc_id,
                 field1_name,
                 field2_name,
                 time_normalization=None,
                 ghost_points=False,
                 filename=__default_Filename):

        self.fd1 = tdc_Field_Data(calc_id,
                                  field1_name,
                                  time_normalization=time_normalization,
                                  ghost_points=ghost_points,
                                  filename=filename)
        self.fd2 = tdc_Field_Data(calc_id,
                                  field2_name,
                                  time_normalization=time_normalization,
                                  ghost_points=ghost_points,
                                  filename=filename)

        # setup class variables ----------
        # store calc_id
        self.calc_id=calc_id
        # store field name
        self.name = field1_name + ' - ' + field2_name
        # read ghost points?
        self.ghost_points=ghost_points
        # open HDF file ------------------
        self.file_id=self.fd1.file_id
        # Initialize Timetable -----------
        self.timetable = self.fd1.timetable
        # set other members to None ------
        self.x    = None
        self.f    = None
        self.i_ts = None
        
    def read(self, i_ts, re_read_x=False,**kwargs):
        self.fd1.read(i_ts, re_read_x=re_read_x,**kwargs)
        self.fd2.read(i_ts, re_read_x=re_read_x,**kwargs)
        self.f =  self.fd1.f-self.fd2.f
        self.x =  self.fd1.x
        self.i_ts = i_ts
