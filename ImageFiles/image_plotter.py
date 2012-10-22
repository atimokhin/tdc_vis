from numpy import *

from Common_Data_Plot import tdc_Data_Plotter

class Image_Plotter(tdc_Data_Plotter):
    """
    Display image read from file
    """
    
    def __init__(self, image_data, idlabel=None):
        """
        Sets internal variables 
        image_data -- Image_Data with image to be plotted
        limits variables
        """
        # base class initialization is enough
        tdc_Data_Plotter.__init__(self,image_data,None,None,None)
        # labels -----------------------
        # idlabel
        if not idlabel:
            self.plot_idlabel='Image:' + self.data[0].image_filename
        # ---------------------------------
        # initialize lines
        self.lines = [ None ]
        
    def plot(self,
             ax,            
             **kwargs):
        """
        Plot image onto axes ax
        ----------
        Arguments:
        ----------
        ax
        **kwargs goes to ax.plot(..)
        """
        self.lines[0] = ax.imshow(self.data[0].image, **kwargs)
            
            
    def replot(self,ax):
        """
        Plot new colormap, *does not change colorbar* 
        """
        self.lines[0] = ax.imshow(self.data[0].image)
        ax.draw_artist(self.lines[0])

    def update_plot(self,ax):
        """
        Plot call replot
        """
        self.replot(ax)

    def set_animated(self,val):
        """
        Set animated property in all lines
        """
        for line in self.lines:
            line.set_animated(val)

            

