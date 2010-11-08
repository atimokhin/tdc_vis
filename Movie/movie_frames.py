class MovieFrames:
    """
    Base class for movie frames
    contains information about number of frames
    and fetches i_timeshot and i_id
    """

    def __init__(self, seq_plotter):
        # sequence plotter
        self.seq_plotter = seq_plotter
        # frame number limits
        self.i_frame_min = 1
        self.i_frame_max = seq_plotter.get_sequence_length()


    def get__i_timeshot(self):
        return self.seq_plotter.get__i_timeshot()

    def get__i_id(self):
        return self.seq_plotter.get__i_id()
