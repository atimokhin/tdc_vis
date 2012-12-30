import matplotlib
import pickle

from ATvis.Common_Data_Plot import AT_Manip

from Auxiliary import tdc_Filenames


class tdc_Manip(AT_Manip):
    """
    Base class for TDC Manipulators
    implements dump_data with correct filenames
    """

    def __init__(self, fig_param=None):
        AT_Manip.__init__(self,fig_param)

    def dump_data(self,filename,dump_id):
        """
        get pure data from plotter and dump it into the pickle file
           'tdc_Filenames.__VisResultsDir/dump_id/filename.pickle' 
        """
        # get pure data copy
        data = [ d.get_pure_data_copy() for d in self.plotter.data ]
        # full file name of the file with manipulator dump
        filename=tdc_Filenames.get_full_vis_filename(dump_id, filename+'.pickle')
        pickle.dump( data, open(filename,'w') )
        print '\nContent dumped in "%s" \n' % filename



class tdc_Manip_Plot_vs_X(tdc_Manip):
    """
    Manipulators for plots vs x-coordinate
    Adds:
    - switching between X and CELL coordinates
    - switching between CELL boundaries ON/OFF
    """

    def to_cell_coordinates(self):
        """
        Convert CURRENT plot to cell cordinates
        """
        self.plotter.to_cell_coordinates(self.ax)
        self.plotter.replot(self.ax)
        self.plotter.cells.draw(self.ax)
        self.x_label.set_text(self.plotter.plot_xlabel)
        self.fig.canvas.draw()

    def to_x_coordinates(self):
        """
        Convert CURRENT plot to x cordinates
        """
        self.plotter.to_x_coordinates(self.ax)
        self.plotter.replot(self.ax)
        self.plotter.cells.draw(self.ax)
        self.x_label.set_text(self.plotter.plot_xlabel)
        self.fig.canvas.draw()
        
    def cells_on(self):
        """
        Shows cell boundaries on the CURRENT plot
        """
        self.plotter.cells_on(self.ax)
        self.fig.canvas.draw()

    def cells_off(self):
        """
        Deletes cell boundaries from the CURRENT plot
        """
        self.plotter.cells_off(self.ax)
        self.fig.canvas.draw()

