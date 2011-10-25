from Common_Data_Plot import tdc_Data_Plotter

class tdc_FFT_Plotter(tdc_Data_Plotter):
    """
    This class is a base class for Furier spectrum plotters

    plots spectrum as black line
    """

    def __init__(self, spectrum):
        """
        spectrum -- field spectrum to be plotted
        """
        tdc_Data_Plotter.__init__(self,spectrum)
        # plot label
        self.plot_ylabel = r'$I_k$'
        self.plot_xlabel = r'$k$'
        self.plot_idlabel='FFT:%s:%s' % (self.data[0].name, self.data[0].calc_id)
        # line
        self.line=None
        # xmin/xmax
        self.xmin = None
        self.xmax = None

    def read(self,i_ts,**kwargs):
        """
        Read data at i_ts
        AND
        update default plot limits [xmin,xmax],
        because spectral range can change if we change sampling range
        """
        tdc_Data_Plotter.read(self,i_ts,**kwargs)
        # update xmin/xmax
        self.xmin = 0
        self.xmax = self.data[0].kk[self.data[0].imax__kk]

    def plot(self,ax,**kwargs):
        """
        Plot spectrum into axes ax
        **kwargs goes to ax.plot(..)
        """
        self.line, = ax.loglog(self.data[0].kk[:self.data[0].imax__kk],
                               self.data[0].Ik[:self.data[0].imax__kk],
                               'k',**kwargs)

    def replot(self,ax):
        """
        Change data for existing lines and replot them
        """
        self.line.set_ydata(self.data[0].Ik[:data[0].imax__kk])
        self.line.set_xdata(self.data[0].kk[:data[0].imax__kk])
        ax.draw_artist(self.line)

    def update_plot(self,ax):
        """
        Change f data for existing lines and replot them
        """
        self.line.set_ydata(self.data[0].Ik[:data[0].imax__kk])
        ax.draw_artist(self.line)

    def set_animated(self,val):
        """
        Set animated property in all lines
        """
        line.set_animated(val)
