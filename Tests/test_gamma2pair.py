import h5py
import matplotlib.pyplot as plt

from Particles import tdc_XP_Data


def test_gamma2pairs( xmin, xmax, n_bins ):

    f_xp = tdc_XP_Data('test_absorption','Pairs')
    f_xp.read(1)
    print f_xp.x_cr
    
    n, bins, patches = plt.hist(f_xp.x_cr, bins=n_bins)
    ax = plt.gca()

    aa = (bins[1]-bins[0])*f_xp.x.size

    f = h5py.File('../RESULTS/test_absorption/dndx_itgr.h5','r')
    ax.plot(f['X'],aa*f['dNdX'])
    f.close()
    ax.set_xlim([xmin,xmax]);
    ax.set_xlabel('x')    
    ax.set_ylabel(r'$dn_{pair}/dx$')  

    f1 = h5py.File('../RESULTS/test_absorption/photons.h5','r')
    ax.plot(f1['X0'],0,'o',markersize=9)
    f1.close()
    plt.draw()
