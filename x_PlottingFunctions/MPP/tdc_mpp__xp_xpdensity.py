from Particles import *
from FMCI      import *
from MPP       import *


def tdc_mpp__xp_xpdensity(ID,
                          i_ts,
                          wlims,
                          xp_partition,
                          sample_dict=None,
                          fig_param=None):
    """
    wlims:
       [wmin,wmax] limits of colormaps on particle weights
    xp_partition:
       partition for making FMCI_XP density plot (goes to tdc_FMCI_XP_Data)
    sample_dict:
       sample dictionary for XP phase portrait (goes to tdc_XP_Data)
    fig_param:
       MPP figure params
    --------
    Returns:
    --------
    ()=>  tdc_MPP__XP_XPDensity instance with the plot
    """
    # XP portrait data
    if sample_dict is None:
        sample_dict = dict(name='regular',n_reduce=1,n_min=200)
    d_xp_e=tdc_XP_Data(ID, 'Electrons', sample_dict=sample_dict )
    d_xp_p=tdc_XP_Data(ID, 'Positrons', sample_dict=sample_dict )
    d_xp_g=tdc_XP_Data(ID, 'Pairs',     sample_dict=sample_dict )
    # XP density data
    d_e=tdc_FMCI_XP_Data(ID, 'Electrons', xp_partition)
    d_p=tdc_FMCI_XP_Data(ID, 'Positrons', xp_partition)
    d_g=tdc_FMCI_XP_Data(ID, 'Pairs', xp_partition)
    # plotters
    p_xp=tdc_XPs_Plotter( (d_xp_e, d_xp_p, d_xp_g) )
    p_e=tdc_FMCI_XP_Plotter(d_e, wlims)
    p_p=tdc_FMCI_XP_Plotter(d_p, wlims)
    p_g=tdc_FMCI_XP_Plotter(d_g, wlims)

    plotters=(p_xp, p_e,p_p,p_g)
    timeshots=(i_ts,)

    mpp=tdc_MPP__XP_XPDensity(plotters, timeshots, fig_param=fig_param)
    mpp.colorbar.ax.tick_params(labelsize=8)
    return mpp
