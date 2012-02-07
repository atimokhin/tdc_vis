import  matplotlib.pyplot as     plt
from    matplotlib.cbook  import flatten

from tdc_mpp_figure_geometry import tdc_MPP_FigureGeometry

                       
class tdc_MPP:
    """
    Multiple Panel Plot
    This is the class which creates figure for MPP plots! 
    --------
    Members:
    --------
    fg
    fig
    grid
    x_labelled_axes
    y_labelled_axes
    """
    __default_label_fontsize     = 11
    __default_ticklabel_fontsize = 8
    __default_timelabel_format   = '%.3f'
    __default_timelabel_fontsize = 8

    def __init__(self,nx,ny, **kwargs):
        """
        This function setup figure and axes grid (nx x ny),
        changes fonts and creates
        x_labelled_axes, y_labelled_axes  lists
        ---------------
        Options:
        ---------------
        _label_fontsize
            size of labels            [ 10 ]
        _ticklabel_fontsize
            fontsize of ticklabels    [ 8 ]
        timelabel_format
           string format for timelabel [ '%.3f' ]
        timelabel_fontsize
           font size for timelabel     [ 8 ]
        """
        # by default set into interactive mode
        self.interactive=True
        # ----------------------------------------
        # setup
        # ----------------------------------------
        self.nx = nx
        self.ny = ny
        #figure geometry
        self.fg = tdc_MPP_FigureGeometry(nx,ny,**kwargs) 
        # figure object
        self.fig = plt.figure( figsize=self.fg.get_figsize_abs(), facecolor='w' )
        # grid of axes
        self.grid=[ [self.fig.add_axes( self.fg.axes_rectangle(i,j) ) for j in range(0,nx)]\
                    for i in range(0,ny) ]
        # setup label fontsizes
        self._label_fontsize = kwargs.get('label_fontsize',
                                          tdc_MPP.__default_label_fontsize)
        self._ticklabel_fontsize = kwargs.get('ticklabel_fontsize',
                                              tdc_MPP.__default_ticklabel_fontsize)
        # set timelabel formats
        self._timelabel_format = kwargs.get('timelabel_format',
                                            self.__default_timelabel_format)
        self._timelabel_fontsize = kwargs.get('timelabel_fontsize',
                                              self.__default_timelabel_fontsize)
        
    
    def _change_fonsize(self,axes_list):
        "function for changing fontsize for axes"
        for ax in axes_list:
            for label in ax.xaxis.get_ticklabels():
                label.set_size(self._ticklabel_fontsize)
            for label in ax.yaxis.get_ticklabels():
                label.set_size(self._ticklabel_fontsize)
            
    def _delete_xlabels_for_middle_plots(self):
        "delete x labels in all but bottom plots"
        for i in range(0,self.ny-1):
            for j in range(0,self.nx):
                self.grid[i][j].xaxis.set_ticklabels([])
            

    def set_ylabel(self,i,label):
        "function for labeling of i'th row"
        coord = self.fg.left_ylabel_pos(i)
        return self.fig.text( *coord, s=label, va='center',ha='left', size=self._label_fontsize)

    def set_top_xlabel(self,j, label):
        "function for labeling of j'th column"
        coord = self.fg.top_xlabel_pos(j)
        return self.fig.text( *coord, s=label, va='top',ha='center', size=self._label_fontsize)
    
    def set_bottom_xlabel(self,j, label):
        "function for labeling coordinates of j'th column "
        coord = self.fg.bottom_xlabel_pos(j)
        return self.fig.text( *coord, s=label, va='bottom',ha='center', size=self._label_fontsize)

    def set_xlim(self, *args, **kwargs):
        "call set_xlim command for each axes in grid"
        for ax in flatten(self.grid):
            ax.set_xlim(*args, **kwargs)
        if self.interactive: self.fig.canvas.draw()

    def set_xticks(self, *args, **kwargs):
        "call set_ticks for each xaxis in the grid"
        for ax in flatten(self.grid):
            ax.xaxis.set_ticks(*args, **kwargs)
        if self.interactive: self.fig.canvas.draw()

    def set_xticklabels(self, labels, tex=True, *args, **kwargs):
        """
        call set_ticklabels for each xaxis in the grid,
        if tex is True, format each label L as "$L$"
        """
        # format in TeX mathmode if necessary
        if tex:
            labels = ['$'+l+'$' for l in labels]
        # set labels for x labelled axes
        for ax in self.x_labelled_axes:
            ax.xaxis.set_ticklabels(labels,*args, **kwargs)
        if self.interactive: self.fig.canvas.draw()

    def set_window_title(self,title_str):
        """
        Set window title
        if backend do not have window - print the title
        """
        try:
            title=self.fig.canvas.manager.window.get_title()
            self.fig.canvas.set_window_title(title+':'+title_str) 
        except AttributeError:
            print title_str 
            
    def interactive_on(self):
        """
        set into interactive mode: changes to figure are plotted
        immediately
        """
        self.interactive=True

    def interactive_off(self):
        """
        switch off interactive mode: changes to figure delayed till
        draw is called
        """
        self.interactive=False


