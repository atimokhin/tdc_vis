import matplotlib.pyplot as plt
import numpy             as np

from Common  import *
from Common  import tdc_Manip, tdc_Data_Plotter


# --------------------------------------
# dictionary with data takent from plots
# filled manually <=====================
# --------------------------------------
pmax_dict= {
    0.1  : [0.1, 0.2],
    0.25 : [0.2, 0.3],
    0.5  : [1.1, 2],
    0.75 : [0.1, 0.2],
    0.9  : [0.2, 0.3],
    0.95 : [1.1, 2]
    }

ksi_max=0.95
# --------------------------------------


tick_and_labels_commands="""
"""




def do_plot():
    global manip_pmax

    from single_figure_style import fig_style

    tdc_set_hardcopy_rcparams()

    manip_pmax = tdc_plot_pmax(100, ksi_max=ksi_max, **fig_style)
    manip_pmax.interactive_off()

    exec tick_and_labels_commands

    manip_pmax.interactive_on()
    plt.show()
    tdc_set_default_rcparams()



def tdc_plot_pmax(nn, ksi_max,
                  ylim=None, xlim=None,
                  print_id=False,
                  no_plot=False,
                  **kwargs):
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

    manip = Pmax_Manip(nn, ksi_max, **kwargs)
    if not no_plot:
        manip.plot(ylim, xlim, print_id=print_id)
    return manip


class Pmax_Manip(tdc_Manip):
    """
    Manipulator class for pmax plot
    """

    def __init__(self, nn, ksi_max, **kwargs):
        # set PLOTTER by calling base class constructor
        tdc_Manip.__init__(self,
                           Pmax_Plotter(nn,ksi_max),
                           **kwargs )

    def __repr__(self):
        s =  'Pmax Plotter:\n'
        return s


class Pmax_Plotter(tdc_Data_Plotter):
    
    def __init__(self,nn,ksi_max):
        # base class initialization is enough
        tdc_Data_Plotter.__init__(self,None)
        self.pa=Pmax_Analytical(nn,ksi_max)
        self.pn=Pmax_Numerical()
        #
        self.xmin=0
        self.xmax=1
        # plot labels
        self.plot_ylabel  = r'$p_\max$'
        self.plot_xlabel  = r'$\xi$'
        self.plot_idlabel = 'Pmax'
    
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
