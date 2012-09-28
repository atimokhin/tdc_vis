import numpy as np
import matplotlib
import pickle

from Auxiliary        import tdc_Setup_Props, tdc_Filenames
from Common_Data_Plot import tdc_Manip

from FMCI.tdc_fmci_xp_partition  import tdc_FMCI_XP_Partition__LinSemiLogUniform
from FMCI.tdc_fmci_xp_data       import tdc_FMCI_XP_Data_Base, tdc_FMCI_XP_Data
from FMCI.tdc_fmci_mp_data       import tdc_FMCI_MP_Data
from FMCI.tdc_fmci_mp_plotter    import tdc_FMCI_MP_Plotter



class tdc_FMCI_MP_Manip(tdc_Manip):
    """
    Manipulator class for FMCI Metaparticles
    """

    __default_w_max = 100
    __default_m_max = 10
    
    def __init__(self,fig_param=None):
        # leve more place for y label
        tdc_Manip.__init__(self,fig_param)

        
    @staticmethod
    def setup_from_data(calc_id,
                        i_ts,
                        particle_name, 
                        xp_partition=None,
                        m_max=None,
                        w_max=None,
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
        manip=tdc_FMCI_MP_Manip(fig_param)
        manip.read_from_data(calc_id,
                             i_ts,
                             particle_name, 
                             xp_partition=xp_partition,
                             m_max=m_max,
                             w_max=w_max)
        return manip


    @staticmethod
    def setup_from_ascii(filename,
                         dump_id,
                         m_max=None,
                         w_max=None,
                         fig_param=None):
        """
        Setup Manip from ascii data file
        filename
           ascii file name is 'filename.dat'
        """
        manip=tdc_FMCI_MP_Manip(fig_param)
        manip.read_from_ascii(filename,
                              dump_id,
                              m_max=m_max,
                              w_max=w_max)
        return manip

    
    @staticmethod
    def setup_from_dump(filename,
                        dump_id,
                        fig_param=None):
        """
        Setup Manip from dumped data
        filename
           pickle file name is 'filename.pickle'
        """
        manip=tdc_FMCI_MP_Manip(fig_param)
        manip.read_from_dump(filename, dump_id)
        return manip


    
    def read_from_data(self, 
                       calc_id,
                       i_ts,
                       particle_name, 
                       xp_partition=None,
                       m_max=None,
                       w_max=None):
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
        # default m_max and w_max
        if m_max is None:
            m_max=self.__default_m_max
        if w_max is None:
            w_max=self.__default_w_max
        # FMCI_XP <<<<<<<
        fmci_xp=tdc_FMCI_XP_Data(calc_id, particle_name, xp_partition)
        self.fmci_mp = tdc_FMCI_MP_Data(fmci_xp, m_max=m_max, w_max=w_max)
        # set PLOTTER by calling base class method
        self.set_plotter( tdc_FMCI_MP_Plotter(self.fmci_mp) )
        # read data
        self.read(i_ts)

        
    def read_from_dump(self,
                       filename,
                       dump_id):
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
        filename=tdc_Filenames().get_full_vis_filename(dump_id, filename+'.pickle')
        self.fmci_mp = pickle.load( open(filename,'r') )[0]
        # i_ts
        self.i_ts = self.fmci_mp.fmci_xp.i_ts
        # set PLOTTER by calling base class method
        self.set_plotter( tdc_FMCI_MP_Plotter(self.fmci_mp) )

        

    def read_from_ascii(self, 
                        filename,
                        dump_id,
                        m_max=None,
                        w_max=None):
        """
        setup Manip by reading the data saved as ascii
        into data file dump_id/filename.dat
        """
        # default m_max and w_max
        if m_max is None:
            m_max=self.__default_m_max
        if w_max is None:
            w_max=self.__default_w_max
        # set restored_from_dump flag so the data cannot be read again
        self.restored_from_dump=True
        # full file name of the file with tdc_FMCI_XP_Data_Base info
        filename=tdc_Filenames().get_full_vis_filename(dump_id, filename+'.dat')
        fmci_xp = tdc_FMCI_XP_Data_Base().setup_from_ascii(filename)
        # setup metaparticles
        self.fmci_mp = tdc_FMCI_MP_Data(fmci_xp, m_max=m_max, w_max=w_max)
        self.fmci_mp.setup_metaparticles()
        self.fmci_mp.setup_markersize()
        # i_ts
        self.i_ts = fmci_xp.i_ts
        # set PLOTTER by calling base class method
        self.set_plotter( tdc_FMCI_MP_Plotter(self.fmci_mp) )

        
    def save_to_ascii(self, 
                      filename,
                      dump_id):
        # full file name of the file with manipulator dump
        filename=tdc_Filenames().get_full_vis_filename(dump_id, filename+'.dat')
        self.fmci_mp.fmci_xp.save_to_ascii(filename)

        
    def __repr__(self):
        s = self._manip_name('tdc_FMCI_MP_Manip')
        ## s += '        w_max : %g\n' % 
        ## s += 'FMCI_XP => %s\n' % str(self.fmci_xp)
        return s

    def plot(self,
             ylim=None,
             xlim=None,
             print_id=False,
             **kwargs):
        """
        Plot Color map of array fmci_XP for already set i_ts and xp_partition
        ----------
        Options:
        ----------
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
        self.plotter.plot(self.ax,**kwargs)
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

