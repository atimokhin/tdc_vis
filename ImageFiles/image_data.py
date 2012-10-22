import os
import matplotlib.image as mpimg
import numpy as np
    
from Auxiliary import tdc_Exception

class Image_Data(object):
    """
    Class containing image dara reaf from graphic file
    image_data
    image_filename
    image_id
    i_im
    """

    default_image_filename_format = 'frame_%05d.png'

    def __init__(self):
        """
        Contains class members in one place
        """
        # data member
        self.image            = None
        self.image_filename   = None
        self.image_id         = None
        self.i_im             = None
        self.imagesize_points = []

        
    @staticmethod
    def init_from_file(filename, **kwargs):
        """
        return tdc_FMCI_XP_Data_Base instance initialized from ascii
        data file 'filename'
        """
        image_data=Image_Data()
        image_data.read_image(filename)
        return image_data

    def __repr__(self):
        s  = 'Image_Data:\n'
        s += 'image filename : %s\n' % self.image_filename
        s += '      image_id : %s\n' % self.image_id
        s += '          i_im : %s\n' % str(self.i_im)
        return s

    def read(self, 
             i_im, 
             filename_format=None):
        """
        read *image file* from the same directory as the current file
        """
        if self.image_filename is None:
            raise Exception("Image_Data: this class was not set up from an image file!")
        if filename_format is None:
            filename_format = self.default_image_filename_format 
        dirname = os.path.dirname(self.image_filename)
        filename = os.path.join(dirname, filename_format % i_im)
        if self.read_image(filename):
            self.i_im=i_im
            
    def read_image(self,filename):
        try:
            self.image=mpimg.imread(filename)
        except IOError:
            print "Image_Data: Can not read file \"%s\"\n" % filename
            return False
        self.imagesize_points = self.image.shape[1::-1]
        self.image_filename=filename
        self.image_id=os.path.basename(os.path.dirname(filename))
        return True
            
    def get_time(self):
        return 0        

        
