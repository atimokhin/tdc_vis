def tdc_save_figure(manip,filename,*args, **kwargs):
    """
    Saves figure from Manipulator manip in the output directory as filename
    """
    filename='../RESULTS_VIS/Figs/' + filename
    manip.fig.savefig(filename,*args,**kwargs)
