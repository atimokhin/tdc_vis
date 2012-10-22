import numpy as np
import matplotlib

from Auxiliary        import tdc_Mesh, tdc_Setup_Props, tdc_Filenames
from Common_Data_Plot import tdc_Manip, paramSingleFig_SED_Work

from Particles.tdc_xp_data       import tdc_XP_Data
from Particles.tdc_sed_data      import tdc_SED_Data
from Particles.tdc_seds_plotter  import tdc_SEDs_Plotter


class tdc_SED_Manip(tdc_Manip):
    """
    Manipulator class for SED
    """

    __default_particle_names = ['Electrons', 'Positrons', 'Pairs']
    __default_p_bins = (1,1e8,100)

    def __init__(self,fig_param=None):
        # leve more place for y label
        tdc_Manip.__init__(self,fig_param)


    @staticmethod
    def init_from_data(calc_id,
                       i_ts,
                       particle_names=None, 
                       p_bins=None,
                       xx=None,
                       fig_param=None):
        """
        Setup Manip by reading original data
     
        calc_id
           calculation id name
        i_ts
           timeshot#
        --------
        Options:
        --------
        particle_names
           <None> name(s) of particles whose distribution functions will be plotted
                  if None, default value ['Electrons', 'Positrons', 'Pairs'] will be used
                  {default value set in tdc_SED_Manip}
        p_bins
           <None> energy bins for distribution function
                  if None, default value (1,1e8,100) will be used
                  {default value set in tdc_SED_Manip}
        xx    
           <None> spatial domain fordistribution function
                  if None, the whole domain will be used
                  {default value set in tdc_SED_Data}

        --------
        """
        manip=tdc_SED_Manip(fig_param)
        manip.read_from_data(calc_id,
                             i_ts,
                             particle_names=particle_names,
                             p_bins=p_bins,
                             xx=xx)
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
        manip=tdc_SED_Manip(fig_param)
        manip.read_from_dump(filename, dump_id)
        return manip
        

        
    def read_from_data(self, 
                       calc_id,
                       i_ts,
                       particle_names=None, 
                       p_bins=None,
                       xx=None):
        """
        setup Manip by reading the original data file
        --------
        Options:
        --------
        particle_names
           <None> name(s) of particles whose distribution functions will be plotted
                  if None, default value ['Electrons', 'Positrons', 'Pairs'] will be used
        p_bins
           <None> energy bins for distribution function
                  if None, default value (1,1e8,100)
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
        # initialize particle energy dictionary
        self.e_p = {}
        # get Mesh
        self._Mesh = self.seds[0].xp._Mesh
        # read data
        self.read(i_ts)
        

    def read_from_dump(self,
                       filename,
                       dump_id):
        """
        setup Manip by reading the pickle'd data dumped
        by Manip called before
        """
        import pickle
        # set restored_from_dump flag so the data cannot be read again
        self.restored_from_dump=True
        # SED DATA <<<<<<<
        # full file name of the file with manipulator dump
        filename=tdc_Filenames.get_full_vis_filename(dump_id, filename+'.pickle')
        dump_dict = pickle.load( open(filename,'r') )
        self.seds = dump_dict['seds']
        self.set_plotter( tdc_SEDs_Plotter(self.seds) )
        # Mesh
        self._Mesh = self.seds[0].xp._Mesh
        # i_ts
        self.i_ts = self.seds[0].xp.i_ts
        # additional parameters
        self.OmegaPl       = dump_dict['OmegaPl']
        self.LambdaDebye   = dump_dict['LambdaDebye']
        self.plasma_params = dump_dict['plasma_params']
        self.n_p   = dump_dict['n_p'] 
        self.e_p   = dump_dict['e_p'] 


    def dump_data(self,filename,dump_id):
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
        dump_dict['e_p']   = self.e_p 
        # full file name of the file with manipulator dump
        filename=tdc_Filenames.get_full_vis_filename(dump_id, filename+'.pickle')
        pickle.dump( dump_dict, open(filename,'w') )
        print '\nContent dumped in "%s" \n' % filename

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
        Read particles at timeshot# i_ts
        and calculates sed for already set p_bins and xx
        """
        if not self.restored_from_dump:
            self.i_ts = i_ts
            self.read_particles(i_ts)
            self.calculate_sed()
        else:
            print '\nData are restored from dump file and cannot be read for another i_ts!\n'

    def plot(self,
             prefix=None,
             ylim=None,
             xlim=None,
             print_id=False,
             **kwargs):
        """
        Plots SED for already  set i_ts, p_bins, xx
        accepts only
        prefix: < 'ns' | 'lc' | None >
          depending on prefix plot:
           - None    : plot SED for both ns and lc moving particles
                       on  the same plot, use color lines
           - 'ns'    : plot SED for particles moving to the NS
                       use solid/dashe/dotted b/w lines
           - 'lc'    : plot SED for particles moving to the LC
                       use solid/dashe/dotted b/w lines
           - 'total' : plot SED for particles all particles as a function
                       of |p|, summing dN_dlogPdX_u+dN_dlogPdX_u
        ylim --    axes limits
        xlim |
        print_id  -- print label on the plot? <False>
        """
        # Create figure and axes -----------
        self.create_figure_and_axes()
        # id label
        id_label = 'i_ts=%i:xx=[%g, %g]:' % (self.i_ts,self.seds[0].xx[0],self.seds[0].xx[1]) +\
                   self.plotter.plot_idlabel          
        # if asked put widnow title label  into figure too
        if print_id:
            self.fig.suptitle(id_label, size='x-small')
        id_label = 'Fig %i|' % self.fig.number + id_label
        self.fig.canvas.set_window_title(id_label) 
        # PLOT --------------------------------------
        self.plotter.plot(self.ax,prefix=prefix,**kwargs)
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

    def calculate_particle_energy(self, pp=None):
        """
        Calculate particle energy in momentum interval pp
        if pp==None -- use the whole momentum interval
        """
        for sed in self.seds:
            self.e_p[sed.name] = sed.get_particle_energy(pp)

    def calculate_info(self, pp=None):
        """
        Calculate additional information:
        - plasma parameters
        - number of particles
        - particle energy
        """
        self.calculate_plasma_params()
        self.calculate_number_of_particles(pp)
        self.calculate_particle_energy(pp)

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


    def info_str__number_of_particles(self):
        """
        Print # of particles into a string
        Number of particles is calculated before by calling calculate_number_of_particles()
        """
        s = '\n%s\nNumber of Particles:\n%s\n' % (30*'-',30*'-')
        for name,np in self.n_p.items():
            s += '%s :\n' % name
            s += '%8s = [ %g, %g ]\n' %  ('pp', np['pp'][0], np['pp'][1])
            for key  in ('UP','DOWN','TOTAL'):
                s += '%8s = %g\n' %  (key, np[key])
        return s

    def info_str__particle_energy(self):
        """
        Print particle energy into a string
        Energies are calculated before by calling calculate_particle_energy()
        """
        e_up_total=0
        e_down_total=0
        s = '\n%s\nEnergy:\n%s\n' % (30*'-',30*'-')
        for name,ep in self.e_p.items():
            s += '%s :\n' % name
            s += '%8s = [ %g, %g ]\n' %  ('pp', ep['pp'][0], ep['pp'][1])
            for key  in ('UP','DOWN','TOTAL'):
                s += '%8s = %g\n' %  (key, ep[key])
            e_up_total   += ep['UP']
            e_down_total += ep['DOWN']
        s += '\nTotal Energy:\n'
        s += '      UP:  %g\n' % e_up_total
        s += '    DOWN:  %g\n' % e_down_total
        s += ' UP/DOWN:  %g\n' % (e_up_total/e_down_total,)
        return s

    def info_str__plasma_params(self):
        """
        Prints parameters of the plasma in the current spatial domain into a string
        """
        s = '\n%s\nPlasma properties:\n%s\n' % (30*'-',30*'-')
        for key  in sorted(self.plasma_params.keys()):
            s += '%10s = %g' % (key,self.plasma_params[key])
        return s

    def print_particle_energy(self):
        print self.info_str__particle_energy()

    def print_number_of_particles(self):
        print self.info_str__number_of_particles()

    def print_plasma_params(self):
        print self.info_str__plasma_params()

    def dump_info(self,filename):
        """
        Write info into a text file
        """
        f = open(filename,'w')
        f.write( str(self) )
        f.write( self.info_str__number_of_particles() )
        f.write( self.info_str__particle_energy() )
        f.close()

    
