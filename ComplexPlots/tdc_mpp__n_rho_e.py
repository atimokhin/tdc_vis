import Fields
from Fields import tdc_Field_Data
from Fields import tdc_Fields_Plotter
from Fields import tdc_EP_Density_Plotter

from MPP       import *

def tdc_mpp__n_rho_e(ID,timeshots,**kwarg):
    """
    plots e/p number density, charge density, and electric field for
    timeshots, returns tdc_MPP_Comparative_Timeseries_H class instance with the
    plot
    """
    # electron and positron number densities
    f1_e = tdc_Field_Data(calc_id=ID, field_name='N', filename='prop_Electrons.h5' )
    f1_p = tdc_Field_Data(calc_id=ID, field_name='N', filename='prop_Positrons.h5' )
    # charge density
    f2 = tdc_Field_Data(calc_id=ID, field_name='Rho')
    # electric field
    f3 = tdc_Field_Data(calc_id=ID, field_name='E_acc')
    # PLOTTERS
    fp1=tdc_EP_Density_Plotter(f1_e,f1_p)
    fp2=tdc_Fields_Plotter(f2)
    fp3=tdc_Fields_Plotter(f3)
    # MFP instance
    mpp = tdc_MPP_Comparative_Timeseries_H( (fp1,fp2,fp3), timeshots, **kwarg)
    return mpp



