import h5py

from Particles import tdc_XPs_Plotter
from Common    import tdc_Data_Sequence,  tdc_Filenames

class XPs_Plotter__OF:
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

    def __init__(self, xps, of__filename):
        """
        reads data for the theoretical curve and sets internal variables
        xps
           XP data to be plotted
        of__filename
           theoretical curve  p(x) for oscillation solution is in the file 'of__filename.h5'
        """
        # initialize XP plotter
        self.XP_Plotter=tdc_XPs_Plotter(xps)
        # calc_id -- need to read 'setup_properties.h5'
        if isinstance(xps[0], tdc_Data_Sequence):
            calc_id = xps[0].current_data.calc_id
        else:
            calc_id = xps[0].calc_id
        # read properties file
        h5_filename  = tdc_Filenames().get_full_filename(calc_id, 'setup_properties.h5')
        f0 = h5py.File(h5_filename,'r')
        L        = f0['/GridProps/L'].value
        dX       = f0['/GridProps/dX'].value
        f0.close()
        # interpolated values for p(x) from numerical solutions
        # of Child's equation
        # read hdf file with interpolation of p(x)
        f1 = h5py.File('_papers/sclf_1/OscillatingFlow/' + of__filename + '.h5','r')
        self.pp_itpl = f1['Dataset1'].value[:,1]
        self.xx_itpl = f1['Dataset1'].value[:,0]
        f1.close()
        # renormalize and off-set line (particle are injected at position -dX/2)
        self.xx_itpl = self.xx_itpl - dX/2
        # select points in the current domain
        mask = self.xx_itpl<=L
        self.xx_itpl = self.xx_itpl[mask]
        self.pp_itpl = self.pp_itpl[mask]
        # -----------------------------------------------------
        # initialize lines
        self.lines_theory = [None]

    def __getattr__(self,attrname):
        "Redirects all non-implemented requests to self.XP_Plotter"
        return getattr(self.XP_Plotter,attrname)

    def plot(self,ax,**kwargs):
        """
        - plot XP
        - plot theoretical lines
        """
        self.XP_Plotter.plot(ax,**kwargs)
        self.lines_theory, = ax.plot(self.xx_itpl, self.pp_itpl,
                                     '--r',
                                     linewidth=1,dashes=(3,2),
                                     **kwargs)


    def replot(self,ax):
        """
        - replot XP
        - draw theoretical lines
        """
        self.XP_Plotter.replot(ax)
        # theoretical lines
        self.lines_theory.set_xdata(self.xx_itpl)
        ax.draw_artist(self.lines_theory)

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
        self.lines_theory.set_animated(val)

    def animation_update(self,ax,i_ts):
        self.XP_Plotter.animation_update(ax,i_ts)
        self.update_plot(ax)

    def to_cell_coordinates(self,ax):
        if self.XP_Plotter.to_cell_coordinates(ax):
            self.xx_itpl /= self.XP_Plotter._Mesh.dx
            
    def to_x_coordinates(self,ax):
        if self.XP_Plotter.to_x_coordinates(ax):
            self.xx_itpl *= self.XP_Plotter._Mesh.dx
