from Common_Data_Plot import tdc_Data_vs_X_Plotter

class tdc_TP_Plotter(tdc_Data_vs_X_Plotter):
    """
    Members:
    --------
    TP
       Instance of tdc_TP_Data class
       if TP is empty - nothing will be done
    lines_p
       Dictionary containing list of lines for tracked particle
    lines_t
       Dictionary containing list of lines for tracked particle trails 
       Keys of dictionary correspond to kind of tracked particle,
       e.g. 'Pairs', 'Electrons' etc.
       Index in the list -- to individual tracked particles:
         lines_p['Pairs'][i]
         lines_t['Pairs'][i]
    trail_length
       [number] length of the plotted particle trail
    marker_style
    markersize
    plotstyle
    """

    __trail_length = 5
    
    __markers = ['o','v','^', '<', '>', '1', '2', '3', '4', 's', 'p', '*', 'h'] 
    __markersize = 6

    __plotstyle_color = { 'Electrons' : ['b'],
                          'Positrons' : ['r'],
                          'Pairs'     : ['k']   }

    __plotstyle_bw    = { 'Electrons' : ['k--'],
                          'Positrons' : ['k'],
                          'Pairs'     : ['k:']  }

    
    def __init__(self, tp, trail_dict=None):
        """
        Arguments:
        ----------
        tp
           tdc_TP_Data instance, if None <default>
           self.TP will be initialized by an empty dictionary
        trail_dict
           dictionary with trail plot properties
           dict( length=3, style='color', marker='symbols', markersize=10 )
           Entries:
           -------
           trail
              Length of the particle trail
              -1  -- plot the whole trail ut to the current time
              <-1 -- plot the whole trail for all time
           style
              'color' | 'bw'
           marker
              'symbols' | 'numbers'
           markersize
              size of the marker in pt.
              for both symbols and numbers
        """
        print "tdc_tp_plotter called"
        # --------------------------------------------------
        # setup plot properties
        # --------------------------------------------------
        if not trail_dict:
            trail_dict ={}
        self.trail_length = trail_dict.get('length', tdc_TP_Plotter.__trail_length)
        self.marker_style = trail_dict.get('marker', 'symbols')
        self.markersize   = trail_dict.get('markersize', self.__markersize)
        if ( trail_dict.get('style', 'color') == 'color' ):
            self.plotstyle  = self.__plotstyle_color
        else:
            self.plotstyle  = self.__plotstyle_bw
        # --------------------------------------------------
        # store Tracked_Particles_Data
        self.TP = tp
        # base class initialization
        # here we set all x-coordinate related stuff
        tdc_Data_vs_X_Plotter.__init__(self,self.TP)
        # labels -------------------------------------------
        self.plot_ylabel  = r'$p$'
        self.plot_idlabel = 'TP : ' + self.TP.calc_id
        # initialize lines dictionary ----------------------
        self.lines_p = dict.fromkeys( self.TP.keys() )
        self.lines_t = dict.fromkeys( self.TP.keys() )
        for key in self.TP:
            self.lines_p[key] = [None]*self.TP.get_number_of_tracked_particles()
            self.lines_t[key] = [None]*self.TP.get_number_of_tracked_particles()
        # --------------------------------------------------
        

    def plot(self,ax,tp_idxs=None,**kwargs):
        """
        Plot particles and trails into axes ax
        **kwargs goes to ax.plot(..)
        Options:
        --------
        tp_idxs
           sequence of TP indexies to be plotted
           <None> -- plot them all
        """
        #store for animation_update use
        self.tp_idxs=tp_idxs
        # plot trajectories
        for name,tps in self.TP.items():
            for i,tp in enumerate(self.__selected_tp(tps,tp_idxs)):
                x_p,p_p,x_t,p_t = self.__get_track_data( tp )
                # plot trail
                self.lines_t[name][i], = ax.plot(x_t, p_t,
                                                 *self.plotstyle[name],
                                                 **kwargs)
                # plot particle
                if self.marker_style == 'symbols':
                    self.lines_p[name][i], = ax.plot(x_p, p_p,
                                                     *self.plotstyle[name],
                                                     marker     = self.__markers[tp.marker],
                                                     markersize = self.markersize,
                                                     **kwargs)
                else:
                    self.lines_p[name][i] = ax.text(x_p, p_p,
                                                    '$%g$' % tp.marker,
                                                    size = self.markersize,
                                                    color= self.plotstyle[name][0][0],
                                                    **kwargs)
                    # workaround of bug(?):
                    # if x,p = None make text labels invisible
                    if not x_p or not p_p:
                        self.lines_p[name][i].set_visible(False)

                    
    def set_animated(self,val):
        "Set animated property of the field plot"
        for lps,lts in zip( self.lines_p.values(),
                            self.lines_t.values() ):
            for lp,lt in zip(lps,lts):
                lp.set_animated(val)
                lt.set_animated(val)

    def replot(self,ax):
        "Relot particles for animation at timestep# i_ts"
        for name,tps in self.TP.items():
            for i,tp in enumerate(self.__selected_tp(tps,self.tp_idxs)):
                x_p,p_p,x_t,p_t = self.__get_track_data( tp )
                # particles
                if self.marker_style == 'symbols':
                    self.lines_p[name][i].set_xdata(x_p)
                    self.lines_p[name][i].set_ydata(p_p)
                else:
                    # workaround of bug(?):
                    # if x,p = None make text labels invisible
                    if x_p and p_p:
                        self.lines_p[name][i].set_visible(True)
                        self.lines_p[name][i].set_position([x_p,p_p])
                    else:
                        self.lines_p[name][i].set_visible(False)
                # trail
                self.lines_t[name][i].set_xdata(x_t)
                self.lines_t[name][i].set_ydata(p_t)
        for lps,lts in zip( self.lines_p.values(),
                            self.lines_t.values() ):
            for lp,lt in zip(lps,lts):
                ax.draw_artist(lp)
                ax.draw_artist(lt)

    def update_plot(self,ax):
        self.replot(ax)
        
    def animation_update(self,ax,i_ts):
        "Read and plot particles for animation at timestep# i_ts"
        self.read(i_ts)
        self.update_plot(ax)


    def __get_track_data(self,tp):
        """
        Return lists with (x_p,p_p, x_t,p_t)
        of particle(x_p,p_p) and trail(x_t,p_t) XP coordinates
        __i_ts must be set before by read() call

        Trail showning algorithm is coded here
        """
        # --------------------------------------------------
        # if whole trail is requested - return it
        # --------------------------------------------------
        if self.trail_length<-1:
            x_t=tp.X[:]
            p_t=tp.P[:]
            return (x_t[-1],p_t[-1], x_t,p_t)
        # --------------------------------------------------
        # proceed with default algorithm
        # --------------------------------------------------
        # index of the current timeshot: ******
        # track end and particle position
        if not tp.timeshot or self.TP.i_ts < tp.timeshot[0]:
            # no particle at all - no trail, no particle 
            return (None,None, None,None)
        elif self.TP.i_ts > tp.timeshot[-1]:
            # particle left domain - no particle
            idx2=tp.timeshot[-1]
            x_p=None
            p_p=None
        else:
            # particle in the domain
            idx2=tp.timeshot.index(self.TP.i_ts)+1
            x_p=tp.X[idx2-1]
            p_p=tp.P[idx2-1]
        # index of track start ****************
        if len(tp.timeshot)>1:
            delta_i_ts = tp.timeshot[1]-tp.timeshot[0]
            i_ts__start = self.TP.i_ts - delta_i_ts*self.trail_length
            if i_ts__start > tp.timeshot[-1]:
                # trail left domain
                idx1 = tp.timeshot[-1]
            elif i_ts__start < tp.timeshot[0]:
                # trail is still shorter than desired
                idx1 = 0
            else:
                # trail is as desired
                idx1 = tp.timeshot.index(i_ts__start)
        else:
            # no trail
            idx1 = 0
        if self.trail_length==-1:
            idx1 = 0
        # trail XP coordinate arrays
        x_t=tp.X[idx1:idx2]
        p_t=tp.P[idx1:idx2]
        # is asked return label coordinates event for particles
        # which are not in the domain anymore
        if self.trail_length==-1:
            x_p=x_t[-1]
            p_p=p_t[-1]
        return (x_p,p_p,x_t,p_t) 

    def __selected_tp(self,tps,tp_idxs):
        """
        Return list of TP from tps  which ids are in selected list tp_idxs
        if tp_idxs is None return the whole tps
        """
        if not tp_idxs:
            return tps
        else:
            if not isinstance(tp_idxs, (tuple,list)):
                tp_idxs = (tp_idxs,)
            return [tp  for tp in tps if tp.marker in tp_idxs]
