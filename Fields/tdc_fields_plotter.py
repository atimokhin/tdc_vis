import inspect
import matplotlib.lines

from Common_Data_Plot import tdc_Data_vs_X_Plotter

class tdc_Fields_Plotter(tdc_Data_vs_X_Plotter):
    """
    This class is a base class for fields plotters

    plots all fields as black lines
    """

    __line_args = inspect.getargspec(matplotlib.lines.Line2D.__init__).args
    __line_args.append('animated')


    def __init__(self, fields, xlabel=None,ylabel=None,idlabel=None):
        """
        fields -- list with fields to be plotted
        """
        # base class initialization is enough
        tdc_Data_vs_X_Plotter.__init__(self,fields, xlabel,ylabel,idlabel)
        # labels ---------------------------
        if not ylabel:
            self.plot_ylabel  = _Field_Labels().get_TeXLabel(self.data[0].name)
        if not idlabel:
            self.plot_idlabel = self.data[0].name+':'+self.data[0].calc_id
        # ----------------------------------
        # initialize lines
        self.lines = len(self.data)*[None]

    def plot(self,ax,**kwargs):
        """
        Plot fields into axes ax
        **kwargs goes to ax.plot(..)
        """
        # filter arguments for field lines
        plot_kwargs = { k: kwargs[k] for k in self.__line_args if kwargs.has_key(k)}        
        # apply custom plot style set manually with set_plotstyle()
        plot_kwargs.update(self._plot_style)
        # plot lines
        for i,field in enumerate(self.data):
            self.lines[i], = ax.plot(field.x, field.f,'k',**plot_kwargs)
        tdc_Data_vs_X_Plotter.plot(self,ax)

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
