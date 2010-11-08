from Common import tdc_Data_vs_X_Plotter

class tdc_Fields_Plotter(tdc_Data_vs_X_Plotter):
    """
    This class is a base class for fields plotters

    plots all fields as black lines
    """

    def __init__(self, fields):
        """
        fields -- list with fields to be plotted
        """
        # base class initialization is enough
        tdc_Data_vs_X_Plotter.__init__(self,fields)
        self.plot_ylabel  = _Field_Labels().get_TeXLabel(self.data[0].name)
        self.plot_idlabel = self.data[0].name+' : '+self.data[0].calc_id

    def plot(self,ax,**kwargs):
        """
        Plot fields into axes ax
        **kwargs goes to ax.plot(..)
        """
        tdc_Data_vs_X_Plotter.plot(self,ax,**kwargs)
        for i,field in enumerate(self.data):
            self.lines[i], = ax.plot(field.x, field.f,'k',**kwargs)


    def animation_update(self,ax,i_ts):
        "Read and plot field for animation at timestep# i_ts"
        self.read(i_ts)
        for i,line in enumerate(self.lines):
            line.set_ydata(self.data[i].f)
        for line in self.lines:    
            ax.draw_artist(line)



class _Field_Labels:
    """
    This class contains string representation
    for labeling plots for different fields
    """

    TeX_Label={\
        'Rho'    : r'$\eta$',\
        'RhoGJ'  : r'$\eta_{\mathrm{GJ}}$',\
        'E_acc'  : r'$E$',\
        'Phi'    : r'$\phi$',\
        'J'      : r'$j$'\
        }

    def get_TeXLabel(self, name):
        return self.TeX_Label.get(name, str(name))
