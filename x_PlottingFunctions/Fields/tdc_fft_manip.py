import matplotlib.pyplot as plt

from Common_Data_Plot  import tdc_Manip
from Fields            import tdc_FFT_Data, tdc_FFT_Plotter, tdc_FFT_Fit, tdc_FFT_Fit_Plotter


class tdc_FFT_Manip(tdc_Manip):
    """
    Manipulator class for Furier transform plot of a field
    """

    def __init__(self,fig_param=None):
        tdc_Manip.__init__(self,fig_param)
        # FFT Data <<<<<<<
        self.fft=None
        self.fft_fit=None
        self.fft_fit_plotter=None

        
    @staticmethod
    def init_from_data(calc_id,
                       i_ts,
                       field_name,
                       xx=None,
                       fitting_type='pl',
                       nk_plot=20,
                       fig_param=None):
        """
        Setup Manip by reading original data

        calc_id
           calculation id name
        field_name
           name of the field which Fourier transform will be plotted
        i_ts
           timeshot#
        -------
        Options:
        --------
        nk_plot
           <20> length of plotting arrays
        fitting_type
           <'pl'>
        fig_param
        --------
        """
        manip=tdc_FFT_Manip(fig_param)
        manip.read_from_data(calc_id,
                             i_ts,
                             field_name,
                             xx=xx,
                             fitting_type=fitting_type,
                             nk_plot=nk_plot)
        return manip

    
    @staticmethod
    def init_from_dump(filename,
                       dump_id,
                       fig_param=None):
        """
        Setup Manip from dumped data
        filename
           pickle file name is 'filename.pickle'
        """
        manip=tdc_FFT_Manip(fig_param)
        manip.read_from_dump(filename, dump_id)
        return manip

  
    def read_from_data(self,
                       calc_id,
                       i_ts,
                       field_name,
                       xx,
                       fitting_type,
                       nk_plot):
        """
        setup Manip by reading the original data file
        """
        # FFT <<<<<<<
        self.fft = tdc_FFT_Data(calc_id,
                                field_name,
                                xx=xx)
        # set PLOTTER by calling base class method
        self.set_plotter( tdc_FFT_Plotter(self.fft) )
        # FFT Fit <<<<<<<
        self.set_fft_fit(fitting_type=fitting_type, nk_plot=nk_plot)
        # read data
        self.read(i_ts)

        
    def read_from_dump(self,filename,dump_id):
        """
        setup Manip by reading the pickle'd data dumped
        by Manip called before
        """
        import pickle
        from   Auxiliary import tdc_Filenames
        # set restored_from_dump flag so the data cannot be read again
        self.restored_from_dump=True
        # Field <<<<<<<
        # full file name of the file with manipulator dump
        filename=tdc_Filenames.get_full_vis_filename(dump_id, filename+'.pickle')
        dump_dict = pickle.load( open(filename,'r') )
        self.fft = dump_dict['fft_data'][0]
        # i_ts
        self.i_ts = self.fft.field.i_ts
        # set PLOTTER by calling base class method
        self.set_plotter( tdc_FFT_Plotter( self.fft ) )
        # FFT Fit <<<<<<<
        self.set_fft_fit(fitting_type=dump_dict['fitting_type'],
                         nk_plot=dump_dict['nk_plot'])

    def dump_data(self,filename,dump_id):
        """
        get pure data from plotter and dump it into the pickle file filename.pickle 
        """
        import pickle
        from   Auxiliary import tdc_Filenames
        data = [ d.get_pure_data_copy() for d in self.plotter.data ]
        dump_dict={}
        dump_dict['fft_data'] = data
        dump_dict['fitting_type'] = self.fft_fit.type 
        dump_dict['nk_plot']   = self.fft_fit.nk_plot
        # full file name of the file with manipulator dump
        filename=tdc_Filenames.get_full_vis_filename(dump_id, filename+'.pickle')
        pickle.dump( dump_dict, open(filename,'w') )
        print '\nContent dumped in "%s" \n' % filename

    def __repr__(self):
        s = self._manip_name('tdc_FFT_Manip')
        s += '   calc_id = \"%s\"\n' % self.fft.calc_id
        s += 'field name = \"%s\"\n' % self.fft.name
        s += '      i_ts = %d\n'     % self.i_ts
        s += '      time = %s\n'     % self.fft.timetable
        s += str(self.fft_fit)
        return s

    def plot(self,
             ylim=None,
             xlim=None,
             print_id=False,
             **kwargs):
        """
        Plots SED for already already set i_ts, p_bins, xx
        accepts only
        ylim --    axes limits
        xlim |
        print_id  -- print label on the plot? <False>
        """
        # Create figure and axes -----------
        self.create_figure_and_axes()
        # id label
        id_label = 'i_ts=%i:xx=[%g, %g]:' % (self.i_ts,self.fft.xx[0],self.fft.xx[1]) +\
                   self.plotter.plot_idlabel          
        # if asked put widnow title label  into figure too
        if print_id:
            self.fig.suptitle(id_label, size='x-small')
        id_label = 'Fig %i|' % self.fig.number + id_label
        self.fig.canvas.set_window_title(id_label) 
        # PLOT --------------------------------------
        self.plotter.plot(self.ax)
        # set axes limits:
        # xlim -- if not set use the whole x range 
        if xlim!=None:
            self.ax.set_xlim(xlim)
        # ylim -- if not set use automatic setting 
        if ylim!=None:
            self.ax.set_ylim(ylim)
        # labels
        self.set_ylabel(self.plotter.plot_ylabel)
        self.set_xlabel(self.plotter.plot_xlabel)
        # change ticklabel_fonsize
        self._change_ticklabel_fonsize()


    def fit(self, kk=None):
        """
        fit Furier spectrum with function type set by set_fft_fit()
        """
        self.fft_fit.fit(kk)

    def show_fit(self):
        """
        Add curve with the spectrum fit to existing plot
        """
        self.fft_fit_plotter.plot(self.ax)
        plt.draw()

    def delete_fit(self):
        """
        Remove spectrum fit from existing plot
        """
        self.fft_fit_plotter.delete_plot(self.ax)
        plt.draw()
    
    def set_fft_fit(self, fitting_type='pl', nk_plot=20):
        """
        Setup spectrum fit
        """
        self.fft_fit = tdc_FFT_Fit(self.fft,
                                   fitting_type=fitting_type,
                                   nk_plot=nk_plot)
        # set PLOTTER by calling base class method
        self.fft_fit_plotter = tdc_FFT_Fit_Plotter( self.fft_fit )
        
