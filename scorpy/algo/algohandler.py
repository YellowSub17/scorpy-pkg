


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


        if iqlm_init is not None:
            self.iqlm_iter = iqlm_init
        else:
            self.iqlm_iter = self.iqlm_base.copy()
            self.iqlm_iter.vals = np.random.random(self.iqlm_iter.vals.shape)

        self.sphv_iter = self.sphv_base.copy()
        # self.sphv_iter.fill_from_iqlm(self.iqlm_iter)

        # self.sphv_diff = self.sphv_base.copy()
        # self.sphv_iter.fill_from_iqlm(iqlm_iter)


    def k_constraint(self):
        # Transform K[I_lm(q)]
        knlm = self.iqlm_iter.copy()
        knlm.calc_knlm(self.us)

        # Inverse Transform K-1[ K[ I_lm(q)] ]
        ikqlm = knlm.copy()
        ikqlm.calc_iqlmp(self.us)

        # Calculate lossy difference
        iqlm_diff = self.iqlm_iter.copy()
        iqlm_diff.vals -= iqlmk.vals

        # Calculate K'
        knlmp = knlm.copy()
        knlmp.calc_knlmp(self.lams)

        # Inverse K' to I'_lm(q)
        iqlmp = knlmp.copy()
        iqlmp.calc_iqlmp(self.us)

        # Add in lossy difference
        iaddqlmp = iqlmp.copy()
        iaddqlmp.vals += iqlm_diff.vals

        # Replace iqlm iteration
        self.iqlm_iter = iaddqlmp



    def b_constraint(self):

        self.sphv_iter.fill_from_iqlm(self.iqlm_iter)

        self.sphv_iter.vol += self.sphv_diff.vol
        self.sphv_iter.vol *= self.sphv_mask.vol

        self.iqlm_iter.fill_from_sphv(sphv_iter)

        sphv_lossy = self.sphv_base.copy()
        sphv_lossy.fill_from_iqlm(self.iqlm_iter)


        self.




    def ER(self):
        self.k_constraint()
        self.b_constraint()


