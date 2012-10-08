from abc import ABCMeta, abstractmethod, abstractproperty
    
class tdc_Data(object):
    """
    Abstarct class for data classes which are compartible with
    standard tdc Movie and Manip 
    """
    __metaclass__ = ABCMeta
    @abstractmethod
    def read(self,i):
        pass
    @abstractmethod
    def get_time(self):
        pass
        
class tdc_Data__with_Timetable(object):
    """
    Base class for data classes with timetables 
    implements get_time() using timetable
    """
    def get_time(self):
        return self.timetable.get_time()
        
        
