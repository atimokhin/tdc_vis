from abc import ABCMeta, abstractmethod, abstractproperty

class tdc_Sequence(object):
    """
    Base class for sequeces compartible with tdc Movie 
    """
    __metaclass__ = ABCMeta
    @abstractmethod
    def read(self,i_seq, **kwargs):
        "Perform read operation for the data[i_seq]"
        pass
    @abstractmethod
    def get__id(self):
        "()=>id  current"
        pass
    @abstractmethod    
    def get__i_ts(self):
        "()=>i_ts current"
        pass
    @abstractmethod    
    def get_sequence_length(self):
        "()=>length of the sequence"
        pass
        
        
