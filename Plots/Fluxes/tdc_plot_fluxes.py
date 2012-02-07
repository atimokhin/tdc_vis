from Common_Data_Plot import tdc_Manip

from Fluxes.tdc_flux_data       import tdc_Flux_Data
from Fluxes.tdc_fluxes_plotter  import tdc_Fluxes_Plotter


def tdc_plot_fluxes( calc_ids,
                     flux_name,
                     prefix=None,
                     ylim=None,
                     xlim=None,
                     print_id=False,
                     no_plot=False,
                     fig_param=None):
    """
    calc_ids
       calculation ids 
    flux_name
       name of the flux to be plotted (dataset name in HDF file)
    prefix
       ns|lc -- by default both ns and lc fluxes will be plotted

    Options:
    --------
    xlim
       <None> X axis limits
    ylim
       <None> Y axis limits
    print_id
       <False> whether to put id label on the figure
    no_plot
       <False> if True do not call plot in Manipulator
       useful if additional plot modifications are required
    """       
    manip = tdc_Flux_Manip(fig_param)
    manip.setup_from_data(calc_ids, flux_name, prefix)
    if not no_plot:
        manip.plot(ylim, xlim, print_id)
    return manip


def tdc_plot_fluxes_restored(filename,
                             dump_id,
                             ylim=None,
                             xlim=None,
                             print_id=False,
                             no_plot=False,
                             fig_param=None):
    """
    filename
       pickle file name is 'filename.pickle'
    Options:
    --------
    print_id
       <False> whether to put id label on the figure
    no_plot
       <False> if True do not call plot in Manipulator
       useful if additional plot modifications are required
    Returns:
    --------
    ()=> tdc_Flux_Manip
    """
    # create Manip
    manip = tdc_Flux_Manip(fig_param)
    manip.restore(filename,dump_id)
    if not no_plot:
        manip.plot(ylim, xlim, print_id)
    return manip


class tdc_Flux_Manip(tdc_Manip):
    """
    Manipulator class for Fluxes
    """
    __default_prefix = ('lc','ns')

    def __init__(self,fig_param=None):
        tdc_Manip.__init__(self, fig_param)

    def setup_from_data(self,
                        calc_ids,
                        flux_name,
                        prefix=None):
        # fluxes
        self.fluxes = dict()
        # prefix
        if not prefix:
            prefix = self.__default_prefix
        # make shure prefix is a tuple
        if not isinstance(prefix, (list,tuple)):
            prefix = (prefix,)
        for pref in prefix:
            self.fluxes[pref] = tdc_Flux_Data(calc_ids, flux_name, pref)
        # set PLOTTER by calling base class constructor
        # with tdc_XPs_Plotter instanse
        self.set_plotter( tdc_Fluxes_Plotter( self.fluxes.values() ) )

    def restore(self,
                filename,
                dump_id):
        """
        setup Manip by reading the pickle'd data dumped
        by Manip called before
        """
        import pickle
        from   Auxiliary import tdc_Filenames
        # set restored_from_dump flag so the data cannot be read again
        self.restored_from_dump=True
        # Flux DATA <<<<<<<
        # full file name of the file with manipulator dump
        filename=tdc_Filenames().get_full_vis_filename(dump_id, filename+'.pickle')
        self.fluxes = pickle.load( open(filename,'r') )
        # set PLOTTER by calling base class method
        self.set_plotter( tdc_Fluxes_Plotter( self.fluxes.values() ) )

    def dump_data(self,filename,dump_id):
        """
        get pure data from plotter and dump it into the pickle file filename.pickle 
        """
        import pickle
        from   Auxiliary import tdc_Filenames
        fluxes = self.fluxes
        for pref in fluxes.keys():
            fluxes[pref] = fluxes[pref].get_pure_data_copy()
        # full file name of the file with manipulator dump
        filename=tdc_Filenames().get_full_vis_filename(dump_id, filename+'.pickle')
        pickle.dump( fluxes, open(filename,'w') )
        print '\nContent dumped in "%s" \n' % filename

    def __repr__(self):
        s = self._manip_name('tdc_Flux_Manip')
        s += 'calc_ids = %s\n' %  str(self.fluxes[ self.fluxes.keys()[0] ].calc_ids)
        s += '\nFluxes:\n'
        for f in self.fluxes.values():
            s += '\n' + str(f)
        return s

    def plot(self,
             ylim=None,
             xlim=None,
             print_id=False,
             **kwargs):
        """
        Do normal linear plot
        """
        self.__general_plot(self.plotter.plot,
                            ylim, xlim,
                            print_id,
                            **kwargs)

    def semilogy(self,
                 ylim=None,
                 xlim=None,
                 print_id=False,
                 **kwargs):
        """
        Do semilogy plot
        """
        self.__general_plot(self.plotter.semilogy,
                            ylim, xlim,
                            print_id,
                            **kwargs)

    def set_time(self,tt):
        "Set working time domain"
        for f in self.fluxes.values():
            f.set_time(tt)

    def smooth(self,window_len=10,window='flat'):
        """
        Smooth flux distribution
        window_len  -- length of the window
        window      -- window type
        """
        for f in self.fluxes.values():
            f.smooth(window_len,window)
    
    def mean(self,tt=None):
        """
        Return dictionary with mean fluxes
        """
        mean_flux = dict()
        for prefix in self.fluxes:
            mean_flux[prefix] = self.fluxes[prefix].mean(tt)
        return mean_flux


    def __general_plot(self, plot_function,
                       ylim=None, xlim=None,
                       print_id=False,
                       **kwargs):
        """
        Common function teplate for plot operation
        plot_function
           All plotting is done via plot_function
        ylim
        xlim 
           axes limits
        print_id
           print label on the plot? <False>
        """
        # Create figure and axes -----------
        self.create_figure_and_axes()
        # id_label        
        id_label = self.plotter.plot_idlabel+' : '
        for prefix in  self.fluxes.keys():       
            id_label += prefix + ' '
        self.fig.canvas.set_window_title(id_label) 
        # plot <----------------
        plot_function(self.ax)
        # ----------------------
        # set axes limits:
        if xlim:
            self.ax.set_xlim(xlim)
        # ylim -- if not set use automatic setting 
        if ylim:
            self.ax.set_ylim(ylim)
        # labels
        self.set_ylabel(self.plotter.plot_ylabel)
        self.set_xlabel(self.plotter.plot_xlabel)
        # change ticklabel_fonsize
        self._change_ticklabel_fonsize()
