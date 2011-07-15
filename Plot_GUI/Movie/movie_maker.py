import gtk, gobject

import Plot_GUI.GUI.movie_gui
import Plot_GUI.Movie.movie_engine


class Movie_Maker:

    def __init__(self, movie_frames, movie_file_maker):

        self.F   = movie_frames
        self.MFM = movie_file_maker

        self.GUI = Plot_GUI.GUI.movie_gui.MovieGUI(self.F,self.MFM)
        self.ME  = Plot_GUI.Movie.movie_engine.MovieEngine(self.F, self.GUI, self.MFM)

        self.GUI.cp.set_frame_number_limits(self.F.i_frame_min, self.F.i_frame_max)
        self.ME.set_frame_number_limits(    self.F.i_frame_min, self.F.i_frame_max)

        # set window title
        self.GUI.set_title(self.F.plot_idlabel) 


    def animate(self,**kwargs):
        self.GUI.show_all()
        # set plot keywords
        self.ME.set_plot_keywords(**kwargs)
        # add ME.animate to idle queue
        gobject.idle_add(self.ME.animate)
        gtk.main()
