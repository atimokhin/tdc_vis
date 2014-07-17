import gtk


class DisplayPanel(gtk.Frame):
    """
    This class represents a panel showing
    - id
    - current timeshot number in the id
    - frame number counted from the beginning of the animation

    internaly it is constructed as
    Frame: VBox: Table: 3+3 Labels
    """

    def __init__(self, i_id=1, i_timeshot=1, i_frame=1, **kwargs):
        "initialize everything"
        # constructor of the base class
        gtk.Frame.__init__(self,**kwargs)
        # size <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!
        self.set_size_request(145,60)
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!
        # initial panel info
        self.i_id       = i_id
        self.i_timeshot = i_timeshot
        self.i_frame    = i_frame
        # setup table
        self.tbl=gtk.Table(3,2,homogeneous=False)
        self.tbl.set_col_spacings(10)
        # ID# --------------
        label=gtk.Label('id :')
        label.set_alignment(1,.5)
        self.tbl.attach(label,0,1,0,1)
        # label_id
        self.label_id=gtk.Label(self.i_id)
        # reques size to make nice table output
        self.label_id.set_size_request(45,15)
        self.label_id.set_alignment(0,.5)
        self.tbl.attach(self.label_id,1,2,0,1)
        # ------------------
        # Timeshot# --------
        label=gtk.Label('timeshot :')
        label.set_alignment(1,.5)
        self.tbl.attach(label,0,1,1,2)
        # timeshot_id
        self.label_timeshot=gtk.Label(self.i_timeshot)
        self.label_timeshot.set_alignment(0,.5)
        self.tbl.attach(self.label_timeshot,1,2,1,2)
        # ------------------
        # Frame# -----------
        label=gtk.Label('frame :')
        label.set_alignment(1,.5)
        self.tbl.attach(label,0,1,2,3)
        # frame_id
        self.label_frame=gtk.Label(self.i_frame)
        self.label_frame.set_alignment(0,.5)
        self.tbl.attach(self.label_frame,1,2,2,3)
        # ------------------
        # add Table into the Frame
        self.add(self.tbl)


    def update_panel(self, i_id, i_timeshot, i_frame):
        """
        update information on display panel:
        call it each time the frame is updated
        """
        self.i_id       = i_id
        self.i_timeshot = i_timeshot
        self.i_frame    = i_frame
        self.label_id.set_text( str(self.i_id) )
        self.label_timeshot.set_text( str(self.i_timeshot) )
        self.label_frame.set_text( str(self.i_frame) )
        
    def get_panel_info():
        "return tuple (i_id, i_timeshot, i_frame)"
        return (self.i_id, self.i_timeshot, self.i_frame)
