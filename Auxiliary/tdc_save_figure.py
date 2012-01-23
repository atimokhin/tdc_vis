from tdc_filenames  import tdc_Filenames

def tdc_save_figure(manip,filename,vis_id,*args,**kwargs):
    """
    Saves figure from Manipulator manip 
    Figure is saved in file:
       'tdc_Filenames.__VisResultsDir/vis_id/filename'

    manip    - manip to be saved (calls manip.fog.savefig)
    filename - name of the file (with suffix!)
    vis_id   - name of the subdirectory withing tdc_Filenames's __VisResultsDir
    """
    filename=tdc_Filenames().get_full_vis_filename(vis_id, filename)
    manip.fig.savefig(filename,*args,**kwargs)
    print '\nFigure is saved as "%s" \n' % filename
