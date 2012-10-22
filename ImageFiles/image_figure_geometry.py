import matplotlib

class Image_Single_FigureGeometry:
    """
    Class for single plot figures, sets:
        figure size,
        axes positions,
    """

    def __init__(self,seq_plotter):
        """
        Initialize figure and axes parameters for displaying a file with an image
        ------------
        params
        ------------
        seq_plotter
        """
        # figure size and axes position
        self.figsize_points = seq_plotter.data[0].imagesize_points
        self.axes_boxes     = [[0, 0, 1, 1]]



class Image_Double_FigureGeometry:
    """
    Size of figure and axes boxes for single pane movie frame
    """

    def __init__(self):
        self.figsize_points=[1100,500]
        self.axes_boxes=[[0.08,.1,.4,.85],[0.58,.1,.4,.85]]
