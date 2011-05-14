import h5py
import numpy as np

from Particles import tdc_XP_Data, tdc_XPs_Plotter
from Common    import tdc_Data_Sequence, tdc_Data_Sequence_Initializer, tdc_Filenames


def plot_test_sclf_xp_movie(plot_module,
                            calc_ids,
                            particle_names,
                            ylim,
                            sample_dict=None,
                            xlim=None,
                            tt=None,
                            fps=None,
                            keep_frame_files=None,
                            moving_grid_dict=None,
                            use_cell_coordinates=False,
                            show_cells=False,
                            time_normalization=None,
                            **kwargs):
    """
    plots XP phase portrait movie on top of theoretical dependence p(x)
    for space charge limited flow
    """
    # make sure calc_id is a sequence
    if not isinstance( calc_ids, (list,tuple) ):
        calc_ids = (calc_ids,)
    # make sure particle_names is a sequence
    if not isinstance( particle_names, (list,tuple) ):
        particle_names = (particle_names,)
    # particles sequence
    xps=[]
    for pname in particle_names:
        xps.append(  tdc_Data_Sequence_Initializer( tdc_XP_Data,
                                                    calc_ids=calc_ids,
                                                    particle_name=pname,
                                                    sample_dict=sample_dict,
                                                    tt=tt,
                                                    time_normalization=time_normalization,
                                                    **kwargs) )
    # plotter
    pp  = test_sclf_XPs_Plotter(calc_ids[0],xps=xps)
    if use_cell_coordinates:
        pp.use_cell_coordinates()
    if show_cells:
        pp.show_cells_on()
    # plot moving grid if asked
    if moving_grid_dict:
        pp  = tdc_Moving_Grid_Plotter(pp,moving_grid_dict)
    # movie frames
    MF = plot_module.Movie.Single_Panel_Movie_Frames(pp, ylim=ylim, xlim=xlim)
    # movie_id - directory with the movie file
    movie_id = 'XP' + '_' + calc_ids[0]
    # -----------------------------------------
    # make movie
    plot_module.Movie.plot_movie( MF, movie_id, fps, keep_frame_files)



class test_sclf_XPs_Plotter:
    """
    This class is phase space portrait plotter superimposed on
    theoretical dependence for non-relativistic and ultra-relativistic
    space charge limited flow
    ==> all non-implemented requests are delegated to self.XP_Plotter
    -----------------
    -----------------
    can be used as a template for complex animation-capable plotters
    implements all necessary methods
    -----------------
    """
    
    def __init__(self, calc_id, xps):
        """
        sets internal variables
        calc_id
           need in order to read setup_properties.h5
        xps
           XP data to be plotted
        """
        # initialize XP plotter
        self.XP_Plotter=tdc_XPs_Plotter(xps)
        # get parameters for theoretical curves
        h5_filename  = tdc_Filenames().get_full_filename(calc_id, 'setup_properties.h5')
        f0 = h5py.File(h5_filename,'r')
        lambda_D = f0['/PlasmaProps/LambdaDebye'].value
        L        = f0['/GridProps/L'].value
        n_cells  = f0['/GridProps/NCells'].value
        dX       = f0['/GridProps/dX'].value
        f0.close()
        # interpolated values for p(x) from numerical solutions
        # of Child's equation
        # read hdf file with interpolation of p(x)
        f1 = h5py.File('x_Tests/sclf/sclf_j1.h5','r')
        self.pp_itpl = f1['Dataset1'].value[:,1]
        self.xx_itpl = f1['Dataset1'].value[:,0]
        # renormalize and off-set line (particle are injected at position -dX/2)
        self.xx_itpl = self.xx_itpl*lambda_D - dX/2
        # select points in the current domain
        mask = self.xx_itpl<=L
        self.xx_itpl = self.xx_itpl[mask]
        self.pp_itpl = self.pp_itpl[mask]
        # -----------------------------------------------------
        # analythical theoretical dependence p(x)
        self.xx = np.linspace(0,L,n_cells*5)
        self.pp_non_rel = 4.5**(1./3.)*(self.xx/lambda_D)**(2./3.)
        self.pp_rel     = np.sqrt(2)*(self.xx/lambda_D)
        # off-set line (particle are injected at position -dX/2)
        self.xx -= dX/2
        # initialize lines
        self.lines_theory = 3*[None]

    def __getattr__(self,attrname):
        "Redirects all non-implemented requests to self.XP_Plotter"
        return getattr(self.XP_Plotter,attrname)

    def plot(self,ax,**kwargs):
        """
        - plot XP
        - plot theoretical lines
        """
        self.XP_Plotter.plot(ax,**kwargs)
        self.lines_theory[0], = ax.plot(self.xx, self.pp_non_rel,'--g',**kwargs)
        self.lines_theory[1], = ax.plot(self.xx, self.pp_rel,'--m',**kwargs)
        self.lines_theory[2], = ax.plot(self.xx_itpl, self.pp_itpl,'-r',**kwargs)

    def replot(self,ax):
        """
        - replot XP
        - draw theoretical lines
        """
        self.XP_Plotter.replot(ax)
        # theoretical lines
        self.lines_theory[0].set_xdata(self.xx)
        self.lines_theory[1].set_xdata(self.xx)
        self.lines_theory[2].set_xdata(self.xx_itpl)
        for line in self.lines_theory:        
            ax.draw_artist(line)

    def update_plot(self,ax):
        """
        Plot particles for animation at timestep# i_ts
        """
        self.replot(ax)

    def set_animated(self,val):
        """
        Set animated property in XP and theoretical lines
        """
        self.XP_Plotter.set_animated(val)
        # theoretical lines        
        for line in self.lines_theory:
            line.set_animated(val)

    def animation_update(self,ax,i_ts):
        self.XP_Plotter.animation_update(ax,i_ts)
        self.update_plot(ax)

    def to_cell_coordinates(self,ax):
        if self.XP_Plotter.to_cell_coordinates(ax):
            self.xx /= self.XP_Plotter._Mesh.dx
            self.xx_itpl /= self.XP_Plotter._Mesh.dx
            
    def to_x_coordinates(self,ax):
        if self.XP_Plotter.to_x_coordinates(ax):
            self.xx *= self.XP_Plotter._Mesh.dx
            self.xx_itpl *= self.XP_Plotter._Mesh.dx
