
import numpy as np
import matplotlib.pyplot as plt
import copy


from .algoprops import AlgoHandlerProps
from .operators import AlgoHandlerOperators
from .schemes import AlgoHandlerSchemes
from ..plot.algoplot import AlgoHandlerPlot

from ..vols import SphericalVol
from ..harms import IqlmHandler





class AlgoHandler(AlgoHandlerProps, AlgoHandlerPlot,
                  AlgoHandlerOperators, AlgoHandlerSchemes):





    def __init__(self, blqq, sphv_supp, lossy_sphv=True, lossy_iqlm=True,
                 rcond=None, inc_odds=True):


        ##### save inputs 
        self.blqq = blqq.copy()
        self.sphv_supp = sphv_supp.copy()
        self.lossy_sphv = lossy_sphv
        self.lossy_iqlm = lossy_iqlm
        self.rcond = rcond
        self.inc_odds = inc_odds


        ##### check input properties are consistent and save them
        assert self.blqq.qmax == self.sphv_supp.qmax
        self.qmax = self.blqq.qmax

        assert self.blqq.nq == self.sphv_supp.nq
        self.nq = self.blqq.nq

        assert self.blqq.nl == self.sphv_supp.nl
        self.nl = self.blqq.nl


        self.ntheta = self.sphv_supp.ntheta
        self.nphi = self.sphv_supp.nphi
        self.lams, self.us = self.blqq.get_eig(inc_odds=self.inc_odds)
        #condition threshold

        if self.rcond is not None:
            eigs_thresh = np.max(self.lams, axis=0)*self.rcond
            for l_ind, eig_thresh in enumerate(eigs_thresh):
                loc = np.where(np.abs(self.lams[:,l_ind]) < eig_thresh)
                self.lams[loc, l_ind] = 0
                loc = np.where(self.lams[:,l_ind] ==0)
                self.us[:, loc, l_ind] = 0


        print('RM ME: LAMS=0')
        self.lams *= 0



        ##### base objects to copy from
        self.iqlm_base = IqlmHandler(self.nq, self.nl, self.qmax, self.inc_odds)
        self.sphv_base = SphericalVol(self.nq, self.ntheta, self.nphi, self.qmax)


        ##### initialize random spherical intensity
        self.sphv_iter = self.sphv_base.copy()
        self.sphv_iter.vol = np.random.random(self.sphv_iter.vol.shape)

        ##### find indices of support that are inside and outside S
        self.supp_loc = np.where(self.sphv_supp == 1 )
        self.supp_notloc = np.where(self.sphv_supp == 0 )





    def copy(self):
        a = copy.deepcopy(self)
        return a





