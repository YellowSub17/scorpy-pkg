


from ..props.algoprops import AlgoHandlerProps
from ..plot.algoplot import AlgoHandlerPlot

from ..vols import SphericalVol
from ..harms import IqlmHandler

import numpy as np
import matplotlib.pyplot as plt



class AlgoHandler(AlgoHandlerProps, AlgoHandlerPlot):




    def __init__(self, blqq, sphv_mask, sphv_start=True):

        ##### save inputs 
        self.blqq = blqq
        self.sphv_mask = sphv_mask


        ##### check input properties are consistent and save them
        assert self.blqq.qmax == self.sphv_mask.qmax
        self.qmax = self.blqq.qmax

        assert self.blqq.nq == self.sphv_mask.nq
        self.nq = self.blqq.nq

        assert self.blqq.nl == self.sphv_mask.nl
        self.nl = self.blqq.nl

        self.ntheta = self.sphv_mask.ntheta
        self.nphi = self.sphv_mask.nphi
        self.lams, self.us = self.blqq.get_eig()
        #condition threshold



        ##### base objects to copy from
        self.iqlm_base = IqlmHandler(self.nq, self.nl, self.qmax)
        self.sphv_base = SphericalVol(self.nq, self.ntheta, self.nphi, self.qmax)


        ##### initialize random spherical intensity
        self.sphv_iter = self.sphv_base.copy()
        self.sphv_iter.vol = np.random.random(self.sphv_iter.vol.shape)

        if not sphv_start:
            ##### calculate initial harmonic values and get s_diff
            self.iqlm_iter = self.iqlm_base.copy()
            self.iqlm_iter.fill_from_sphv(self.sphv_iter)

            self.sphv_lm = self.sphv_base.copy()
            self.sphv_lm.fill_from_iqlm(self.iqlm_iter)

            self.sphv_diff = self.sphv_iter.copy()
            self.sphv_diff.vol -= self.sphv_lm.vol


    def ER_sphv(self):
        _ = self.k_constraint_sphv()
        _ = self.b_constraint_sphv()

    def ER_iqlm(self):
        _ = self.k_constraint_iqlm()
        _ = self.b_constraint_iqlm()









    def k_constraint_sphv(self):
        ##### save input
        sphv_i = self.sphv_iter.copy()

        ##### Convert spherical coordinates to harmonic coeff.
        self.iqlm_iter = self.iqlm_base.copy()
        self.iqlm_iter.fill_from_sphv(self.sphv_iter)

        ##### get low pass filtered spherical coordinates
        self.sphv_lm = self.sphv_base.copy()
        self.sphv_lm.fill_from_iqlm(self.iqlm_iter)

        ##### difference lost between low pass filtered and original coords.
        self.sphv_diff = self.sphv_base.copy()
        self.sphv_diff.vol = self.sphv_iter.vol - self.sphv_lm.vol

        ##### Transform K[I_(q, l, m)]
        self.knlm = self.iqlm_iter.copy()
        self.knlm.calc_knlm(self.us)

        ##### Inverse Transform K-1[ K[ I(q, l, m)] ]
        self.ikqlm = self.knlm.copy()
        self.ikqlm.calc_iqlmp(self.us)

        ##### difference lost over K transformation
        self.iqlm_diff = self.iqlm_iter.copy()
        self.iqlm_diff.vals -= self.ikqlm.vals

        ##### Calculate K' after modifered by lamda
        self.knlmp = self.knlm.copy()
        self.knlmp.calc_knlmp(self.lams)

        ##### Inverse K' to I(q, l, m)
        self.iqlmp = self.knlmp.copy()
        self.iqlmp.calc_iqlmp(self.us)

        ##### Add in difference lost over K trasnformation
        self.iqlm_add = self.iqlmp.copy()
        # self.iqlmp_add.vals += self.iqlm_diff.vals

        ##### calculate the spherical coordinates deom new harmonics
        self.sphvp = self.sphv_base.copy()
        self.sphvp.fill_from_iqlm(self.iqlm_add)


        ##### Add in difference lost over low pass filter 
        self.sphv_add = self.sphvp.copy()
        # self.sphv_add.vol += self.sphv_diff.vol

        ##### replace iterating volume
        self.sphv_iter = self.sphv_add.copy()

        ##### copy final output
        sphv_f = self.sphv_iter.copy()

        ##### retrun input and output
        return sphv_i, sphv_f

    def b_constraint_sphv(self):
        ##### save input
        sphv_i = self.sphv_iter.copy()

        ##### only keep intenisty values at bragg positions defined by mask
        self.sphv_b = self.sphv_base.copy()
        self.sphv_b.vol = self.sphv_iter.vol * self.sphv_mask.vol

        ##### replace iterating sphv
        self.sphv_iter = self.sphv_b.copy()

        ##### copy final output
        sphv_f = self.sphv_iter.copy()

        ##### return input and output
        return sphv_i, sphv_f



    def k_constraint_iqlm(self, sphv=None):
        ##### save input
        iqlm_i = self.iqlm_iter.copy()

        ##### Transform K[I_(q, l, m)]
        self.knlm = self.iqlm_iter.copy()
        self.knlm.calc_knlm(self.us)

        ##### Inverse Transform K-1[ K[ I(q, l, m)] ]
        self.ikqlm = self.knlm.copy()
        self.ikqlm.calc_iqlmp(self.us)

        ##### Calculate lossy difference
        self.iqlm_diff = self.iqlm_iter.copy()
        self.iqlm_diff.vals -= self.ikqlm.vals

        ##### Calculate K'
        self.knlmp = self.knlm.copy()
        self.knlmp.calc_knlmp(self.lams)

        ##### Inverse K' to I'_lm(q)
        self.iqlmp = self.knlmp.copy()
        self.iqlmp.calc_iqlmp(self.us)

        ##### Add in lossy difference
        self.iqlm_add = self.iqlmp.copy()
        # self.iqlmp_add.vals += self.iqlm_diff.vals

        ##### Replace iterating iqlm 
        self.iqlm_iter = self.iqlm_add.copy()

        ##### copy final output
        iqlm_f = self.iqlm_iter.copy()

        ##### return input and output
        return iqlm_i, iqlm_f

    def b_constraint_iqlm(self, lossy_flag=True):
        ##### save input
        iqlm_i = self.iqlm_iter.copy()

        ##### harmonic recomp to spherical coordinates
        self.sphv_iter.fill_from_iqlm(self.iqlm_iter)

        ##### add in lost difference from spherical harmonic recomp
        self.sphv_add = self.sphv_iter.copy()
        # self.sphv_add.vol += self.sphv_diff.vol

        ##### only keep intenisty values at bragg positions defined by mask
        self.sphv_b = self.sphv_base.copy()
        self.sphv_b.vol = self.sphv_iter.vol * self.sphv_mask.vol

        ##### spherical harmonic decomp after bragg masking
        self.iqlm_iter.fill_from_sphv(self.sphv_b)

        ##### recalculate the low pass filtered spherical coordinates
        self.sphv_lm = self.sphv_base.copy()
        self.sphv_lm.fill_from_iqlm(self.iqlm_iter)

        ##### get the difference between the bragg masked and low pass filtered coordinates
        self.sphv_diff = self.sphv_iter.copy()
        self.sphv_diff.vol -= self.sphv_lm.vol

        ##### copy final output
        iqlm_f = self.iqlm_iter.copy()

        ##### return input and output
        return iqlm_i, iqlm_f




