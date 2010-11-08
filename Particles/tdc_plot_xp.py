import Common
from Common  import tdc_Manip_Plot_vs_X

from tdc_xp_data          import tdc_XP_Data
from tdc_xps_tp_plotter   import tdc_XPs_TP_Plotter


def tdc_plot_xp(calc_id, i_ts,
                particle_names=None, 
                sample_dict=None,
                tp=None, trail_dict=None,
                ylim=None, xlim=None,
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

    manip = tdc_XP_Manip(calc_id,
                         particle_names, sample_dict,
                         tp, trail_dict,
                         **kwargs)
    manip.read(i_ts)
    if not no_plot:
        manip.plot(ylim, xlim, print_id)
    return manip




class tdc_XP_Manip(tdc_Manip_Plot_vs_X):
    """
    Manipulator class for XP
    """
    __default_particle_names = ['Electrons', 'Positrons', 'Pairs']

    def __init__(self, calc_id,
                 particle_names=None,
                 sample_dict=None,
                 tp=None, trail_dict=None,
                 **kwargs):

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
        # set PLOTTER by calling base class constructor
        # with tdc_XPs_Plotter instanse
        tdc_Manip_Plot_vs_X.__init__(self,
                                     tdc_XPs_TP_Plotter( self.xps,
                                                         tp=self.tp,
                                                         trail_dict=trail_dict ),
                                     **kwargs)


    def __repr__(self):
        s =  'tdc_XP_Manip:\n\n'
        s += 'calc_id = \"%s\"\n' % self.xps[0].calc_id
        s += ' sample = %s\n'     % str(self.xps[0].sample)
        s += '   i_ts = %d\n'     % self.i_ts
        s += '   time = %s\n'     % self.xps[0].timetable
        if self.tp:
            s += '    TP : %s\n' % self.tp
        return s
