class tdc_Filenames:
    """
    class with methods for retriving full filename and setting sesults directory
    There are twom types of results directories:
        RESULTS     -- computation data
        RESULTS_VIS -- results of visualization (movie/pictures)
    """

    __default_ResultsDir    ='../RESULTS/'
    __default_VisResultsDir ='../RESULTS_VIS/'

    __ResultsDir    = __default_ResultsDir
    __VisResultsDir = __default_VisResultsDir

    def set_results_dir(self, name=__default_ResultsDir):
        tdc_Filenames.__ResultsDir=name

    def get_results_dir(self):
        return tdc_Filenames.__ResultsDir

    def get_full_filename(self,calc_id,fielname):
        return tdc_Filenames.__ResultsDir + '/' + calc_id + '/' + fielname


    def set_vis_results_dir(self, name=__default_VisResultsDir):
        tdc_Filenames.__VisResultsDir=name

    def get_vis_results_dir(self):
        return tdc_Filenames.__VisResultsDir

    def get_full_vis_fielname(self,vis_id,fielname):
        return tdc_Filenames.__VisResultsDir + '/' + vis_id + '/' + fielname
 


# ------------------------------
# functions for interactive work
# ------------------------------

__all__ = [ 'tdc_set_results_dir',
            'tdc_get_results_dir',
            'tdc_get_fielname',            
            'tdc_set_vis_results_dir',
            'tdc_get_vis_results_dir',
            'tdc_get_vis_fielname' ]


def tdc_set_results_dir(name):
    "global function for setteng RESULTS directory"
    tdc_Filenames().set_results_dir(name)

def tdc_get_results_dir():
    "global function for getting RESULTS directory"
    return tdc_Filenames().get_results_dir()

def tdc_get_fielname(calc_id,fielname):
    return tdc_Filenames().get_full_fielname(calc_id,fielname)


def tdc_set_vis_results_dir(name):
    "global function for setteng RESULTS_VIS directory"
    tdc_Filenames().set_vis_results_dir(name)

def tdc_get_vis_results_dir():
    "global function for getting RESULTS_VIS directory"
    return tdc_Filenames().get_vis_results_dir()

def tdc_get_vis_fielname(vis_id,fielname):
    return tdc_Filenames().get_full_vis_fielname(vis_id,fielname)
