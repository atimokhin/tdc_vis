import h5py
import matplotlib.pyplot as plt
import numpy as np

from Auxiliary  import tdc_Filenames as tdc_Filenames
from Auxiliary  import tdc_Mesh      as tdc_Mesh

def pairs_from_single_particle( calc_id,
                                n_bins_e,
                                n_bins_x,
                                xlim1=None,
                                ylim1=None,
                                ylim2=None ):
    
    # read photons --------------------------
    filename = tdc_Filenames.get_full_filename(calc_id, 'cache_photons.h5')
    f2 = h5py.File(filename,'r')
    # number of emitted photons
    n_ph = f2['N'].value
    # photon energies
    E = f2['E'].value[0:n_ph]
    # position of emitting particle
    X0 = f2['X0'].value
    f2.close()
    # photon histogram ---------------------
    e_bins = np.logspace(np.log10(E.min()),np.log10(E.max()),n_bins_e)
    d_e = np.diff(e_bins)
    p, bin_edges = np.histogram( E, bins=e_bins )
    bins = 0.5*(bin_edges[0:-1]+bin_edges[1:])
    # figure <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    fig, (ax1,ax2) = plt.subplots(1,2,figsize=(12, 6))
    # plot photon spectrum -----------------
    ax1.loglog(bins, bins*p/d_e, 'r',drawstyle='steps-mid')
    if xlim1: ax1.set_xlim(xlim1)
    if ylim1: ax1.set_ylim(ylim1)
    ax1.set_xlabel(r'$E_{\gamma}$')  
    ax1.set_ylabel(r'$E\;dN_\gamma/dE$')  
    # read pairs ---------------------------
    filename = tdc_Filenames.get_full_filename(calc_id, 'cache_pairs.h5')
    f0 = h5py.File(filename,'r')
    # number of pairs
    n_pairs = f0['N'].value
    # positions of injected pairs
    x_cr    = f0['X_cr'].value[0:n_pairs]
    f0.close()
    # read mesh ----------------------------
    mesh = tdc_Mesh(calc_id)
    # photon histogram ---------------------
    x_bins = np.linspace(x_cr.min(),x_cr.max(),n_bins_x)
    p, bin_edges = np.histogram( x_cr, bins=x_bins )
    bins = 0.5*(bin_edges[0:-1]+bin_edges[1:])
    dx = x_bins[1]-x_bins[0]
    # plot pair spatial distribution -------
    ax2.plot(bins, p/dx/n_ph, 'b',drawstyle='steps-mid')
    ax2.plot(X0,0,'o',markersize=9)
    ax2.set_xlim(mesh.xmin,mesh.xmax)
    if ylim2: ax2.set_ylim(ylim2)
    ax2.set_xlabel(r'$x$')  
    ax2.set_ylabel(r'$1/N_{\gamma}\;dN_{e^\pm}/dx$')  
    
