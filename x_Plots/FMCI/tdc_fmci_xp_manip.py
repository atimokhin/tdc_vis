import numpy as np
import matplotlib
import pickle

from Auxiliary        import tdc_Setup_Props, tdc_Filenames
from Common_Data_Plot import tdc_Manip

from FMCI.tdc_fmci_xp_partition  import tdc_FMCI_XP_Partition__LinSemiLogUniform
from FMCI.tdc_fmci_xp_data       import tdc_FMCI_XP_Data_Base, tdc_FMCI_XP_Data
from FMCI.tdc_fmci_xp_plotter    import tdc_FMCI_XP_Plotter


class tdc_FMCI_XP_Manip(tdc_Manip):
    """
    Manipulator class for FMCI_XP
    """

    __default_XP_partition = None
    __default_wlims = [1e-2,1e2 ]
    
    def __init__(self,fig_param=None):
        # leve more place for y label
        tdc_Manip.__init__(self,fig_param)

    @staticmethod
    def init_from_data(calc_id,
                       i_ts,
                       particle_name, 
                       xp_partition=None,
                       wlims=None,
                       fig_param=None):
        """
        Setup Manip by reading original data

        --------
        Arguments:
        --------
        calc_id
          calculation id name
        i_ts
           timeshot#
        particle_name
           name of particles whose distribution function will be plotted
        --------
        Options:
        --------
        xp_partition
        wlims
          <None> -- interval for particle weights [wmin,wmax] to be plotted 
                    as distinct colors according the current color map
                    if None, use the default value stored at class initialization
        --------
        """
        manip=tdc_FMCI_XP_Manip(fig_param)
        manip.read_from_data(calc_id,
                             i_ts,
                             particle_name, 
                             xp_partition=xp_partition,
                             wlims=wlims)
        return manip


    @staticmethod
    def init_from_ascii(filename,
                        dump_id,
                        wlims=None,
                        fig_param=None):
        """
        Setup Manip from ascii data file
        filename
           ascii file name is 'filename.dat'
        """
        manip=tdc_FMCI_XP_Manip(fig_param)
        manip.read_from_ascii(filename,
                              dump_id,
                              wlims=wlims)
        return manip


    @staticmethod
    def init_from_dump(filename,
                       dump_id,
                       wlims=None,
                       fig_param=None):
        """
        Setup Manip from dumped data
        filename
           pickle file name is 'filename.pickle'
        """
        manip=tdc_FMCI_XP_Manip(fig_param)
        manip.read_from_dump(filename,
                             dump_id,
                             wlims=wlims)
        return manip


    def read_from_data(self, 
                       calc_id,
                       i_ts,
                       particle_name, 
                       xp_partition=None,
                       wlims=None):
        """
        setup Manip by reading the original data file
        --------
        Arguments
        --------
        particle_name
                  name of particle which distribution will be plotted
        --------
        Options:
        --------
        xp_partition
           <None> -- XP domain partiction to use for fmci_XP
        wlims
           <None> -- interval for particle weights [wmin,wmax] to be plotted 
        """        
        # default xp_partition <<<<<<<<<<<<<<<<<<<<<<
        if not xp_partition:
            xp_partition=tdc_FMCI_XP_Partition__LinSemiLogUniform( x_dict=dict(n=120,xx=None),
                                                                   p_dict=dict(n=50,pp=[1,5e8]) )
        # default wlims
        if not wlims:
            wlims=self.__default_wlims
        # FMCI_XP <<<<<<<
        self.fmci_xp=tdc_FMCI_XP_Data(calc_id, particle_name, xp_partition)
        # set PLOTTER by calling base class method
        self.set_plotter( tdc_FMCI_XP_Plotter(self.fmci_xp, wlims) )
        # read data
        self.read(i_ts)


    def read_from_dump(self,
                       filename,
                       dump_id,
                       wlims=None):
        """
        setup Manip by reading the pickle'd data dumped
        into data file dump_id/filename.pickle
        --------
        Options:
        --------
        wlims
           <None> -- interval for particle weights [wmin,wmax] to be plotted 
        """
        # set restored_from_dump flag so the data cannot be read again
        self.restored_from_dump=True
        # fmci_XP DATA <<<<<<<
        # full file name of the file with manipulator dump
        filename=tdc_Filenames.get_full_vis_filename(dump_id, filename+'.pickle')
        self.fmci_xp = pickle.load( open(filename,'r') )[0]
        # i_ts
        self.i_ts = self.fmci_xp.i_ts
        # default wlims
        if not wlims:
            wlims=self.__default_wlims
        # set PLOTTER by calling base class method
        self.set_plotter( tdc_FMCI_XP_Plotter(self.fmci_xp, wlims) )


    def read_from_ascii(self, 
                        filename,
                        dump_id,
                        wlims=None):
        """
        setup Manip by reading the data saved as ascii
        into data file dump_id/filename.dat
        """
        # set restored_from_dump flag so the data cannot be read again
        ## self.restored_from_dump=True
        # full file name of the file with tdc_FMCI_XP_Data_Base info
        filename=tdc_Filenames.get_full_vis_filename(dump_id, filename+'.dat')
        self.fmci_xp = tdc_FMCI_XP_Data_Base.init_from_ascii(filename)
        # i_ts
        self.i_ts = self.fmci_xp.i_ts
        # default wlims
        if not wlims:
            wlims=self.__default_wlims
        # set PLOTTER by calling base class method
        self.set_plotter( tdc_FMCI_XP_Plotter(self.fmci_xp, wlims) )


    def save_to_ascii(self, 
                      filename,
                      dump_id):
        # full file name of the file with manipulator dump
        filename=tdc_Filenames.get_full_vis_filename(dump_id, filename+'.dat')
        self.fmci_xp.save_to_ascii(filename)


    def __repr__(self):
        s = self._manip_name('tdc_FMCI_XP_Manip')
        s += ' default wlims : [%g, %g]\n\n' % tuple(self.__default_wlims)
        s += 'FMCI_XP => %s\n' % str(self.fmci_xp)
        return s


    def plot(self,
             wlims=None,
             ylim=None,
             xlim=None,
             print_id=False,
             **kwargs):
        """
        Plot Color map of array fmci_XP for already set i_ts and xp_partition
        ----------
        Options:
        ----------
        wlims
           <None> -- interval for particle weights [wmin,wmax] to be plotted 
                     as distinct colors according the current color map
                     if None, use the default value stored at class initialization
        ylim |    
        xlim |    -- axes limits
        print_id  -- print label on the plot? <False>
        """
        # Create figure and axes -----------
        self.create_figure_and_axes()
        # id label
        id_label = 'i_ts=%i:' % self.i_ts + self.plotter.plot_idlabel          
        # if asked put widnow title label  into figure too
        if print_id:
            self.fig.suptitle(id_label, size='x-small')
        id_label = 'Fig %i|' % self.fig.number + id_label
        self.fig.canvas.set_window_title(id_label) 
        # PLOT --------------------------------------
        self.plotter.plot(self.ax,wlims=wlims,**kwargs)
        # set axes limits:
        # xlim -- if not set use the whole x range 
        if xlim!=None:
            self.ax.set_xlim(xlim)
        # ylim -- if not set use automatic setting 
        if ylim!=None:
            self.ax.set_ylim(ylim)
        # labels
        if matplotlib.rcParams['text.usetex']:
            self.set_ylabel(self.plotter.plot_ylabel_latex)
        else:
            self.set_ylabel(self.plotter.plot_ylabel)
        self.set_xlabel(self.plotter.plot_xlabel)
        # change ticklabel_fonsize
        self._change_ticklabel_fonsize()

    def set_xp_partition(self,xp_partition):
        self.fmci_xp.set_xp_partition(xp_partition)

    def fill_fmci_XP_array(self):
        self.fmci_xp.fill_fmci_XP_array()
