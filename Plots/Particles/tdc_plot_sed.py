import numpy as np

from Common  import tdc_Mesh,  tdc_Setup_Props
from Common  import tdc_Manip

from Particles.tdc_xp_data       import tdc_XP_Data
from Particles.tdc_sed_data      import tdc_SED_Data
from Particles.tdc_seds_plotter  import tdc_SEDs_Plotter


def tdc_plot_sed(calc_id, i_ts,
                 particle_names=None,
                 p_bins=None,
                 xx=None,
                 ylim=None,
                 xlim=None,
                 print_id=False,
                 no_plot=False,
                 **kwargs):
    """
    calc_id
       calculation id name
    i_ts
       timeshot#
    Options:
    --------
    particle_names
       name(s) of particles whose phase prtraits are to be plotted
    p_bins
    xx    
    xlim 
    ylim
       <None>  axis limits
    print_id
       <False> whether to put id label on the figure
    no_plot
       <False> if True do not call plot in Manipulator
       useful if additional plot modifications are required
    Returns:
    --------
    ()=> tdc_SED_Manip
    """
    manip = tdc_SED_Manip(**kwargs)
    manip.setup_from_data(calc_id,
                          particle_names,
                          p_bins,
                          xx,
                          **kwargs)
    manip.read(i_ts)
    if not no_plot:
        manip.plot(ylim, xlim, print_id)
    return manip


def tdc_plot_sed_restored(filename,
                          ylim=None,
                          xlim=None,
                          print_id=False,
                          no_plot=False,
                          **kwargs):
    """
    filename
       pickle file name is 'filename.pickle'
    Options:
    --------
    xlim 
    ylim
       <None>  axis limits
    print_id
       <False> whether to put id label on the figure
    no_plot
       <False> if True do not call plot in Manipulator
       useful if additional plot modifications are required
    Returns:
    --------
    ()=> tdc_XP_Manip
    """
    # create Manip
    manip = tdc_SED_Manip(**kwargs)
    manip.restore(filename)
    if not no_plot:
        manip.plot(ylim, xlim, print_id)
    return manip


