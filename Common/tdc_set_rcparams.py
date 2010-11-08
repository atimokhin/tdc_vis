import matplotlib as mpl

__all__ = [ 'tdc_set_hardcopy_rcparams',
            'tdc_set_screen_rcparams',
            'tdc_set_presentation_rcparams',
            'tdc_set_default_rcparams',
            'tdc_set_hires_dpi'           ]


def tdc_set_hardcopy_rcparams():
    mpl.rcParams['lines.linewidth']       = 0.25   # line width in points
    mpl.rcParams['lines.markeredgewidth'] = 0.25   # the line width around the marker symbol
    mpl.rcParams['lines.antialiased']     = True   # render lines in antialised (no jaggies)
    mpl.rcParams['patch.linewidth']       = 0.25   # edge width in points
    mpl.rcParams['axes.linewidth']        = 0.25   # edge linewidth
    mpl.rcParams['grid.linewidth']        = 0.25   # in points
    mpl.rcParams['figure.dpi']            = 100

def tdc_set_screen_rcparams():
    mpl.rcParams['lines.linewidth']       = 0.5   # line width in points
    mpl.rcParams['lines.markeredgewidth'] = 0.5   # the line width around the marker symbol
    mpl.rcParams['lines.antialiased']     = True   # render lines in antialised (no jaggies)
    mpl.rcParams['patch.linewidth']       = 0.5   # edge width in points
    mpl.rcParams['axes.linewidth']        = 0.5   # edge linewidth
    mpl.rcParams['grid.linewidth']        = 0.5   # in points


def tdc_set_presentation_rcparams():
    pass

def tdc_set_default_rcparams():
    tdc_set_screen_rcparams()
    mpl.rcParams['figure.dpi'] = 100


def tdc_set_hires_dpi():
    mpl.rcParams['figure.dpi'] = 600

