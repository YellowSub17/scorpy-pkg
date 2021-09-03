import numpy as np
import copy
from .iteralgopropertymixins import IqlmHandlerProps
import pyshtools as pysh
import matplotlib.pyplot as plt


class IqlmHandler(IqlmHandlerProps):

    def __init__(self, nq, nl, qmax):
        self._nq = nq
        self._nl = nl
        self._qmax = qmax
        self.vals = []
        for iq in range(self.nq):
            self.vals.append(np.zeros((2,nl,nl)))


    def copy(self):
        return copy.deepcopy(self)

    def mask_ilm(self,lowerl=None, upperl=None, lstep=None):

        if lowerl is None:
            lower=0
        if upperl is None:
            upper=self.nl
        if lstep is None:
            lstep=1

        mask = np.zeros( (2, self.nl, self.nl))
        mask[:, lowerl:upperl:lstep, :] = 1

        for q_ind in range(self.nq):
            self.vals[q_ind] *= mask

    def fill_from_sphv(self, sphv):

        for iq, q_slice in enumerate(sphv.vol):
            pysh_grid = pysh.shclasses.DHRealGrid(q_slice)
            coeffs = pysh_grid.expand().coeffs

            self.vals[iq] = coeffs




'


    def fill_klnm(self, bl_u):






    def fill_klnm(self, bl_u):

        for l in range(0, self.nl, 2):
            new_vals = np.zeros(self.vals[l].shape)
            for im, m in zip(range(0, 2 * l + 1), range(-l, l + 1)):
                ilm = self.vals[l][:, im] * self.qpts**2

                for iq in range(self.nq):
                    x = np.dot(ilm, bl_u[:, iq, l])
                    new_vals[iq, m] = x
            self.vals[l] = new_vals

    # def fill_kprime(self, bl_l):
        # for l in range(0, self.nl, 2):
            # new_vals = np.zeros(self.vals[l].shape)
            # # for im, m in zip(range(0, 2*l+1), range(-l, l+1)):
            # for iq in range(self.nq):

                # ned = np.sqrt(np.abs(bl_l[iq, l]))
                # km = np.abs(self.vals[l][iq, :])**2
                # donk = np.sqrt(np.sum(km))

                # if donk == 0:
                    # donk = 1

                # ned = 1
                # donk = 1
                # new_vals[iq, :] = (ned / donk) * self.vals[l][iq, :]

            # self.vals[l] = new_vals

    # def fill_ilmprime(self, bl_u):

        # for l in range(0, self.nl, 2):
            # ul = bl_u[..., l]
            # for im, m in zip(range(0, 2 * l + 1), range(-l, l + 1)):
                # kp = self.vals[l][:, im]
                # ku = np.dot(ul, kp)
                # self.vals[l][:, im] = ku
