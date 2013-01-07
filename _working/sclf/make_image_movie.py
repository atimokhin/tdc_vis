#!/usr/bin/python
# import os
if __name__ == '__main__':
    import tdc_vis


from ATvis.Common_Data_Plot import *

from Auxiliary          import *
from Common_Data_Plot   import *
from x_PlottingFunctions            import plot_image_files_movie
from Movie              import Movie_Interface_Selector

# ============================================================
# Directory
# ============================================================
tdc_Filenames.set_results_dir('../RESULTS/')
## tdc_Filenames.set_results_dir('../RESULTS/FreeAgent/')


# ============================================================
# IDs 
# ============================================================
ID='XP_SCLF__jm0.5_L50_X0.5_nGJ2e5_nx5e3_dt2e-3__RhoGJConst__noMC__dP5e-2_inj15_s1'


ii=None
ii=10

fps = 14

keep_frame_files=False
# ==================



def do_movie(ID):
    # select interface
    interface = Movie_Interface_Selector()

    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # XP Movie
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    plot_image_files_movie(interface.movie_module,
                           ID,
                           ii=ii,
                           fps=fps,
                           keep_frame_files=keep_frame_files)
    # ~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":
    do_movie(ID)
