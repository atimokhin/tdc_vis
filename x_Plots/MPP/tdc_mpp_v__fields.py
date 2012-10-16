from Fields import tdc_Field_Data
from Fields import tdc_Fields_Plotter
from Fields import tdc_EP_Density_Plotter

from Fields import tdc_FFT_Data
from Fields import tdc_FFT_Plotter

from Auxiliary_Plotters import tdc_Moving_Grid_Plotter

from MPP       import *


def tdc_mpp_v__e_rho_n(ID,timeshots,
                       moving_grid_dict=None,
                       fig_param=None):
    """
    for *timeshots* plots:
    [1] e/p number density
    [2] charge density
    [3] electric field
    --------
    Returns:
    --------
    ()=>  tdc_MPP_Comparative_Timeseries_V instance with the plot
    """
    # electric field
    f1 = tdc_Field_Data(calc_id=ID, field_name='E_acc')
    # charge density
    f2 = tdc_Field_Data(calc_id=ID, field_name='Rho')
    # electron and positron number densities
    f3_e = tdc_Field_Data(calc_id=ID, field_name='N', filename='prop_Electrons.h5' )
    f3_p = tdc_Field_Data(calc_id=ID, field_name='N', filename='prop_Positrons.h5' )
    # PLOTTERS
    fp1=tdc_Fields_Plotter(f1)
    fp2=tdc_Fields_Plotter(f2)
    fp3=tdc_EP_Density_Plotter(f3_e,f3_p)
    if moving_grid_dict:
        fp1 = tdc_Moving_Grid_Plotter(fp1,moving_grid_dict)
        fp2 = tdc_Moving_Grid_Plotter(fp2,moving_grid_dict)
        fp3 = tdc_Moving_Grid_Plotter(fp3,moving_grid_dict)
    # MFP instance
    mpp = tdc_MPP_Comparative_Timeseries_V( (fp1,fp2,fp3), timeshots, fig_param=fig_param)
    return mpp


def tdc_mpp_v__e_fft_discharge(ID,timeshots,
                               xx_discharge,
                               xx_out,
                               moving_grid_dict=None,
                               fig_param=None):
    """
    for *timeshots* plots:
    [1] electric field
    [2] Spectrum inside discharge zone [xx_discharge]
    [3] Spectrum outside of discharge zone [xx_out]
    --------
    Returns:
    --------
    ()=>  tdc_MPP_Comparative_Timeseries_V instance with the plot
    """
    # electric field
    f1 = tdc_Field_Data(calc_id=ID, field_name='E_acc')
    # Discharge spectrum
    s1 = tdc_FFT_Data(calc_id=ID, field_name='E_acc', xx=xx_discharge, power_2_flag=False)
    # Discharge spectrum
    s2 = tdc_FFT_Data(calc_id=ID, field_name='E_acc', xx=xx_out, power_2_flag=False)
    # PLOTTERS
    fp1=tdc_Fields_Plotter(f1)
    sp1=tdc_FFT_Plotter(s1)
    sp1.plot_ylabel = r'$I_k,\ x\in[%g,%g]$' % tuple(xx_discharge)
    sp2=tdc_FFT_Plotter(s2)
    sp2.plot_ylabel = r'$I_k,\ x\in[%g,%g]$' % tuple(xx_out)
    # MFP instance
    mpp = tdc_MPP_Comparative_Timeseries_V( (fp1,sp1,sp2), timeshots, fig_param=fig_param)
    return mpp


def tdc_mpp_v__e_n_fft(ID,timeshots,
                       xx_discharge,
                       moving_grid_dict=None,
                       fig_param=None):
    """
    for *timeshots* plots:
    [1] e/p number density
    [2] charge density
    [3] electric field
    --------
    Returns:
    --------
    ()=>  tdc_MPP_Comparative_Timeseries_V instance with the plot
    """
    # electric field
    f1 = tdc_Field_Data(calc_id=ID, field_name='E_acc')
    # electron and positron number densities
    f2_e = tdc_Field_Data(calc_id=ID, field_name='N', filename='prop_Electrons.h5' )
    f2_p = tdc_Field_Data(calc_id=ID, field_name='N', filename='prop_Positrons.h5' )
    # Discharge spectrum
    s1 = tdc_FFT_Data(calc_id=ID, field_name='E_acc', xx=xx_discharge, power_2_flag=False)
    # PLOTTERS
    fp1=tdc_Fields_Plotter(f1)
    fp2=tdc_EP_Density_Plotter(f2_e,f2_p)
    sp1=tdc_FFT_Plotter(s1)
    sp1.plot_ylabel = r'$I_k,\ x\in[%g,%g]$' % tuple(xx_discharge)
    if moving_grid_dict:
        fp1 = tdc_Moving_Grid_Plotter(fp1,moving_grid_dict)
        fp2 = tdc_Moving_Grid_Plotter(fp2,moving_grid_dict)
    # MFP instance
    mpp = tdc_MPP_Comparative_Timeseries_V( (fp1,sp1,fp2), timeshots, fig_param=fig_param)
    return mpp
