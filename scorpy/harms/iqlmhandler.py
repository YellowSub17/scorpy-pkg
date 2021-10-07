import numpy as np
import copy
import pyshtools as pysh
import matplotlib.pyplot as plt

from .harmsprops import IqlmHandlerProps
from ..plot.harmsplot import IqlmHandlerPlot


class IqlmHandler(IqlmHandlerProps, IqlmHandlerPlot):

    def __init__(self, nq, nl, qmax):
        self._nq = nq
        self._nl = nl
        self._qmax = qmax
        self.vals = np.zeros( (self.nq, 2, self.nl, self.nl))


    def copy(self):
        return copy.deepcopy(self)

    def mask_l(self,upperl=None, lowerl=None, lstep=None):
        if lowerl is None:
            lower=0
        if upperl is None:
            upper=self.nl
        if lstep is None:
            lstep=1

        mask = np.zeros( (self.nq, 2, self.nl, self.nl))
        mask[:, :, lowerl:upperl:lstep, :] = 1
        self.vals *= mask


    def _check_qlm(self, q, l, m):
        assert abs(m) <= l, 'Cannot set harmonic for M > L.'
        assert q < self.nq, 'q index out of range'
        assert l < self.nl, 'l index out of range'
        if m < 0:
            cs=1
        else:
            cs=0
        return cs

    def get_val(self, q, l, m):
        cs = self._check_qlm(q, l, m)
        return self.vals[q, cs, l, abs(m)]

    def set_val(self, q, l, m, val=1):
        cs = self._check_qlm(q, l, m)
        self.vals[q, cs, l, abs(m)] = val

    def add_val(self, q, l, m, val=1):
        cs = self._check_qlm(q, l, m)
        self.vals[q, cs, l, abs(m)] += val




    def fill_from_sphv(self, sphv):

        for iq, q_slice in enumerate(sphv.vol):
            pysh_grid = pysh.shclasses.DHRealGrid(q_slice)
            coeffs = pysh_grid.expand().coeffs

            self.vals[iq] = coeffs



    def calc_knlm(self, bl_u, inc_odds=True):
        '''
        transform from the spherical harmonics iqlm to k-space coefficients knlm
        '''
        if inc_odds:
            lskip=1
        else:
            lskip=2
        #initiailize new values
        new_vals = np.zeros( (self.nq, 2, self.nl, self.nl))

        for n in range(self.nq):
            for cs in range(0,2):
                for l in range(0, self.nl, lskip):
                    ulq = bl_u[:,n, l]
                    for m in range(l+1):

                        i_q = self.vals[:,cs, l, m]
                        x = np.dot(i_q, ulq)

                        new_vals[n, cs, l, m] = x
        self.vals = new_vals



    def calc_iqlmp(self, bl_u, inc_odds=True):
        '''
        transform from k-space coefficients knlm to spherical harmonics iqlm
        '''
        if inc_odds:
            lskip=1
        else:
            lskip=2
        #initiailize new values
        new_vals = np.zeros( (self.nq, 2, self.nl, self.nl))


        for q_ind in range(self.nq):
            for cs in range(0,2):

                for l in range(0, self.nl, lskip):
                    ulq = bl_u[q_ind,  :,l]
                    for m in range(l+1):
                        kp = self.vals[:,cs,l,m]
                        ku = np.dot(ulq, kp)

                        new_vals[q_ind, cs, l, m] = ku
        self.vals = new_vals


    def calc_knlmp(self, bl_l, ned_thresh=1e-6, inc_odds=True):
        '''
        calculate modified k-space coefficients knlm'
        '''
        if inc_odds:
            lskip=1
        else:
            lskip=2
        #initiailize new values
        new_vals = np.zeros( (self.nq, 2, self.nl, self.nl))

        for q_ind in range(self.nq):
            for l in range(0, self.nl, lskip):

                ned = bl_l[q_ind,l]
                #sqrt?

                km = np.abs(self.vals[q_ind, :, l,:])**2
                donk = np.sum(km)
                if donk==0:
                    ned = 1
                    donk = 1
                self.vals[q_ind, :, l, :] *= (ned/donk)




