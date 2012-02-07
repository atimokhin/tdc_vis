from Common_Data_Plot import tdc_Manip_Plot_vs_X

from Particles.tdc_xp_data        import tdc_XP_Data
from Particles.tdc_xps_tp_plotter import tdc_XPs_TP_Plotter


def tdc_plot_xp(calc_id, i_ts,
                particle_names=None, 
                sample_dict=None,
                tp=None,
                trail_dict=None,
                ylim=None,
                xlim=None,
                symlog=False,
                linthreshy=5,
                print_id=False,
                no_plot=False,
                fig_param=None):
    """
    calc_id
       calculation id name
    i_ts
       timeshot#
    Options:
    --------
    particle_names
       name(s) of particles whose phase prtraits are to be plotted
    sample_dict
       tdc_XP_Sample... instance
    tp
       <None> TP_Data instance
    trail_dict
       <None> trail_dict
    xlim 
    ylim
       <None>  axis limits
    symlog
       <False>
       whether to plot momentum in symlog scale:
       p is linear in the interval [-linthreshy,linthreshy]
       and logarithmic outside
    linthreshy
       <5>
       p is linear in the interval [-linthreshy,linthreshy]
       and logarithmic outside
    print_id
       <False> whether to put id label on the figure
    no_plot
       <False> if True do not call plot in Manipulator
       useful if additional plot modifications are required
    Returns:
    --------
    ()=> tdc_XP_Manip
    """
    manip = tdc_XP_Manip(fig_param)
    manip.setup_from_data(calc_id,
                          particle_names,
                          sample_dict,
                          tp,
                          trail_dict)
    manip.read(i_ts)
    if not no_plot:
        manip.plot(ylim=ylim,
                   xlim=xlim,
                   print_id=print_id,
                   symlog=symlog,
                   linthreshy=linthreshy)
    return manip


def tdc_plot_xp_restored(filename,
                         dump_id,
                         ylim=None,
                         xlim=None,
                         symlog=False,
                         linthreshy=5,
                         print_id=False,
                         no_plot=False,
                         fig_param=None):
    """
    filename
       pickle file name is 'filename.pickle'
    Options:
    --------
    xlim 
    ylim
       <None>  axis limits
    symlog
       <False>
       whether to plot momentum in symlog scale:
       p is linear in the interval [-linthreshy,linthreshy]
       and logarithmic outside
    linthreshy
       <5>
       p is linear in the interval [-linthreshy,linthreshy]
       and logarithmic outside
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
    manip = tdc_XP_Manip(fig_param)
    manip.restore(filename,dump_id)
    if not no_plot:
        manip.plot(ylim=ylim,
                   xlim=xlim,
                   print_id=print_id,
                   symlog=symlog,
                   linthreshy=linthreshy)
    return manip



class tdc_XP_Manip(tdc_Manip_Plot_vs_X):
    """
    Manipulator class for XP
    """
    __default_particle_names = ['Electrons', 'Positrons', 'Pairs']

    def __init__(self,fig_param=None):
        tdc_Manip_Plot_vs_X.__init__(self,fig_param)
        # XP DATA <<<<<<<
        self.xps=None
        # TP 
        self.tp=None

    def setup_from_data(self, calc_id,
                        particle_names=None,
                        sample_dict=None,
                        tp=None,
                        trail_dict=None):
        """
        setup Manip by reading the original data file
        """
        # set default sample if none is given
        if not sample_dict:
            sample_dict=dict(name='regular', n_reduce=1, n_min=1)
        # use default particle_names if not set in arguments
        if not particle_names:
            particle_names = self.__default_particle_names
        # make sure particle_names is a sequence
        if not isinstance( particle_names, (list,tuple) ):
            particle_names = (particle_names,)
        # XP DATA <<<<<<<
        self.xps=[]
        for pname in particle_names:
            self.xps.append( tdc_XP_Data( calc_id,
                                          particle_name=pname,
                                          sample_dict=sample_dict) )
        # TP
        self.tp=tp
        # set PLOTTER by calling base class method
        self.set_plotter( tdc_XPs_TP_Plotter( self.xps,
                                              tp=self.tp,
                                              trail_dict=trail_dict )
                          )

    def restore(self,
                filename,
                dump_id,
                tp=None,
                trail_dict=None):
        """
        setup Manip by reading the pickle'd data dumped
        by Manip called before
        """
        import pickle
        from   Auxiliary import tdc_Filenames
        # set restored_from_dump flag so the data cannot be read again
        self.restored_from_dump=True
        # XP DATA <<<<<<<
        # full file name of the file with manipulator dump
        filename=tdc_Filenames().get_full_vis_filename(dump_id, filename+'.pickle')
        self.xps = pickle.load( open(filename,'r') )
        # i_ts
        self.i_ts = self.xps[0].i_ts
        # TP
        self.tp=tp
        # set PLOTTER by calling base class method
        self.set_plotter( tdc_XPs_TP_Plotter( self.xps,
                                              tp=self.tp,
                                              trail_dict=trail_dict )
                          )

    def __repr__(self):
        s = self._manip_name('tdc_XP_Manip')
        s += 'calc_id = \"%s\"\n' % self.xps[0].calc_id
        s += ' sample = %s\n'     % str(self.xps[0].sample)
        s += '   i_ts = %d\n'     % self.i_ts
        s += '   time = %s\n'     % self.xps[0].timetable
        if self.tp:
            s += '    TP : %s\n' % self.tp
        return s
