import numpy as np
from Particles import tdc_plot_xp


def test_sclf(calc_id,i_ts,j=1):

    def p_rel(x,j):
        gamma = 1 + np.sqrt(2*j)*x + 0.5*(j-1) * x**2
        return np.sqrt(gamma**2-1)
        
    def p_nonrel(x,j):
        return 1.651*pow(j,1./3)*pow(x,2./3)

    manip_xp=tdc_plot_xp(calc_id, i_ts, particle_names=('Electrons',), print_id=True)

    ax=manip_xp.fig.gca()
    xlim = ax.get_xlim()
    xx = np.linspace(xlim[0],xlim[1],1000)

    ax.plot(xx,p_rel(xx,j),'k--')
    ax.plot(xx,p_nonrel(xx,j),'r--')
    manip_xp.fig.canvas.draw()
