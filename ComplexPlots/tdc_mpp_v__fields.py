from Fields import tdc_Field_Data
from Fields import tdc_Fields_Plotter
from Fields import tdc_EP_Density_Plotter

from Common.tdc_moving_grid_plotter       import tdc_Moving_Grid_Plotter

from MPP       import *


def tdc_mpp_v__e_rho_n(ID,timeshots,
                       moving_grid_dict=None,
                       **kwarg):
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
    mpp = tdc_MPP_Comparative_Timeseries_V( (fp1,fp2,fp3), timeshots, **kwarg)
    return mpp
