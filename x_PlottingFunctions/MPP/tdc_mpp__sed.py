import Particles
from Particles  import tdc_SED_Data
from Particles  import tdc_SEDs_Plotter

from ATvis.MPP import AT_MPP_SED_Timeseries_H


def tdc_mpp__sed(ID, timeshots, xxs, p_bins=None, fig_param=None):
    """
    plots SED for timeshots, returns tdc_MPP_H instance with the plot
    uses default energy bins hardcoded inside the function:
      __default_p_bins
      if not instructed otherwise
    """
    # energy bins ------------------
    __default_p_bins = (1,1e8,100)
    if not p_bins:
        p_bins=__default_p_bins
    # ------------------------------
    # DATA
    s_p  = tdc_SED_Data(ID, particle_name='Positrons', p_bins=p_bins )
    s_e  = tdc_SED_Data(ID, particle_name='Electrons', p_bins=p_bins )
    s_g  = tdc_SED_Data(ID, particle_name='Pairs',     p_bins=p_bins )
    # plotters
    sp = tdc_SEDs_Plotter( [s_p,s_e,s_g] )
        
    mpp = AT_MPP_SED_Timeseries_H( sp, timeshots, xxs, fig_param=fig_param)
    return mpp
