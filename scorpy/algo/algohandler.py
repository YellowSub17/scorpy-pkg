


from .algopropertymixins import AlgoHandlerProps
from .algoplotmixins import AlgoHandlerPlot

from ..vols import SphericalVol



class AlgoHandler:




    def __init__(self):
        self.qmax = 1
        self.nq = 100
        self.ntheta = 180
        self.nphi = 360
        self.nl = 90


        self.sphv_add = SphericalVol(self.nq, self.ntheta, self.nphi, self.qmax)


    def k_constraint(self):
        pass

    def b_constraint(self):
        pass





