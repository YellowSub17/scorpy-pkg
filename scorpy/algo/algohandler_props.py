


from ..vols.sphv.sphericalvol import SphericalVol
from ..iqlm.iqlmhandler import IqlmHandler



class AlgoHandlerProps:


    @property
    def tag(self):
        return self._tag


    @property
    def path(self):
        return self._path


    @property
    def qmax(self):
        return self._qmax


    @property
    def qmin(self):
        return self._qmin



    @property
    def nq(self):
        return self._nq

    @property
    def npsi(self):
        return self._npsi


    @property
    def nl(self):
        return self._nl


    @property
    def lcrop(self):
        return self._lcrop


    @property
    def dxsupp(self):
        return self._dxsupp


    @property
    def pinv_rcond(self):
        return self._pinv_rcond


    @property
    def eig_rcond(self):
        return self._eig_rcond


    @property
    def lossy_iqlm(self):
        return self._lossy_iqlm


    @property
    def lossy_sphv(self):
        return self._lossy_sphv


    @property
    def rotk(self):
        return self._rotk


    @property
    def rottheta(self):
        return self._rottheta


    @property
    def sphv_base(self):
        return SphericalVol(self.nq, self.nl*2, self.nl*4, self.qmax, self.qmin)

    @property
    def iqlm_base(self):
        return IqlmHandler(self.nq, self.nl, self.qmax, self.qmin)










