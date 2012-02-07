import matplotlib as mpl

__all__ = [ 'tdc_set_default_rcparams',
            'tdc_set_latex_rcparams',
            'tdc_set_hardcopy_rcparams' ]

def tdc_set_default_rcparams():
    mpl.rcParams['lines.antialiased']     = True   # render lines in antialised (no jaggies)
    mpl.rcParams['lines.linewidth']       = 0.75   # line width in points
    mpl.rcParams['lines.markeredgewidth'] = 0.5    # the line width around the marker symbol
    mpl.rcParams['patch.linewidth']       = 0.5    # edge width in points
    mpl.rcParams['axes.linewidth']        = 0.75   # edge linewidth
    mpl.rcParams['grid.linewidth']        = 0.75   # in points
    # change fonts and text drawing to mathtext 
    mpl.rcParams['font.serif']            = 'Bitstream Vera Serif'
    mpl.rcParams['font.family']           = 'serif'
    mpl.rcParams['text.usetex']           = False
    mpl.rcParams['figure.dpi']            = 100
    print 'Set back to **default** rcParams!'


def tdc_set_latex_rcparams():
    # let LaTeX draw all labels: necessary for complex labels
    mpl.rcParams['text.usetex']           = True
    mpl.rcParams['font.family']           = 'serif'
    mpl.rcParams['font.serif']            = 'Times'
    print '>>>> labels are rendered by LaTeX!'    



def tdc_set_hardcopy_rcparams():
    mpl.rcParams['lines.antialiased']     = True   # render lines in antialised (no jaggies)
    mpl.rcParams['lines.linewidth']       = 0.5   # line width in points
    mpl.rcParams['lines.markeredgewidth'] = 0.5   # the line width around the marker symbol
    mpl.rcParams['patch.linewidth']       = 0.5   # edge width in points
    mpl.rcParams['axes.linewidth']        = 0.5   # edge linewidth
    mpl.rcParams['grid.linewidth']        = 0.5   # in points
    # let LaTeX draw all labels: necessary for complex labels
    tdc_set_latex_rcparams()
    print 'Set to     >>hardcopy<< rcParams!'
