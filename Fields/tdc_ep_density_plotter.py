from Common_Data_Plot   import tdc_Data_vs_X_Plotter
from tdc_fields_plotter import tdc_Fields_Plotter


class tdc_EP_Density_Plotter(tdc_Fields_Plotter):
    """
    This class is plotter for (e)lectron, (p)ositron number densities
    ===========
    - it implements plot() function fron tdc_Fields_Plotter 
    - sets plot label
    """

    def __init__(self, f_e, f_p, e_density_negative=True, xlabel=None,ylabel=None,idlabel=None):
        """
        f_e -- field with electron number density
        f_p -- field with positron number density
        e_density_negative -- <True> if true Electron density is negative
        """
        # initialize base class
        tdc_Fields_Plotter.__init__(self, (f_e,f_p), xlabel,ylabel,idlabel )
        # labels -----------------------
        if not ylabel:
            self.plot_ylabel = r'$\eta_{\pm}$'
        if not idlabel:
            self.plot_idlabel='N_{e,p}:'+self.data[0].calc_id
        # ------------------------------
        # how to plot e and p number densities
        if e_density_negative:
            self.e_sign = -1
        else:
            self.e_sign =  1

    def plot(self,ax,**kwargs):
        "Plot Field into axes ax"
        self.lines[0], = ax.plot(self.data[0].x, self.e_sign*self.data[0].f,'b',**kwargs)
        self.lines[1], = ax.plot(self.data[1].x,             self.data[1].f,'r',**kwargs)
        tdc_Data_vs_X_Plotter.plot(self,ax)

    def animation_update(self,ax,i_ts):
        "Read and plot field for animation at timestep# i_ts"
        self.read(i_ts)
        self.lines[0].set_ydata( self.e_sign*self.data[0].f)
        self.lines[1].set_ydata(             self.data[1].f)
        for line in self.lines:    
            ax.draw_artist(line)



class tdc_EPG_Density_Plotter(tdc_Fields_Plotter):
    """
    This class is plotter for (e)lectron, (p)ositron, (g)amma-rays number densities
    ===========
    - it implements plot() function fron tdc_Fields_Plotter 
    - sets plot label
    """

    def __init__(self, f_e, f_p, f_g, e_density_negative=True):
        """
        f_e -- field with electron number density
        f_p -- field with positron number density
        f_g -- field with gamma-ray number density
        e_density_negative -- <True> if true Electron density is negative
        """
        tdc_Fields_Plotter.__init__(self, (f_e,f_p,f_g) )
        # label
        self.plot_ylabel = r'$n_{e,\gamma}$'
        self.plot_idlabel='N_{e,p,g} : '+self.data[0].calc_id
        # how to plot e and p number densities
        if e_density_negative:
            self.e_sign = -1
        else:
            self.e_sign =  1

    def plot(self,ax,**kwargs):
        "Plot Field into axes ax"
        self.lines[0], = ax.plot(self.data[0].x, self.e_sign*self.data[0].f,'b',**kwargs)
        self.lines[1], = ax.plot(self.data[1].x,             self.data[1].f,'r',**kwargs)
        self.lines[2], = ax.plot(self.data[2].x,             self.data[2].f,'k',**kwargs)
        tdc_Data_vs_X_Plotter.plot(self,ax)

    def animation_update(self,ax,i_ts):
        "Read and plot field for animation at timestep# i_ts"
        self.read(i_ts)
        self.lines[0].set_ydata( self.e_sign*self.data[0].f)
        self.lines[1].set_ydata(             self.data[1].f)
        self.lines[2].set_ydata(             self.data[2].f)
        for line in self.lines:    
            ax.draw_artist(line)



class tdc_EPGP_Density_Plotter(tdc_Fields_Plotter):
    """
    This class is plotter for (e)lectron, (p)ositron, (g)amma-rays, (p)rotons number densities
    ===========
    - it implements plot() function fron tdc_Fields_Plotter 
    - sets plot label
    """

    def __init__(self, f_e, f_p, f_g, f_pr, e_density_negative=True):
        """
        f_e -- field with electron number density
        f_p -- field with positron number density
        f_g -- field with gamma-ray number density
        f_pr -- field with protons number density
        e_density_negative -- <True> if true Electron density is negative
        """
        tdc_Fields_Plotter.__init__(self, (f_e,f_p,f_g,f_pr) )
        # label
        self.plot_ylabel = r'$n_{e,\gamma,p}$'
        self.plot_idlabel='N_{e,p,g,p} : '+self.data[0].calc_id
        # how to plot e and p number densities
        if e_density_negative:
            self.e_sign = -1
        else:
            self.e_sign =  1

    def plot(self,ax,**kwargs):
        "Plot Field into axes ax"
        self.lines[0], = ax.plot(self.data[0].x, self.e_sign*self.data[0].f,'b',**kwargs)
        self.lines[1], = ax.plot(self.data[1].x,             self.data[1].f,'r',**kwargs)
        self.lines[2], = ax.plot(self.data[2].x,             self.data[2].f,'k',**kwargs)
        self.lines[3], = ax.plot(self.data[3].x,             self.data[3].f,'m',**kwargs)
        tdc_Data_vs_X_Plotter.plot(self,ax)

    def animation_update(self,ax,i_ts):
        "Read and plot field for animation at timestep# i_ts"
        self.read(i_ts)
        self.lines[0].set_ydata( self.e_sign*self.data[0].f)
        self.lines[1].set_ydata(             self.data[1].f)
        self.lines[2].set_ydata(             self.data[2].f)
        self.lines[3].set_ydata(             self.data[3].f)
        for line in self.lines:    
            ax.draw_artist(line)
