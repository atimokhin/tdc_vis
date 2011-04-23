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
        # labels
        self.plot_ylabel  = _Field_Labels().get_TeXLabel(self.data[0].name)
        self.plot_idlabel = self.data[0].name+' : '+self.data[0].calc_id
        # initialize lines
        self.lines = len(self.data)*[None]

    def plot(self,ax,**kwargs):
        """
        Plot fields into axes ax
        **kwargs goes to ax.plot(..)
        """
        for i,field in enumerate(self.data):
            self.lines[i], = ax.plot(field.x, field.f,'k',**kwargs)
        tdc_Data_vs_X_Plotter.plot(self,ax,**kwargs)

    def replot(self,ax):
        """
        Change data for existing lines and replot them
        """
        for i,line in enumerate(self.lines):
            line.set_ydata(self.data[i].f)
            line.set_xdata(self.data[i].x)
        for line in self.lines:    
            ax.draw_artist(line)

    def update_plot(self,ax):
        """
        Change f data for existing lines and replot them
        """
        for i,line in enumerate(self.lines):
            line.set_ydata(self.data[i].f)
        for line in self.lines:    
            ax.draw_artist(line)

    def set_animated(self,val):
        """
        Set animated property in all lines
        """
        for line in self.lines:
            line.set_animated(val)


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
