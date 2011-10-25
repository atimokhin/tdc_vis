import h5py
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import ATbase as AT

from Auxiliary import tdc_Filenames
from Particles import tdc_XP_Data


def test_single_particle_acceleration(calc_id='test_single_particle_acceleration',
                                      particle_name='Electrons'):

    """
    plots particle trajectories
    """
    # setup parameters =======================
    infile=AT.FileInput()
    infile.ReadFile(tdc_Filenames().get_full_filename(calc_id, 'cascade.input'))
    infile.ChangeGroup('ELECTRODYNAMICS::Electrostatic_1D::BoundaryConditions_Phi')
    dV = infile.get_param('dV')
    infile.ChangeGroup()
    # parameters of computation region -------
    filename = tdc_Filenames().get_full_filename(calc_id, 'setup_properties.h5')
    f1 = h5py.File(filename,'r')
    xmax = f1['GridProps/L'].value
    dT   = f1['GridProps/dT'].value
    p_cf = f1['PulsarGapProps/Pcf'].value
    f1.close()
    # particles parameters
    filename = tdc_Filenames().get_full_filename(calc_id, particle_name + '.h5')
    f2 = h5py.File(filename,'r')
    Q = f2['/PROPERTIES/Charge'].value
    M = f2['/PROPERTIES/Mass'].value
    f2.close()
    # constant in analythical particle equation of motion
    A = - p_cf * Q/M * dV/xmax
    # read particle data =====================
    sample_dict = dict(name='regular',n_reduce=1,n_min=1000)
    # XP data
    xp = tdc_XP_Data( calc_id,
                      particle_name=particle_name,
                      sample_dict=sample_dict)
    xx=[]
    pp=[]
    idx=[]
    n_ts = xp.timetable.get_number_of_timeshots()
    # read positions and momentum of particle
    for i in range(n_ts):
        xp.read(i+1)
        if len(xp.x):
            idx.append(i)
            xx.append(xp.x[0])
            pp.append(xp.p[0])
    tt = xp.timetable.to_absolute_time(xp.timetable.get_time_array()[idx])
    # transform Python lists into ndarrays
    xx = np.array(xx)
    pp = np.array(pp)
    tt = np.array(tt)
    #print 'pp ', pp, '\n xx ',xx, '\n tt ',tt
    # figure <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2,figsize=(11, 8))
    fig.suptitle('Single particle acceleration: Q=%g; M=%g;  P_cf=%g' % (Q,M,p_cf) )
    # axes formatter
    formatter=matplotlib.ticker.ScalarFormatter()
    formatter.set_powerlimits((-3, 4))
    # p vs x ---------------------
    # particle data
    ax1.plot(xx, pp, 'ro')
    ax1.set_xlim([0,xmax]);
    ax1.set_xlabel(r'$x$')    
    ax1.set_ylabel(r'$p$')  
    # theoretical curve **********
    pp_theory = math.copysign(1,A) * np.sqrt( (np.sqrt(1+pp[0]**2) + A*(xx-xx[0]))**2 - 1 ) - 0.5*A*dT
    # correct for the initial codition
    pp_theory[0] += 0.5*A*dT
    ax1.plot(xx, pp_theory, 'b-')
    # residual ..............
    ax3.semilogy(xx, abs( (pp_theory-pp)/pp ), 'b-')
    ax3.set_xlim([0,xmax]);
    ax3.set_xlabel(r'$x$')    
    ax3.set_ylabel(r'$(p-p_{th})/p$')  
    #ax3.yaxis.set_major_formatter(formatter)
    # x vs t ---------------------
    ax2.plot(tt, xx, 'go')
    ax2.set_xlim([0,tt[-1]]);
    ax2.set_ylim([0,xmax]);
    ax2.set_xlabel(r'$t$')    
    ax2.set_ylabel(r'$x$')  
    # theoretical curve ....
    xx_theory = (np.sqrt( 1 + (pp[0]+A*tt)**2 ) - np.sqrt(1+pp[0]**2) )/A + xx[0]
    ax2.plot(tt, xx_theory, 'b-')
    # residual ..............
    ax4.semilogy(tt, (xx_theory-xx)/xx, 'b-')
    ax4.set_xlim([0,tt[-1]]);
    ax4.set_xlabel(r'$t$')    
    ax4.set_ylabel(r'$(x-x_{th})/x$')  
    ax4.yaxis.set_major_formatter(formatter)
   

if __name__ == "__main__":
    test_single_particle_acceleration()
    plt.show()
