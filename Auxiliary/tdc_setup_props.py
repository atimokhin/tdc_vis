import h5py

from tdc_filenames  import tdc_Filenames

class tdc_Setup_Props(object):
    """
    This class contains information from setup_properties.h5 file
    NB: redirects all non-defined requests to self.file_id
    Members:
    -------
    file_id
       h5py.File instance with setup_properties.h5 data
    """

    __default_Filename = 'setup_properties.h5'
    
    def __init__(self, calc_id):
        h5_filename=tdc_Filenames.get_full_filename(calc_id, self.__default_Filename)
        self.file_id = h5py.File(h5_filename)

    def __getattr__(self,attrname):
        return getattr(self.file_id,attrname)

    def get_papam(self,dataset_name):
        "return paparm stored in dataset with the name *dataset_name*"
        return self.file_id[dataset_name].value

    def get_xmin_xmax(self):
        "computational region boundaries"
        return (0,self.get_papam('/GridProps/L'))
