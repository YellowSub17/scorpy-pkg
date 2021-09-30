


from ..props.algoprops import AlgoHandlerProps
from ..plot.algoplot import AlgoHandlerPlot

from ..vols import SphericalVol
from ..harms import IqlmHandler

import numpy as np
import matplotlib.pyplot as plt



class AlgoHandler(AlgoHandlerProps, AlgoHandlerPlot):




    def __init__(self, blqq, sphv_mask):

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

        self.sphv_iter = self.sphv_base.copy()
        self.sphv_iter.vol = np.random.random(self.sphv_iter.vol.shape)

        self.iqlm_iter = self.iqlm_base.copy()
        self.iqlm_iter.fill_from_sphv(self.sphv_iter)

        self.sphv_lm = self.sphv_base.copy()
        self.sphv_lm.fill_from_iqlm(self.iqlm_iter)

        self.sphv_diff = self.sphv_iter.copy()
        self.sphv_diff.vol -= self.sphv_lm.vol


        self.iqlm_iter.vals = np.random.random(self.iqlm_iter.vals.shape)
        self.sphv_diff.vol *=0


    def k_constraint(self):
        # Transform K[I_lm(q)]
        self.knlm = self.iqlm_iter.copy()
        self.knlm.calc_knlm(self.us)

        # Inverse Transform K-1[ K[ I_lm(q)] ]
        self.ikqlm = self.knlm.copy()
        self.ikqlm.calc_iqlmp(self.us)

#         # Calculate lossy difference
        # self.iqlm_diff = self.iqlm_iter.copy()
        # self.iqlm_diff.vals -= self.ikqlm.vals

        # Calculate K'
        self.knlmp = self.knlm.copy()
        self.knlmp.calc_knlmp(self.lams)

        # Inverse K' to I'_lm(q)
        self.iqlmp = self.knlmp.copy()
        self.iqlmp.calc_iqlmp(self.us)

        # Add in lossy difference
        self.iaddqlmp = self.iqlmp.copy()
#         self.iaddqlmp.vals += self.iqlm_diff.vals

        # Replace iqlm iteration
        self.iqlm_iter = self.iaddqlmp.copy()



    def b_constraint(self):

        self.sphv_iter.fill_from_iqlm(self.iqlm_iter)


        self.sphv_add = self.sphv_iter.copy()
#         self.sphv_add.vol += self.sphv_diff.vol



        self.sphv_bra = self.sphv_add.copy()
        self.sphv_bra.vol *= self.sphv_mask.vol

        self.iqlm_iter.fill_from_sphv(self.sphv_bra)

        self.sphv_lm = self.sphv_base.copy()
        self.sphv_lm.fill_from_iqlm(self.iqlm_iter)

        # self.sphv_diff = self.sphv_iter.copy()
        # self.sphv_diff.vol -= self.sphv_lm.vol





    def ER(self):
        self.k_constraint()
        self.b_constraint()


