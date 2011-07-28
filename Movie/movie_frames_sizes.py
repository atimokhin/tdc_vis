
class Single_Panel_Movie_Frames_Sizes:
    """
    Size of figure and axes boxes for single pane movie frame
    """
    ylabel_left_x = 0.01
    xlabel_bottom_y = 0.05

    def __init__(self):
        self.figsize_points=[705,480]
        self.axes_boxes=[[0.1135,.125,.8582,.8125]]
        # define sizes
        self.dx_ax = self.axes_boxes[0][2]
        self.dy_ax = self.axes_boxes[0][3]
        self.left_margin   = self.axes_boxes[0][0]
        self.bottom_margin = self.axes_boxes[0][1]

    def xlabel_pos(self,i):
        "x label position in figure coordinates"
        return ( self.left_margin+.5*self.dx_ax,
                 self.xlabel_bottom_y)

    def ylabel_pos(self,i):
        "y label position in figure coordinates"
        return ( self.ylabel_left_x,
                 self.bottom_margin+.5*self.dy_ax)

class Double_Panel_Movie_Frames_Sizes:
    """
    Size of figure and axes boxes for single pane movie frame
    """

    def __init__(self):
        self.figsize_points=[1100,500]
        self.axes_boxes=[[0.08,.1,.4,.85],[0.58,.1,.4,.85]]

