import time
import gtk

class MovieEngine:

    def __init__(self, movie_frame, gui, movie_file_maker):

        # Movie Frame - where movie will be plotted
        self.F = movie_frame
        # GUI - all cotrol is done here
        self.GUI = gui
        # Movie file maker
        self.MFM = movie_file_maker
        
        # here we store axes background during animation
        self.background=None
        # counter
        self.i_frame=1
        self.i_frame_min=1
        self.i_frame_max=1
        # for profiling
        self.tstart = time.time()
        # flags
        self.redraw_flag=False


    def set_frame_number_limits(self, i_min=1,i_max=1):
        self.i_frame_min=i_min
        self.i_frame_max=i_max
        

    def animate(self):
        "Function that does the actual animation"
        # Frames
        F = self.F
        # AxesPanel
        AP = self.GUI.ap
        # ControlPanel
        CP = self.GUI.cp
        # DisplayPanel
        DP = self.GUI.dp

        # plot initial animation frame [if background is None] 
        if self.background is None:
            # plot
            F.plot(animated=True)
            # set current axes limits on axes panel 
            AP.set_xlim(F.get_xlims())
            AP.set_ylim(F.get_ylims())
            F.canvas.draw()
            self.background = F.canvas.copy_from_bbox(F.ax.bbox)

        # redraw axes if axes limits changed
        if AP.reset_axes_flag:
            self.reset_axes()
        if F.axes_lims_changed_flag:
            # clear axes and plot again
            F.replot()
            F.canvas.draw()
            self.background = F.canvas.copy_from_bbox(F.ax.bbox)
            F.axes_lims_changed_flag=False

        # set i_frame
        if CP.set_iframe_flag:
            self.i_frame = CP.get_frame_number()
            CP.set_iframe_flag = False
            

        # restore the clean slate background
        F.canvas.restore_region(self.background)
        # update the data
        F.animation_update(self.i_frame)
        # just redraw the axes rectangle
        F.canvas.blit(F.ax.bbox)

        # update diplay_panel
        DP.update_panel( F.get__i_id(),
                         F.get__i_timeshot(),
                         self.i_frame )
        CP.set_frame_number(self.i_frame)
        CP.set_iframe_flag = False

        # STOP/PLAY
        if not CP.play_flag and not CP.go_back_flag and not CP.go_forward_flag:
            F.set_animated(False)        
            while not CP.play_flag:
                time.sleep(0.025)
                while gtk.events_pending():
                    gtk.main_iteration(False)
                if CP.quit_flag or CP.set_iframe_flag:
                    break
                if CP.go_back_flag or CP.go_forward_flag or AP.reset_axes_flag:
                    F.set_animated(True)
                    break
            else:
                F.set_animated(True)

        # RECORD movie --------------------------
        if CP.record_flag:
            self.MFM.store_snapshot( F.canvas )
        # ---------------------------------------

        # we are at the LAST frame in animation sequence
        # stay there until go_back or quit 'signal' from GUI
        if self.i_frame==self.i_frame_max:
            F.set_animated(False)
            while not CP.go_back_flag:
                time.sleep(0.05)
                while gtk.events_pending():
                    gtk.main_iteration(False)
                if CP.quit_flag or CP.set_iframe_flag:
                    break
                if AP.reset_axes_flag:
                   F.set_animated(True)
                   break 
            else:
                F.set_animated(True)


        # update frame counter
        if CP.go_back_flag:
            self.i_frame -= 1
        elif not CP.set_iframe_flag and not AP.reset_axes_flag:
            self.i_frame += 1
            
        # we are at the FIRST frame in animation sequence
        # stay there until go_forward,play or quit 'signal' from GUI
        if self.i_frame < self.i_frame_min:
            F.set_animated(False)
            while not CP.go_forward_flag and not CP.play_flag:
                time.sleep(0.05)
                while gtk.events_pending():
                    gtk.main_iteration(False)
                if CP.quit_flag or CP.set_iframe_flag:
                    break
                if AP.reset_axes_flag:
                   F.set_animated(True)
                   break 
            else:
                F.set_animated(True)
                self.i_frame = self.i_frame_min

        # QUIT
        if CP.quit_flag:
            # print the timing info and quit
            print 'FPS:' , 100/(time.time()-self.tstart)
            self.GUI.destroy()
            gtk.main_quit()
            return False

        # wait for <- -> button release if in STOP mode
        if not CP.play_flag:
           time.sleep(0.15)
           while gtk.events_pending():
               gtk.main_iteration(False)           

        return True



    def reset_axes(self):
        self.F.ax.set_xlim([self.GUI.ap.x_min,self.GUI.ap.x_max])
        self.F.ax.set_ylim([self.GUI.ap.y_min,self.GUI.ap.y_max])
        self.GUI.ap.reset_axes_flag = False
        
