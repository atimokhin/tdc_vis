import matplotlib.pyplot as plt
import numpy             as np

from ATvis.Common_Data_Plot import *

from Auxiliary        import *
from Common_Data_Plot import *
from Common_Data_Plot import tdc_Manip


# --------------------------------------
# dictionary with data takent from plots
# filled manually <=====================
# --------------------------------------
pmax_dict= {
    0.1  : [0.26, 0.47],
#    0.25 : [0.87, 1.2],
    0.25 : [0.96, 1.23],
    0.5  : [2, 3],
    0.75 : [4.5, 8],
    0.9  : [11, 17.66],
    0.95 : [20.72, 33.34]
    }

ksi_max=0.984
# --------------------------------------


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





def do_plot():
    global manip_pmax

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<
    AT_rcParams.set_hardcopy()
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<

    manip_pmax = tdc_plot_pmax(100, ksi_max=ksi_max, fig_param=paramSingleFig_MNRAS)
    manip_pmax.interactive_off()

    exec tick_and_labels_commands

    manip_pmax.interactive_on()
    plt.show()



def tdc_plot_pmax(nn, ksi_max,
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
    ()=> Pmax_Manip
    """

    manip = Pmax_Manip(fig_param)
    manip.setup_from_data(nn, ksi_max)
    if not no_plot:
        manip.plot(ylim, xlim, print_id=print_id)
    return manip


class Pmax_Manip(tdc_Manip):
    """
    Manipulator class for pmax plot
    """

    def setup_from_data(self,
                        nn,
                        ksi_max):
        self.set_plotter( Pmax_Plotter(nn,ksi_max) )
        
    def __repr__(self):
        s =  'Pmax Plotter:\n'
        return s


class Pmax_Plotter(AT_Data_Plotter):
    
    def __init__(self,nn,ksi_max, xlabel=None,ylabel=None,idlabel=None):
        # base class initialization is enough
        AT_Data_Plotter.__init__(self,
                                  None,
                                  xlabel=r'$\xi$',
                                  ylabel=r'$p_{\mathrm{beam}}$',
                                  idlabel='Pmax')
        #
        self.pa=Pmax_Analytical(nn,ksi_max)
        self.pn=Pmax_Numerical()
        #
        self.xmin=0
        self.xmax=1
    
    def read(self, i_ts,**kwargs):
        pass

    def plot(self,ax):
        self.pa.plot(ax)
        self.pn.plot(ax)

    def animation_update(self,ax,i_ts):
        "Read and plot particles for animation at timestep# i_ts"
        pass


class Pmax_Analytical:
    
    def __init__(self, nn, ksi_max=1):
        self.xx=np.linspace(0,ksi_max-1./nn,nn-1)
        self.pp=self.pmax(self.xx)
        self.lines=[]

    def plot(self,ax):
        self.lines, = ax.plot(self.xx, self.pp,'-r',linewidth=1)

    def pmax(self,ksi):
        return 2*ksi/(1-ksi**2)


class Pmax_Numerical:

    def __init__(self):
        # dictionary with data takent from plots
        self.pmax_dict=pmax_dict 
        # make arrays for plotting
        self.xx=[]
        self.pp=[]
        for x,p in self.pmax_dict.items():
            self.xx.append([x,x])
            self.pp.append(p)
        # initialize line list
        self.lines=len(self.pmax_dict)*[None]
        
    def plot(self,ax):
        for line,x,p in zip(self.lines,self.xx,self.pp):
            line, = ax.plot(x, p,'-b',linewidth=4)
        

if __name__ == "__main__":
    do_plot()