class tdc_MPP_H(tdc_MPP):
    """
    Multiple Panel Plot
    Horizontally alighned similar plots
    
    Members:
    x_labelled_axes
    y_labelled_axes
    """

    def __init__(self,nx,ny, **kwargs):
        """
        Call tdc_MPP.__init__
        Set y_labelled_axes and x_labelled_axes
        """
        tdc_MPP.__init__(self,nx,ny, **kwargs)
        # get rid of top tick labels
        self._delete_xlabels_for_middle_plots()
        # get rid of right tick labels
        self._delete_ylabels_for_middle_plots()
        # list of labelled axis
        self.y_labelled_axes=[ self.grid[i][0]     for i in range(0,ny) ]
        self.x_labelled_axes=[ self.grid[ny-1][j]  for j in range(0,nx) ]
        # change all axes fontsizes
        self._change_fonsize(self.y_labelled_axes)
        self._change_fonsize(self.x_labelled_axes)

    def _delete_ylabels_for_middle_plots(self):
        "delete y labels in all but leftmost plots"
        for i in range(0,self.ny):
            for j in range(1,self.nx):
                self.grid[i][j].yaxis.set_ticklabels([])

    def set_yscale(self, rows, type='linear', linthreshy=5):
        "call set_yscale command for each axes in the i'th row"
        for i in flatten([rows]):
            for ax in self.grid[i]:
                ax.set_yscale(type, linthreshy=linthreshy)
        if self.interactive: self.fig.canvas.draw()
            
    def set_ylim(self, rows, *args, **kwargs):
        "call set_ylim command for each axes in the i'th row"
        for i in flatten([rows]):
            for ax in self.grid[i]:
                ax.set_ylim(*args, **kwargs)
        if self.interactive: self.fig.canvas.draw()

    def set_yticks(self, rows, *args, **kwargs):
        "call set_ticks for each yaxis in rows"
        for i in flatten([rows]):
            for ax in self.grid[i]:
                ax.yaxis.set_ticks(*args, **kwargs)
        if self.interactive: self.fig.canvas.draw()

    def set_yticklabels(self, rows, labels,tex=False, *args, **kwargs):
        """
        call set_ticklabels for labelled yaxis in the i'th row,
        if tex is True, format each label L as "$L$"
        """
        # format in TeX mathmode if necessary
        if tex: labels = ['$'+l+'$' if len(l)!=0 else l  for l in labels]
        # set labels for y labelled axes
        for i in flatten([rows]):
            self.grid[i][0].yaxis.set_ticklabels(labels,*args, **kwargs)
        if self.interactive: self.fig.canvas.draw()


class tdc_MPP_V(tdc_MPP):
    """
    Multiple Panel Plot
    Vertically alighned similar plots

    Members:
    x_labelled_axes
    y_labelled_axes
    """

    def __init__(self,nx,ny, **kwargs):
        """
        Call tdc_MPP.__init__
        Set y_labelled_axes and x_labelled_axes
        """
        tdc_MPP.__init__(self,nx,ny, **kwargs)
        # get rid of top tick labels
        self._delete_xlabels_for_middle_plots()
        # list of labelled axis
        self.y_labelled_axes=flatten(self.grid)
        self.x_labelled_axes=[ self.grid[ny-1][j]  for j in range(0,nx) ]
        # change all axes fontsizes
        self._change_fonsize(self.y_labelled_axes)
        self._change_fonsize(self.x_labelled_axes)
    
    def set_yscale(self, columns, type='linear', linthreshy=5):
        "call set_yscale command for each axes in the j'th column"
        for j in flatten([columns]):
            for ax in [ axs[j] for axs in self.grid ]:
                ax.set_yscale(type, linthreshy=linthreshy)
        if self.interactive: self.fig.canvas.draw()

    def set_ylim(self, columns, *args, **kwargs):
        "call set_ylim command for each axes in the j'th column"
        for j in flatten([columns]):
            for ax in [ axs[j] for axs in self.grid ]:
                ax.set_ylim(*args, **kwargs)
        if self.interactive: self.fig.canvas.draw()

    def set_yticks(self, columns, *args, **kwargs):
        "call set_ticks for each yaxis in rows"
        for j in flatten([columns]):
            for ax in [ axs[j] for axs in self.grid ]:
                ax.yaxis.set_ticks(*args, **kwargs)
        if self.interactive: self.fig.canvas.draw()

    def set_yticklabels(self, columns, labels,tex=False, *args, **kwargs):
        """
        call set_ticklabels for labelled yaxis in the i'th row,
        if tex is True, format each label L as "$L$"
        """
        # format in TeX mathmode if necessary
        if tex: labels = ['$'+l+'$' if len(l)!=0 else l  for l in labels]
        # set labels for y labelled axes
        for j in flatten([columns]):
            for ax in [ axs[j] for axs in self.grid ]:
                ax.yaxis.set_ticklabels(labels,*args, **kwargs)
        if self.interactive: self.fig.canvas.draw()



