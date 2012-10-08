import os

from tdc_exception import tdc_Exception


class tdc_Filenames(object):
    """
    class with methods for retriving full filename and setting results directory
    There are twom types of results directories:
        RESULTS     -- computation data
        RESULTS_VIS -- results of visualization (movie/pictures)
    """

    __default_ResultsDir    ='../RESULTS/'
    __default_VisResultsDir ='../RESULTS_VIS/'

    __ResultsDir    = __default_ResultsDir
    __VisResultsDir = __default_VisResultsDir

    @staticmethod
    def set_results_dir(name=None):
        tdc_Filenames.__ResultsDir = \
          name if name is not None else tdc_Filenames.__default_ResultsDir
        # check whether the directory name is valid
        if not os.path.isdir(tdc_Filenames.__ResultsDir):
            print "Results Directory \"%s\" does not exist!\n" % tdc_Filenames.__ResultsDir
            raise tdc_Exception()
            

    @staticmethod
    def get_results_dir():
        return tdc_Filenames.__ResultsDir

    @staticmethod
    def get_full_filename(calc_id,filename):
        return os.path.join(tdc_Filenames.__ResultsDir, calc_id, filename)

    @staticmethod
    def set_vis_results_dir(name=None):
        tdc_Filenames.__VisResultsDir = \
          name if name is not None else tdc_Filenames.__default_VisResultsDir
        # check whether the directory name is valid
        if not os.path.isdir(tdc_Filenames.__VisResultsDir):
            print "VisResults Directory \"%s\" does not exist!\n" % tdc_Filenames.__VisResultsDir
            raise tdc_Exception()

    @staticmethod
    def get_vis_results_dir():
        return tdc_Filenames.__VisResultsDir

    @staticmethod
    def get_full_vis_filename(vis_id,filename):
        return os.path.join(tdc_Filenames.__VisResultsDir, vis_id, filename)
 

