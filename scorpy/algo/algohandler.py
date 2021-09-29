


from ..props.algoprops import AlgoHandlerProps
from ..plot.algoplot import AlgoHandlerPlot

from ..vols import SphericalVol
from ..harms import IqlmHandler

import numpy as np
import matplotlib.pyplot as plt



class AlgoHandler(AlgoHandlerProps, AlgoHandlerPlot):




    def __init__(self, blqq, sphv_mask, iqlm_init=None):

        self.blqq = blqq
        self.sphv_mask = sphv_mask


        assert self.blqq.qmax == self.sphv_mask.qmax
        self.qmax = self.blqq.qmax

        assert self.blqq.nq == self.sphv_mask.nq
        self.nq = self.blqq.nq

        assert self.blqq.nl == self.sphv_mask.nl
        self.nl = self.blqq.nl

        self.ntheta = self.sphv_mask.ntheta
        self.nphi = self.sphv_mask.nphi

        self.lams, self.us = self.blqq.get_eig()


        self.iqlm_base = IqlmHandler(self.nq, self.nl, self.qmax)
        self.sphv_base = SphericalVol(self.nq, self.ntheta, self.nphi, self.qmax)

        # self.iqlm_diff = self.iqlm_base.copy()
        # self.sphv_diff = self.sphv_base.copy()

        if iqlm_init is not None:
            self.iqlm_iter = iqlm_init
        else:
            self.iqlm_iter = self.iqlm_base.copy()
            self.iqlm_iter.vals = np.random.random(self.iqlm_iter.vals.shape)

        self.sphv_iter = self.sphv_base.copy()


    def k_constraint(self):
        knlm = self.iqlm_iter.copy()
        knlm.calc_knlm(self.us)

        iqlmk = knlm.copy()
        iqlmk.calc_iqlmp(self.us)

        # iqlm_diff = self.iqlm_iter.copy()
        # self.iqlm_diff.vals -= iqlmk.vals

        knlmp = knlm.copy()
        knlmp.calc_knlmp(self.lams)

        iqlmp = knlmp.copy()
        iqlmp.calc_iqlmp(self.us)

        # iqlmp.vals += self.iqlm_diff.vals

        self.iqlm_iter = iqlmp



    def b_constraint(self):

        self.sphv_iter.fill_from_iqlm(self.iqlm_iter)
        self.sphv_iter.plot_slice(0, 49)

        self.sphv_iter.vol *= self.sphv_mask.vol

        self.iqlm_iter.fill_from_sphv(self.sphv_iter)



    def ER(self):
        self.k_constraint()
        self.b_constraint()


