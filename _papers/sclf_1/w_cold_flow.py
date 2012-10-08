import matplotlib.pyplot as plt
import numpy             as np

from Auxiliary        import *
from Common_Data_Plot import *
from Common_Data_Plot import tdc_Manip, tdc_Data_Plotter
# --------------------------------------


# --------------------------------------
# dictionary with data taken from plots
# filled manually <=====================
# --------------------------------------
w_e_dict= {
    0.1  : [2e-4,   3.7e-5],
    0.25 : [2.7e-4, 6.7e-5],
    0.5  : [3e-3,   1.3e-3],
    0.75 : [1.2e-2, 5e-3],
    0.9  : [1.1e-2, 3e-3]
    }

ksi_max=0.984
# --------------------------------------


tick_and_labels_commands="""
manip_w.set_xlim([-0.025,1.025])
manip_w.set_xticks(np.arange(0,1.1,0.2))
manip_w.set_xticklabels(['0','0.2','0.4','0.6','0.8','1'])
manip_w.set_xticks(np.arange(0.1,1.1,0.2),minor=True)

manip_w.set_ylim([3e-13,1.1e-10])
"""




def do_plot():
    global manip_w

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<
    tdc_rcParams.set_hardcopy()
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<

    manip_w = tdc_plot_w_cold_flow(100, ksi_max=ksi_max, fig_param=paramSingleFig_SED_MNRAS)
    manip_w.interactive_off()

    exec tick_and_labels_commands

    manip_w.interactive_on()
    plt.show()



def tdc_plot_w_cold_flow(nn, ksi_max,
                         ylim=None, xlim=None,
                         print_id=False,
                         no_plot=False,
                         fig_param=None):
    """
    nn
       # of points
    ksi_max
       maximum value of ksi
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
    ()=> W_Manip
    """

    manip = W_Manip(fig_param)
    manip.setup_from_data(nn, ksi_max)
    if not no_plot:
        manip.plot(ylim, xlim, print_id=print_id)
    return manip


class W_Manip(tdc_Manip):
    """
    Manipulator class for pmax plot
    """

    def setup_from_data(self,
                        nn,
                        ksi_max):
        self.set_plotter( W_Plotter(nn,ksi_max) )
        
    def __repr__(self):
        s =  'W Plotter:\n'
        return s


class W_Plotter(tdc_Data_Plotter):
    
    def __init__(self,nn,ksi_max, xlabel=None,ylabel=None,idlabel=None):
        # base class initialization is enough
        tdc_Data_Plotter.__init__(self,
                                  None,
                                  xlabel=r'$\xi$',
                                  ylabel=r'$\tilde{W}$',
                                  idlabel='W')
        #
        ## self.wa=Pmax_Analytical(nn,ksi_max)
        self.wn=W_E2_Numerical()
        #
        self.xmin=0
        self.xmax=1
    
    def read(self, i_ts,**kwargs):
        pass

    def plot(self,ax):
        ## self.wa.plot(ax)
        self.wn.plot(ax)

    def animation_update(self,ax,i_ts):
        "Read and plot particles for animation at timestep# i_ts"
        pass


## class Pmax_Analytical:
    
##     def __init__(self, nn, ksi_max=1):
##         self.xx=np.linspace(0,ksi_max-1./nn,nn-1)
##         self.pp=self.pmax(self.xx)
##         self.lines=[]

##     def plot(self,ax):
##         self.lines, = ax.plot(self.xx, self.pp,'-r',linewidth=1)

##     def pmax(self,ksi):
##         return 2*ksi/(1-ksi**2)


class W_E2_Numerical:

    def __init__(self):
        # dictionary with data takent from plots
        self.w_e_dict = w_e_dict 
        # make arrays for plotting
        self.xx       = self.w_e_dict.keys()
        self.xx.sort()
        self.ww       = 4.8e-9 * np.array([self.w_e_dict[x][0] for x in self.xx])
        self.ww_err   = 4.8e-9 * np.array([self.w_e_dict[x][1] for x in self.xx])
        # initialize line list
        self.line     = None
        
    def plot(self,ax):
        ax.set_yscale('log')
        self.line = ax.errorbar(self.xx, self.ww, yerr=self.ww_err, fmt='-o',markersize=2)
        

if __name__ == "__main__":
    do_plot()
