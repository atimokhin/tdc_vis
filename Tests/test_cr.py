import h5py
import matplotlib.pyplot as plt
import numpy as np

from Common import tdc_Filenames as tdc_Filenames

def  test_cr(calc_id,n_bins):

    F0=5.236e0
    # read Kcr table
    f = h5py.File('../tdc_main/_MC/Emission/Kcr.h5','r')
    eta_kcr = f['/Dataset1'][:]
    kcr     = f['/Dataset2'][:]/F0
    f.close()

    # --------------------------------------------
    # continuous photon emission -----------------
    filename = tdc_Filenames().get_full_filename(calc_id, 'photons_cr_cont.h5')
    f1 = h5py.File(filename,'r')
    EpsilonC = np.array(f1['EpsilonC'])
    Tau      = np.array(f1['Tau'])
    F_min    = np.array(f1['F_min'])
    n_cont   = np.array(f1['N'])
    # photon energies
    E = f1['E'][0:n_cont]/EpsilonC
    # photon weights
    W = f1['Weight'][1:n_cont]
    f1.close()

    # de - energy bins widths
    d_eta = np.diff(E)

    plt.subplot(1,2,1)
    plt.loglog( E[1:], W/(Tau/F_min)/d_eta,'r')
    plt.loglog(eta_kcr,kcr,'b')
    plt.xlabel(r'$\eta$')  
    plt.ylabel(r'$\kappa(\eta)/F(0)$')   

    print 'w_total_continuous = ', np.sum(W/Tau)
    del E, W, d_eta
    # --------------------------------------------


    # --------------------------------------------
    # discrete photon emission -------------------
    filename = tdc_Filenames().get_full_filename(calc_id, 'photons_cr_discrete.h5')
    f2 = h5py.File(filename,'r')
    EpsilonC = np.array(f2['EpsilonC'])
    Tau      = np.array(f2['Tau'])
    F_min    = np.array(f2['F_min'])
    n_discr  = np.array(f2['N'])
    # photon energies
    E        = f2['E'][0:n_discr]/EpsilonC
    f2.close()

    e_bins = np.logspace(np.log10(E.min()),np.log10(E.max()),n_bins)
    p, bin_edges = np.histogram( E, bins=e_bins )
    bins = 0.5*(bin_edges[0:-1]+bin_edges[1:])

    # de - energy bins widths
    d_e = np.diff(e_bins)

    plt.subplot(1,2,2)
    p = p/(Tau/F_min)/d_e
    plt.loglog(bins, p, 'r',drawstyle='steps-mid')
    plt.loglog(eta_kcr,kcr,'b')
    plt.xlabel(r'$\eta$')  

    print 'w_total_discrete = ', np.sum(p/Tau)



