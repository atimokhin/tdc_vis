import matplotlib as mpl

class tdc_rcParams(object):
    """
    Class with methods changing rcParams
    """
    @staticmethod
    def set_default():
        """
        - Forces lines to be drawn thicker (0.75 points)
        - Forces all mathematical labels to be rendered by matplotlib's mathtext
        """
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
    
    @staticmethod
    def set_latex():
        """
        Force all mathematical labels to be rendered by LaTeX
        """
        # let LaTeX draw all labels: necessary for complex labels
        mpl.rcParams['text.usetex']           = True
        mpl.rcParams['font.family']           = 'serif'
        mpl.rcParams['font.serif']            = 'Times'
        print '>>>> labels are rendered by LaTeX!'    
    
    @staticmethod
    def set_hardcopy():
        """
        - Force lines to be drawn thinner (0.5 points)
        - Force all mathematical labels to be rendered by LaTeX
        """
        mpl.rcParams['lines.antialiased']     = True   # render lines in antialised (no jaggies)
        mpl.rcParams['lines.linewidth']       = 0.5   # line width in points
        mpl.rcParams['lines.markeredgewidth'] = 0.5   # the line width around the marker symbol
        mpl.rcParams['patch.linewidth']       = 0.5   # edge width in points
        mpl.rcParams['axes.linewidth']        = 0.5   # edge linewidth
        mpl.rcParams['grid.linewidth']        = 0.5   # in points
        # let LaTeX draw all labels: necessary for complex labels
        tdc_rcParams.set_latex()
        print 'Set to     >>hardcopy<< rcParams!'
