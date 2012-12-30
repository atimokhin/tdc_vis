import scipy
import scipy.optimize
import math

from ATvis.Common_Data_Plot import AT_Plotter

from Auxiliary        import tdc_Exception

from tdc_fft_data     import tdc_FFT_Data


# ----------------------------------------
# functions for spectrum fittings
# ----------------------------------------

def _power_law(k, A, alpha):
    "fitting function"
    return A * k**alpha
def _power_law_fit(k_log, A, alpha):
    "function used in fitting - logarithmic"
    return math.log(A) + alpha*k_log

# ----------------------------------------



class WrongFittingFunctionException(tdc_Exception):
    "Exception class for tdc_FFT_Data_Fit"
    pass

        
class tdc_FFT_Fit:
    """
    Class with analytical fit for Furier spectrum of a field
    ==> fitting is done in logarithmic coordinates
    -------
    Members
    -------
    kmin
    kmax
       fitted interval interval
    nk_plot
       length of plotting arrays
    kk_plot
    Ik_plot
       arrays for plotting spectral fit
    """
    
    def __init__(self, fft_data, fitting_type='pl', nk_plot=20):
        """
        nk_plot
          length of plotting arrays
        """
        # tdc_FFT_Data instance
        if isinstance(fft_data, tdc_FFT_Data):
            self.fft_data = fft_data
        else:
            raise TypeError()
        # type of the fitting function
        self.type=fitting_type
        # setup fitting function
        if self.type=='pl':
            self.__func_fit = _power_law_fit
            self.__func     = _power_law
        else:
            raise WrongFittingFunctionException()
        # plotting arrays
        self.nk_plot=nk_plot
        self.kk_plot=None
        self.Ik_plot=None
        # initialize members
        self.kmin = None
        self.kmax = None
        self.__popt = None
        self.__pcov = None

    def __repr__(self):
        # print FFT_Data info
        s = str(self.fft_data)
        # common part
        s += 'tdc_FFT_Data_Fit:\n'
        s += '   plot points : %i\n'     % self.nk_plot
        s += '          type : %s\n'     % self.type
        if self.kk_plot!=None:
            s += '  fitted for kk=[%g,%g]\n' % (self.kmin,self.kmax)
            # print info for specific fitting functions
            if self.type=='pl':
                s += ' A * k**(alpha): A=%g, alpha=%g\n' % (self.__popt[0],self.__popt[1])
        else:
            s += '--> FFT_Data have not been fitted yet!'
        return s

    def fit(self, kk=None):
        """
        Fit Fourier spectrum with the function set at class instantination
        ==> NB: fitting is done in logarithmic coordinates
        and fills plotting arrays with data
        --------
        Options:
        --------
        kk
           (k1,k2) <None> spectral interval for function fitting
           by default interval [ kk[1], kk[imax__kk] ] will be fitted
           ==> i.e. k=0 is excluded
        """
        # fitting interval
        if kk:
            ik_min=(self.fft_data.kk[1:self.fft_data.imax__kk]<=kk[0]).nonzero()[0][-1]
            ik_max=(self.fft_data.kk[1:self.fft_data.imax__kk]<=kk[1]).nonzero()[0][-1]
        else:
            ik_min=1;
            ik_max=self.fft_data.imax__kk
        # do fitting
        self.__popt,self.__pcov = scipy.optimize.curve_fit(self.__func_fit,
                                                           scipy.log(self.fft_data.kk[ik_min:ik_max]),
                                                           scipy.log(self.fft_data.Ik[ik_min:ik_max]) )
        # boundaries of fitted interval
        self.kmin = self.fft_data.kk[ik_min]
        self.kmax = self.fft_data.kk[ik_max]
        # fill plot arrays <===============
        self.kk_plot=scipy.logspace( scipy.log10(self.kmin),
                                     scipy.log10(self.kmax),
                                     self.nk_plot )
        self.Ik_plot=self.fitting_function(self.kk_plot)
        # =================================
            
    def fitting_function(self,k):
        """
        Returns value of fitting finction for given k
        This function can be used for plotting
        """
        return self.__func(k,*self.__popt)
    

class tdc_FFT_Fit_Plotter(AT_Plotter):
    """
    Plotter for plotting FFT_Fit
    """
    
    def __init__(self,fft_data_fit, xlabel=None,ylabel=None,idlabel=None):
        """
        fft_data_fit
           tdc_FFT_Data_Fit objects
        """
        AT_Plotter.__init__(self,fft_data_fit, xlabel,ylabel,idlabel)
        
    def plot(self,ax,**kwargs):
        """
        Plot spectrum fit onto existing axes ax
        """
        if self.data[0].kk_plot!=None:
            self.line, = ax.loglog(self.data[0].kk_plot,
                                   self.data[0].Ik_plot,
                                   '--r', linewidth=2,
                                   **kwargs)
        else:
            print '\nDo fitting first!\n'

    def delete_plot(self,ax):
        """
        Delete spectrum fit plot from axes ax
        """
        try:
            ax.lines.remove(self.line)
        except ValueError:
            pass
