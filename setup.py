import pickle

from Common    import *
from Particles import *
from Fields    import *
from Fluxes    import *

from PhysicalProperties    import *


RESULTS_DIR='../RESULTS/FreeAgent/'
##RESULTS_DIR='../RESULTS/'
tdc_set_results_dir(RESULTS_DIR)
print '\nRESULTS_DIR is set to "%s"! \n' % RESULTS_DIR
