
import numpy as np
import matplotlib.pyplot as plt
import copy


from .algoprops import AlgoHandlerProps
from .constraints import AlgoHandlerConstraints
from ..plot.algoplot import AlgoHandlerPlot

from ..vols import SphericalVol
from ..harms import IqlmHandler





class AlgoHandler(AlgoHandlerProps, AlgoHandlerPlot, AlgoHandlerConstraints):



    def __init__(self, blqq, sphv_mask, iter_obj='sphv',
                 lossy_sphv=True, lossy_iqlm=True, rcond=None, inc_odds=True):

        ##### save inputs 
        self.blqq = blqq
        self.sphv_mask = sphv_mask
        self.iter_obj = iter_obj
        self.lossy_sphv = lossy_sphv
        self.lossy_iqlm = lossy_iqlm
        self.rcond = rcond
        self.inc_odds = inc_odds


        ##### check input properties are consistent and save them
        assert self.blqq.qmax == self.sphv_mask.qmax
        self.qmax = self.blqq.qmax

        assert self.blqq.nq == self.sphv_mask.nq
        self.nq = self.blqq.nq

        assert self.blqq.nl == self.sphv_mask.nl
        self.nl = self.blqq.nl

        assert self.iter_obj in ['sphv', 'iqlm']
        # assert self.iter_obj in ['sphv']

        self.ntheta = self.sphv_mask.ntheta
        self.nphi = self.sphv_mask.nphi
        self.lams, self.us = self.blqq.get_eig(inc_odds=self.inc_odds)
        #condition threshold

        if self.rcond is not None:
            eigs_thresh = np.max(self.lams, axis=0)*self.rcond
            for l_ind, eig_thresh in enumerate(eigs_thresh):
                loc = np.where(np.abs(self.lams[:,l_ind]) < eig_thresh)
                self.lams[loc, l_ind] = 0
                loc = np.where(self.lams[:,l_ind] ==0)
                self.us[:, loc, l_ind] = 0



        ##### base objects to copy from
        self.iqlm_base = IqlmHandler(self.nq, self.nl, self.qmax, self.inc_odds)
        self.sphv_base = SphericalVol(self.nq, self.ntheta, self.nphi, self.qmax)


        ##### initialize random spherical intensity
        self.sphv_iter = self.sphv_base.copy()
        self.sphv_iter.vol = np.random.random(self.sphv_iter.vol.shape)



    def copy(self):
        a = copy.deepcopy(self)
        return a




    def ER(self):
        if self.iter_obj=='iqlm':
            _ = self.k_constraint_iqlm()
            _ = self.k_constraint_iqlm()
            _ = self.b_constraint_iqlm()

        elif self.iter_obj=='sphv':
            _ = self.k_constraint_sphv()
            _ = self.k_constraint_sphv()
            _ = self.b_constraint_sphv()





    def HIO(self, beta=0.5):

        pass




