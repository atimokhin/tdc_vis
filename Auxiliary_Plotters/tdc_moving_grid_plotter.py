import matplotlib as mpl
import numpy      as np

class tdc_Moving_Grid_Plotter:
    """
    This class is responsible for plotting moving
    grids in movies or other specialized plots
    Members:
    --------
    plotter
    n_lines
    speed
    extend_grid_y
    grid_lines
    grid_xx0
    """

    def __init__(self, plotter, moving_grid_dict=None):
        """
        plotter
           main plotter
        moving_grid_dict
           dictionary with parameters
           moving_grid_dict = dict(n_lines=20, speed=1, extend_grid_y=[-1,1])
        """
        # wrap actual plotter
        self.plotter = plotter
        # extract parameters
        self.n_lines = moving_grid_dict['n_lines']
        self.speed   = moving_grid_dict['speed']
        self.extend_grid_y = moving_grid_dict.get('extend_grid_y')
        # initialize positions and lines list
        self.grid_lines = self.n_lines*[None]
        self.grid_xx0   = self.n_lines*[None]

    def __getattr__(self,attrname):
        "Redirect non-implemented requests to main plotter"
        return getattr(self.plotter, attrname)

    def plot(self,ax, **kwargs):
        """
        Call wrapped plotter and plot grid lines
        NB: **kwargs goes to ax.plot(..) and  self.plotter.plot(...)
            plotter should be tdc_Data_vs_X_Plotter (need xmin/xmax)
        """
        self.plotter.plot(ax,**kwargs)
        # axes limits
        ylims = ax.get_ylim()
        # initial grid positions [at t=0]
        self.xmax = self.plotter.xmax
        self.grid_xx0 = np.linspace(0,self.plotter.xmax,self.n_lines)
        # update positions for the current time
        t  = self.plotter.data[0].timetable.get_absolute_time()
        xx,yy = self._grid_lines_points(t,ylims)
        # filter grid lines  parameters from kwargs
        grid_lines_keys = ('animated',)
        grid_lines_kwargs = { k: kwargs[k] for k in grid_lines_keys if kwargs.has_key(k) }
        # plot grid lines
        for i,x  in enumerate(xx):
            self.grid_lines[i], = ax.plot( (x,x), yy, 'r',
                                           linewidth=0.75*mpl.rcParams['lines.linewidth'],
                                           **grid_lines_kwargs )

    def set_animated(self,val):
        "Set animated property in all lines"
        self.plotter.set_animated(val)
        for line in self.grid_lines:
            line.set_animated(val)

    def animation_update(self,ax,i_ts):
        "Read and plot field for animation at timestep# i_ts"
        # do main plot
        self.plotter.animation_update(ax,i_ts)
        # plot moving gris
        ylims = ax.get_ylim()
        # update grid line positions for the current time
        t  = self.plotter.data[0].timetable.get_absolute_time()
        xx,yy = self._grid_lines_points(t,ylims)
        # plot grid lines
        for line,x in zip(self.grid_lines, xx):
            line.set_xdata([x,x])
            line.set_ydata(yy)
        for line in self.grid_lines:    
            ax.draw_artist(line)        

    def _grid_lines_points(self,t, ylims):
        """
        return grid lines points at time t
        correct y if necessary
        """
        # x coordinates
        xx = self.grid_xx0 + self.speed*t
        xx = xx - np.fix(xx/self.xmax)*self.xmax
        if self.speed<0:
            xx = np.remainder((self.xmax+xx),self.xmax)
        # y coordinates
        yy = list(ylims)
        if self.extend_grid_y:
            yy[0] += self.extend_grid_y[0]
            yy[1] += self.extend_grid_y[1]
        return (xx,yy)
