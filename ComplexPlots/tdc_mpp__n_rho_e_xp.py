import Fields
from Fields import tdc_Field_Data
from Fields import tdc_Fields_Plotter
from Fields import tdc_EP_Density_Plotter

import Particles
from Particles  import tdc_XP_Data
from Particles  import tdc_XPs_Plotter

from MPP        import *

def tdc_mpp__n_rho_e_xp(ID,timeshots,**kwargs):
    """
    plots e/p number density, charge density, and electric field for
    timeshots, returns tdc_MPP_Comparative_Timeseries_H instance with the
    plot
    """
    # DATA ---------------------
    # electron and positron number densities
    f1_e = tdc_Field_Data(calc_id=ID, field_name='N', filename='prop_Electrons.h5' )
    f1_p = tdc_Field_Data(calc_id=ID, field_name='N', filename='prop_Positrons.h5' )
    # charge density
    f2 = tdc_Field_Data(ID, 'Rho')
    # electric field
    f3 = tdc_Field_Data(ID, 'E_acc')
    # phase space portraits
    sample_dict = kwargs.get('sample_dict',dict(name='regular',n_reduce=10,n_min=200))
    xp_e = tdc_XP_Data(ID, 'Electrons', sample_dict)
    xp_p = tdc_XP_Data(ID, 'Positrons', sample_dict)
    xp_g = tdc_XP_Data(ID, 'Pairs',     sample_dict)
    # PLOTTERS -----------------
    # fields
    p1 = tdc_EP_Density_Plotter(f1_e,f1_p)
    p2 = tdc_Fields_Plotter(f2)
    p3 = tdc_Fields_Plotter(f3)
    # xp
    p4 = tdc_XPs_Plotter( (xp_p,) )
    p5 = tdc_XPs_Plotter( (xp_e,) )
    p6 = tdc_XPs_Plotter( (xp_g,) )
    # MFP instance -------------
    mpp = tdc_MPP_Comparative_Timeseries_H( (p1,p2,p3,p4,p5,p6), timeshots, **kwargs)
    return mpp



