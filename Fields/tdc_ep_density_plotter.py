from tdc_fields_plotter import tdc_Fields_Plotter

class tdc_EP_Density_Plotter(tdc_Fields_Plotter):
    """
    This class is plotter for electron and positron number densities

    - it implements plot() function fron tdc_Fields_Plotter 
    - sets plot label
    """

    def __init__(self, f_e, f_p, e_density_negative=True):
        """
        f_e -- field with electron number density
        f_p -- field with positron number density
        e_density_negative -- <True> if true Electron density is negative
        """
        tdc_Fields_Plotter.__init__(self, (f_e,f_p) )
        # label
        self.plot_ylabel = r'$\eta_{\pm}$'
        self.plot_idlabel='N_{e,p} : '+self.data[0].calc_id

        if e_density_negative:
            self.e_sign = -1
        else:
            self.e_sign =  1


    def plot(self,ax,**kwargs):
        "Plot Field into axes ax"
        self.lines[0], = ax.plot(self.data[0].x, self.e_sign*self.data[0].f,'b',**kwargs)
        self.lines[1], = ax.plot(self.data[1].x,             self.data[1].f,'r',**kwargs)


    def animation_update(self,ax,i_ts):
        "Read and plot field for animation at timestep# i_ts"
        self.read(i_ts)
        self.lines[0].set_ydata( self.e_sign*self.data[0].f)
        self.lines[1].set_ydata(             self.data[1].f)
        for line in self.lines:    
            ax.draw_artist(line)