class tdc_SED_Manip(tdc_Manip):
    """
    Manipulator class for SED
    """
    
    __default_particle_names = ['Electrons', 'Positrons', 'Pairs']
    __default_p_bins = (1,1e8,100)

    def __init__(self,**kwargs):
        tdc_Manip.__init__(self,**kwargs)

    def setup_from_data(self, calc_id,
                        particle_names=None, 
                        p_bins=None,
                        xx=None,
                        **kwargs):
        """
        setup Manip by reading the original data file
        """        
        # use default particle_names if not set in arguments
        if not particle_names:
            particle_names = self.__default_particle_names
        # make sure particle_names is a sequence
        if not isinstance( particle_names, (list,tuple) ):
            particle_names = (particle_names,)
        # default energy bins
        if not p_bins:
            p_bins=self.__default_p_bins
        # SEDs <<<<<<<
        self.seds=[]
        for pname in particle_names:
            self.seds.append( tdc_SED_Data( calc_id,
                                            particle_name=pname,
                                            p_bins=p_bins,
                                            xx=xx) )
        # set PLOTTER by calling base class method
        self.set_plotter( tdc_SEDs_Plotter(self.seds) )
        # setup normalization constants
        setup_props = tdc_Setup_Props(calc_id)
        self.OmegaPl     = setup_props.get_papam('PlasmaProps/OmegaPl')
        self.LambdaDebye = setup_props.get_papam('PlasmaProps/LambdaDebye')
        # initialize plasma params to empty dictionary
        self.plasma_params = {}
        # initialize number of particles dictionary
        self.n_p = {}
        # get Mesh
        self._Mesh = self.seds[0].xp._Mesh

    def restore(self,
                filename,
                p_bins=None,
                xx=None):
        """
        setup Manip by reading the pickle'd data dumped
        by Manip called before
        """
        import pickle
        # set restored_from_dump flag so the data cannot be read again
        self.restored_from_dump=True
        # SED DATA <<<<<<<
        dump_dict = pickle.load( open(filename+'.pickle','r') )
        self.seds = dump_dict['seds']
        self.set_plotter( tdc_SEDs_Plotter(self.seds) )
        # Mesh
        self._Mesh = self.seds[0].xp._Mesh
        # i_ts
        self.i_ts = self.seds[0].i_ts
        # additional parameters
        self.OmegaPl       = dump_dict['OmegaPl']
        self.LambdaDebye   = dump_dict['LambdaDebye']
        self.plasma_params = dump_dict['plasma_params']
        self.n_p   = dump_dict['n_p'] 


    def dump_data(self,filename):
        """
        get pure data from plotter and dump it into the pickle file filename.pickle 
        """
        import pickle
        data = [ d.get_pure_data_copy() for d in self.plotter.data ]
        dump_dict={}
        dump_dict['seds'] = data
        dump_dict['OmegaPl']       = self.OmegaPl
        dump_dict['LambdaDebye']   = self.LambdaDebye
        dump_dict['plasma_params'] = self.plasma_params
        dump_dict['n_p']   = self.n_p 
        pickle.dump( dump_dict, open(filename+'.pickle','w') )

    def __repr__(self):
        s = self._manip_name('tdc_SED_Manip')
        s += 'calc_id = \"%s\"\n'       % self.seds[0].calc_id
        s += '   i_ts = %d\n'           % self.i_ts
        s += '   time = %s\n'           % self.seds[0].timetable
        s += ' p_bins = [%g, %g, %g]\n' % tuple(self.seds[0].p_bins)
        s += '     xx = [%g, %g]\n'     % tuple(self.seds[0].xx)
        s += '\nPlasma properties:\n'
        for key  in sorted(self.plasma_params.keys()):
            s += '%10s = %g\n' % (key,self.plasma_params[key])
        return s

    def read(self, i_ts, **kwargs):
        """
        Read sparticles at timeshot# i_ts
        and calculates sed for already set p_bins and xx
        """
        if not self.restored_from_dump:
            self.i_ts = i_ts
            self.read_particles(i_ts)
            self.calculate_sed()
        else:
            print '\nData are restored from dump file and cannot be read for another i_ts!\n'

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
        # FIGURE ------------------------------------
        self.fig = self.fg.create_figure(facecolor='w')
        xx_str = '[%g, %g]' % tuple(self.seds[0].xx)
        # id label
        id_label = self.plotter.plot_idlabel         +\
                   '   i_ts=' + str(self.i_ts)       +\
                   '   xx='   + xx_str
        self.fig.canvas.set_window_title(id_label) 
        # if asked put widnow title label  into figure too
        if print_id:
            self.fig.suptitle(id_label,size='x-small' )
        # AXES --------------------------------------
        self.ax  = self.fig.axes[0]
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

    def calculate_sed(self, xx=None):
        """
        Calculates sed for already set p_bins and given xx
        """
        for sed in self.seds:
            sed.calculate_sed(xx)
        # calculate plasma parameters
        self.calculate_plasma_params()

    def calculate_plasma_params(self):
        """
        Calculates Debye lengths
        """
        # get \omega^2 of all plasma components
        omega2=0
        for sed in self.seds:
            omega2 += sed.get_omega2()
        self.omega = np.sqrt(omega2)
        # plasma frequency
        self.plasma_params['omega'] = self.OmegaPl*self.omega
        # Debye length
        self.plasma_params['l_D'] = self.LambdaDebye/self.omega
        # Debye length in cell coordinates
        self.plasma_params['l_D_cell'] = self._Mesh.x2cell(self.plasma_params['l_D'])

    def calculate_number_of_particles(self, pp=None):
        """
        Calculate number of particles in momentum interval pp
        if pp==None -- use the whole momentum interval
        """
        for sed in self.seds:
            self.n_p[sed.name] = sed.get_number_of_particles(pp)
        
    def set_momentum_bins(self,p_bins):
        """
        Sets 4-momentum bins p_bins for all SEDs
        """
        for sed in self.seds:
            sed.set_momentum_bins(p_bins)

    def set_xx_default(self,xx=None):
        """
        Set xx_default for all SEDs
        Avoid reading Mesh, save to use on restored data
        """
        if not xx:
            xx = [self._Mesh.xmin, self._Mesh.xmax]
        for sed in self.seds:
            sed.set_xx_default(xx)

    def read_particles(self, i_ts):
        """
        Read sparticles at timeshot# i_ts
        """
        for sed in self.seds:
            sed.read_particles(i_ts)
        # clear plasma params dictionary
        self.plasma_params={}        

    def print_number_of_particles(self):
        """
        Print # of particles calculated before by calling
        calculate_number_of_particles()
        """
        for name,np in self.n_p.items():
            print '%s :' % name
            print '%8s = [ %g, %g ]' %  ('pp', np['pp'][0], np['pp'][1])
            for key  in ('UP','DOWN','TOTAL'):
                print '%8s = %g' %  (key, np[key])

    def print_plasma_params(self):
        """
        Prints parameters of the plasma in the current spatial domain
        """
        print 'Plasma properties:\n'
        for key  in sorted(self.plasma_params.keys()):
            print '%10s = %g' % (key,self.plasma_params[key])
            
