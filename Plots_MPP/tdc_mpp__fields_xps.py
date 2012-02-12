import Fields
from Fields import tdc_Field_Data
from Fields import tdc_Fields_Plotter
from Fields import tdc_EP_Density_Plotter

import Particles
from Particles  import tdc_XP_Data
from Particles  import tdc_XPs_Plotter

from MPP        import *


def tdc_mpp__n_rho_e_xp(ID,timeshots,sample_dict=None,fig_param=None):
    """
    for *timeshots* plots:
    [1] e/p number density
    [2] charge density
    [3] electric field
    XP for:
    [4] (e)lectrons,
    [5] (p)ositrons,
    [6] (g)amma-rays
    --------
    Returns:
    --------
    ()=>  tdc_MPP_Comparative_Timeseries_H instance with the plot
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
    if not sample_dict:
        sample_dict = dict(name='regular',n_reduce=10,n_min=200)
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
    mpp = tdc_MPP_Comparative_Timeseries_H( (p1,p2,p3,p4,p5,p6), timeshots, fig_param=fig_param)
    return mpp



def tdc_mpp__n_rho_j_e_xp(ID,timeshots,sample_dict=None,fig_param=None):
    """
    for *timeshots* plots:
    [1] e/p number density
    [2] charge density
    [3] current density
    [4] electric field
    XP for:
    [5] (e)lectrons,
    [6] (p)ositrons,
    [7] (g)amma-rays
    --------
    Returns:
    --------
    ()=>  tdc_MPP_Comparative_Timeseries_H instance with the plot
    """
    # DATA ---------------------
    # electron and positron number densities
    f1_e = tdc_Field_Data(calc_id=ID, field_name='N', filename='prop_Electrons.h5' )
    f1_p = tdc_Field_Data(calc_id=ID, field_name='N', filename='prop_Positrons.h5' )
    # charge density
    f2 = tdc_Field_Data(ID, 'Rho')
    # current density
    f3 = tdc_Field_Data(ID, 'J')
    # electric field
    f4 = tdc_Field_Data(ID, 'E_acc')
    # phase space portraits
    if not sample_dict:
        sample_dict = dict(name='regular',n_reduce=10,n_min=200)
    xp_e = tdc_XP_Data(ID, 'Electrons', sample_dict)
    xp_p = tdc_XP_Data(ID, 'Positrons', sample_dict)
    xp_g = tdc_XP_Data(ID, 'Pairs',     sample_dict)
    # PLOTTERS -----------------
    # fields
    p1 = tdc_EP_Density_Plotter(f1_e,f1_p)
    p2 = tdc_Fields_Plotter(f2)
    p3 = tdc_Fields_Plotter(f3)
    p4 = tdc_Fields_Plotter(f4)
    # xp
    p5 = tdc_XPs_Plotter( (xp_p,) )
    p6 = tdc_XPs_Plotter( (xp_e,) )
    p7 = tdc_XPs_Plotter( (xp_g,) )
    # MFP instance -------------
    mpp = tdc_MPP_Comparative_Timeseries_H( (p1,p2,p3,p4,p5,p6,p7), timeshots, fig_param=fig_param)
    return mpp


def tdc_mpp__n_rho_j_e_xp_epgp(ID,timeshots,sample_dict=None,fig_param=None):
    """
    for *timeshots* plots:
    [1] e/p number density
    [2] charge density
    [3] current density
    [4] electric field
    XP for:
    [5] (e)lectrons,
    [6] (p)ositrons,
    [7] (g)amma-rays
    [8] (p)rotons
    --------
    Returns:
    --------
    ()=>  tdc_MPP_Comparative_Timeseries_H instance with the plot
    """
    # DATA ---------------------
    # electron and positron number densities
    f1_e = tdc_Field_Data(calc_id=ID, field_name='N', filename='prop_Electrons.h5' )
    f1_p = tdc_Field_Data(calc_id=ID, field_name='N', filename='prop_Positrons.h5' )
    # charge density
    f2 = tdc_Field_Data(ID, 'Rho')
    # current density
    f3 = tdc_Field_Data(ID, 'J')
    # electric field
    f4 = tdc_Field_Data(ID, 'E_acc')
    # phase space portraits
    if not sample_dict:
        sample_dict = dict(name='regular',n_reduce=10,n_min=200)
    xp_e = tdc_XP_Data(ID, 'Electrons', sample_dict)
    xp_p = tdc_XP_Data(ID, 'Positrons', sample_dict)
    xp_g = tdc_XP_Data(ID, 'Pairs',     sample_dict)
    xp_pr = tdc_XP_Data(ID, 'Protons',     sample_dict)
    # PLOTTERS -----------------
    # fields
    p1 = tdc_EP_Density_Plotter(f1_e,f1_p)
    p2 = tdc_Fields_Plotter(f2)
    p3 = tdc_Fields_Plotter(f3)
    p4 = tdc_Fields_Plotter(f4)
    # xp
    p5 = tdc_XPs_Plotter( (xp_p,) )
    p6 = tdc_XPs_Plotter( (xp_e,) )
    p7 = tdc_XPs_Plotter( (xp_g,) )
    p8 = tdc_XPs_Plotter( (xp_pr,) )
    # make Protons markersize equal to those of the other particles
    p8.change_default_plotstyle('Protons',markersize=1)
    # MFP instance -------------
    mpp = tdc_MPP_Comparative_Timeseries_H( (p1,p2,p3,p4,p5,p6,p7,p8), timeshots, fig_param=fig_param)
    return mpp
