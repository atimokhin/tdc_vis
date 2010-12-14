import h5py
import matplotlib.pyplot as plt


def test_absorption( xmin, xmax, n_bins ):
    """
    plots histogram with positions of absorbed photons
    and theoretical curve showing distribution of absorbed photon positions
    obtained by direct numerical integration of the cross-section

    Photon emission  point is shown by a red dot
    """
    f0 = h5py.File('../RESULTS/test_absorption/cache_pairs.h5','r')
    n_pairs = f0['N'].value
    x_cr    = f0['X_cr'].value[0:n_pairs]
    f0.close()
    n, bins, patches = plt.hist(x_cr, bins=n_bins)
    ax = plt.gca()
    aa = (bins[1]-bins[0])*x_cr.size

    f1 = h5py.File('../RESULTS/test_absorption/dndx_itgr.h5','r')
    x_dNdX = f1['X'].value
    dNdX   = f1['dNdX'].value
    f1.close()
    ax.plot(x_dNdX, aa*dNdX)
    ax.set_xlim([xmin,xmax]);
    ax.set_xlabel('x')    
    ax.set_ylabel(r'$dn_{pair}/dx$')  

    f2 = h5py.File('../RESULTS/test_absorption/cache_photons.h5','r')
    ax.plot(f1['X0'],0,'o',markersize=9)
    f2.close()

    plt.show()
