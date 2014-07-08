if __name__ == '__main__':
    import tdc_vis
    
import matplotlib.pyplot as plt

from ATvis.Common_Data_Plot import *

from Auxiliary        import *
from FMCI             import *
from x_PlottingFunctions.MPP import tdc_mpp__xp_xpdensity

from mpp_params import mpp_params
# ================================================
# Figure parameters for MPP plot
# ================================================
# adjust standard figure parameters
mpp_params['top_margin_abs']   = .05  # redeuce marging on top
mpp_params['right_margin_abs'] = .5   # accomidate colorbar
# additional parameters for plot with colorbar
mpp_params['dx_cbar_abs']                 = .1
mpp_params['dy_cbar_abs']                 = 2.9
mpp_params['dx_cbar_pad_from_ax_abs']     = 0.1
mpp_params['dy_cbar_pad_from_center_abs'] = -0.85;
# ================================================


#------------------------------------
# parameters for specific cases
#------------------------------------
tdc_Filenames.set_results_dir('../RESULTS/WD2TB/FMC_1')


plot_flag='SCLF_superGJ'
# plot_flag='RS'

    
if ( plot_flag == 'SCLF_superGJ' ):
    ID='SCLF__Crab_B1_R8.8e6_jm1.5_P0.033_Chi60_L0.3_nGJ5e4_nx1e4_dt1e-5_sU'
    i_ts=480
    wlims=[1e-2,11]
    xlims=[-0.01,0.31]
elif ( plot_flag == 'RS' ):
    ID='RS__Crab_B1_R8.6e6_jp1_P0.033_L0.2_nGJ5e4_nx1e4_dt8e-6_sU_a'
    i_ts=473
    wlims=[1e-2,11]
    xlims=[-0.01,0.21]
#------------------------------------



# ================================================
# plotting commands
# ================================================
# sample and partition for plots
sample_dict = dict(name='regular',n_reduce=2,n_min=1000)
xp_partition=tdc_FMCI_XP_Partition__LinSemiLogUniform( x_dict=dict(n=400,xx=None),
                                                       p_dict=dict(n=100,pp=[1,5e8]) )
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
AT_rcParams.set_hardcopy()
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# main plot command
mpp=tdc_mpp__xp_xpdensity(ID,
                          i_ts,
                          wlims,
                          xp_partition,
                          sample_dict=sample_dict,
                          fig_param=mpp_params)
# x-label
mpp.set_bottom_xlabel(0, r'$x$')
# ticks and limits on the plot -------
# x-axis
mpp.set_xlim( xlims )
# mpp.set_xticks(np.arange(0,0.4,.1))
# mpp.set_xticklabels(['0','0.1','0.2','0.3'])
# mpp.set_xticks(np.arange(0.02,0.32,.02), minor=True)
mpp.set_xticks(np.arange(0,0.3,.1))
mpp.set_xticklabels(['0','0.1','0.2'])
mpp.set_xticks(np.arange(0.02,0.22,.02), minor=True)
# y-axis
mpp.set_ylim( 0, [-5e8,5e8] )
mpp.set_yticks(0, [-1e8,-1e4,0,1e4,1e8])
# ------------------------------------
plt.show()

