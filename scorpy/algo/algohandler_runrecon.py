




from ..vols.sphv.sphericalvol import SphericalVol
from ..vols.corr.correlationvol import CorrelationVol
from ..vols.blqq.blqqvol import BlqqVol
from ..iqlm.iqlmhandler import IqlmHandler




import numpy as np




class AlgoHandlerRunRecon:




    def load_inputs(self, blqq=None, sphv_supp=None):


        if blqq is None:
            self._blqq = BlqqVol(path=f'{self.path}/blqq_{self.tag}_data.dbin')
        else:
            self._blqq = blqq.copy()
            self._qmax = self.blqq.qmax
            self._nq = self.blqq.nq
            self._nl = self.blqq.nl

        if sphv_supp is None:
            self._sphv_supp = SphericalVol(path=f'{self.path}/sphv_{self.tag}_supp.dbin')
        else:
            self._sphv_supp = sphv_supp.copy()
            self._ntheta = self.sphv_supp.ntheta
            self._nphi = self.sphv_supp.nphi


        self._supp_loc = np.where(self.sphv_supp.vol == 1 )
        self._supp_notloc = np.where(self.sphv_supp.vol == 0 )


        self._lams, self._us = self.blqq.get_eig()
        #condition threshold
        if self.rcond is not None:
            eigs_thresh = np.max(self.lams, axis=0)*self.rcond
            for l_ind, eig_thresh in enumerate(eigs_thresh):
                loc = np.where(np.abs(self.lams[:,l_ind]) < eig_thresh)
                self.lams[loc, l_ind] = 0
                loc = np.where(self.lams[:,l_ind] ==0)
                self.us[:, loc, l_ind] = 0


        ##### base objects to copy from
        self._iqlm_base = IqlmHandler(self.nq, self.nl, self.qmax, self.inc_odds)
        self._sphv_base = SphericalVol(self.nq, self.ntheta, self.nphi, self.qmax)


        ##### initialize random spherical intensity
        if sphv_init is not None:
            self.sphv_iter = sphv_init.copy()
        else:
            self.sphv_iter = self.sphv_base.copy()
            self.sphv_iter.vol = np.random.random(self.sphv_iter.vol.shape)








#     def __init__(self, blqq, sphv_supp, sphv_init=None, lossy_sphv=True, lossy_iqlm=True,
                 # rcond=None, inc_odds=True):

        # ##### check inputs
        # assert blqq.qmax == sphv_supp.qmax
        # assert blqq.nq == sphv_supp.nq
        # assert 2*blqq.nl == sphv_supp.ntheta

        # ##### save inputs 
        # self._blqq = blqq.copy()
        # self._sphv_supp = sphv_supp.copy()
        # self._lossy_sphv = lossy_sphv
        # self._lossy_iqlm = lossy_iqlm
        # self._rcond = rcond
        # self._inc_odds = inc_odds


        # ##### find indices of support that are inside and outside S
        # self._supp_loc = np.where(self.sphv_supp.vol == 1 )
        # self._supp_notloc = np.where(self.sphv_supp.vol == 0 )

        # ##### check input properties are consistent and save them
        # self._qmax = self.blqq.qmax

        # self._nq = self.blqq.nq

        # self._nl = self.blqq.nl
        # self._ntheta = self.sphv_supp.ntheta
        # self._nphi = self.sphv_supp.nphi

        # self._lams, self._us = self.blqq.get_eig(inc_odds=self.inc_odds)
        # #condition threshold
        # if self.rcond is not None:
            # eigs_thresh = np.max(self.lams, axis=0)*self.rcond
            # for l_ind, eig_thresh in enumerate(eigs_thresh):
                # loc = np.where(np.abs(self.lams[:,l_ind]) < eig_thresh)
                # self.lams[loc, l_ind] = 0
                # loc = np.where(self.lams[:,l_ind] ==0)
                # self.us[:, loc, l_ind] = 0



        # ##### base objects to copy from
        # self._iqlm_base = IqlmHandler(self.nq, self.nl, self.qmax, self.inc_odds)
        # self._sphv_base = SphericalVol(self.nq, self.ntheta, self.nphi, self.qmax)


        # ##### initialize random spherical intensity
        # if sphv_init is not None:
            # self.sphv_iter = sphv_init.copy()
        # else:
            # self.sphv_iter = self.sphv_base.copy()
            # self.sphv_iter.vol = np.random.random(self.sphv_iter.vol.shape)



