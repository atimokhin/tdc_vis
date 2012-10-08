
class RS:
    """
    class with Ruderman-Sutherland cascace properties
    """

    def __init__(self, P=1, rho_6=1, B_12=1):
        self.P     = P
        self.rho_6 = rho_6
        self.B_12  = B_12

    def h(self, P=None, rho_6=None, B_12=None):
        "Height of the vacuum gap in [cm]"
        if not P:     P     = self.P
        if not rho_6: rho_6 = self.rho_6
        if not B_12:  B_12  = self.B_12
        return 5e3 * pow(rho_6,2./7) * pow(P,3./7) / pow(B_12,4./7)

    def tau_1(self, P=None, rho_6=None, B_12=None):
        "Vacuum gap timescale [sec]"
        return self.h(P, rho_6, B_12)/3e10
