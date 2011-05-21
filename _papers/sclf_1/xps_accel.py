from Common  import tdc_Manip_Plot_vs_X

from Particles.tdc_xp_data          import tdc_XP_Data
from Particles.tdc_xps_tp_plotter   import tdc_XPs_TP_Plotter


tick_and_labels_commands="""
manip_pmax.set_xlim([-0.025,1.025])
manip_pmax.set_xticks(np.arange(0,1.1,0.2))
manip_pmax.set_xticklabels(['0','0.2','0.4','0.6','0.8','1'])
manip_pmax.set_xticks(np.arange(0.1,1.1,0.2),minor=True)

manip_pmax.set_ylim([-1.5,36])
manip_pmax.set_yticks([0,10,20,30])
manip_pmax.set_yticklabels(['0','10','20','30'])
manip_pmax.set_yticks(np.arange(0,36,2),minor=True)
"""
filename='xps_accel'



def do_dump(filename):
    global manip_xps_accel

    IDs=['SCLF__jm1.0_L100_X0.5_nGJ2e5_nx5e3_dt4e-3__RhoGJConst__noMC__dP5e-2_inj20',
         'SCLF__jm1.25_L100_X0.5_nGJ2e5_nx5e3_dt4e-3__RhoGJConst__noMC__dP5e-2_inj25',
         'SCLF__jm1.5_L100_X0.5_nGJ2e5_nx5e3_dt4e-3__RhoGJConst__noMC__dP5e-2_inj30']
    i_ts = 751

    manip_xps_accel = tdc_plot_xp_accel(IDs, i_ts)
    manip_xps_accel.dump_data(filename)


def do_plot(filename):
    global manip_xps_accel

    tdc_set_hardcopy_rcparams()
    tdc_set_results_dir('../RESULTS/__TDC_2')

    manip_xps_accel = tdc_plot_xp_accel_restored(filename)
    tdc_set_default_rcparams()
    manip_xps_accel.interactive_off()

    exec tick_and_labels_commands

    manip_pmax.interactive_on()
    plt.show()



def tdc_plot_xp_accel(calc_ids,
                      i_ts,
                      particle_names=None, 
                      sample_dict=None,
                      tp=None,
                      trail_dict=None,
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
    sample_dict
       tdc_XP_Sample... instance
    tp
       <None> TP_Data instance
    trail_dict
       <None> trail_dict
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
    manip = XP_Manip_Accel(**kwargs)
    manip.setup_from_data(calc_ids,
                          particle_names, sample_dict,
                          tp, trail_dict,
                          **kwargs)
    manip.read(i_ts)
    if not no_plot:
        manip.plot(ylim, xlim, print_id)
    return manip


def tdc_plot_xp_accel_restored(filename,
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
    manip = XP_Manip_Accel(**kwargs)
    manip.restore(filename)
    if not no_plot:
        manip.plot(ylim, xlim, print_id)
    return manip



class XP_Manip_Accel(tdc_Manip_Plot_vs_X):
    """
    Manipulator class for XP
    """
    __default_particle_names = ['Electrons']

    def __init__(self,**kwargs):
        tdc_Manip_Plot_vs_X.__init__(self,**kwargs)
        # XP DATA <<<<<<<
        self.xps=None
        # TP 
        self.tp=None
        
    def setup_from_data(self,
                        calc_ids,
                        particle_names=None,
                        sample_dict=None,
                        tp=None,
                        trail_dict=None,
                        **kwargs):
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
        for id in calc_ids:
            for pname in particle_names:
                self.xps.append( tdc_XP_Data( id,
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
                tp=None,
                trail_dict=None):
        """
        setup Manip by reading the pickle'd data dumped
        by Manip called before
        """
        import pickle
        # set restored_from_dump flag so the data cannot be read again
        self.restored_from_dump=True
        # XP DATA <<<<<<<
        self.xps = pickle.load( open(filename+'.pickle','r') )
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
        s = self._manip_name('XP_Manip_Accel')
        for xp in self.xps:
            s += 'calc_id = \"%s\"\n' % xp.calc_id
        s += '   i_ts = %d\n'     % self.i_ts
        if self.tp:
            s += '    TP : %s\n' % self.tp
        return s


if __name__ == "__main__":
    do_plot()
