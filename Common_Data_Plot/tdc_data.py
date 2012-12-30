            
class tdc_Data__with_Timetable(object):
    """
    Base class for data classes with timetables 
    implements get_time() using timetable
    """
    def get_time(self):
        return self.timetable.get_time()
        
        
