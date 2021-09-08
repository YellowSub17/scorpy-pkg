import numpy as np
import copy
from .iteralgopropertymixins import IqlmHandlerProps
from .iteralgoplotmixins import IqlmHandlerPlot
import pyshtools as pysh
import matplotlib.pyplot as plt


class IqlmHandler(IqlmHandlerProps, IqlmHandlerPlot):

    def __init__(self, nq, nl, qmax):
        self._nq = nq
        self._nl = nl
        self._qmax = qmax
        vals = []
        for iq in range(self.nq):
            vals.append(np.zeros((2,self.nl,self.nl)))
        self.vals = np.stack(vals, 0)


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



    def calc_knlm(self, bl_u):
        #initiailize new values
        new_vals = []
        for iq in range(self.nq):
            new_vals.append(np.zeros((2,self.nl,self.nl)))
        new_vals = np.stack(new_vals,0)


        for n in range(self.nq):
            for cs in range(0,2):
                for l in range(self.nl):
                    for m in range(l):

                        i_q = self.vals[:,cs, l, m]*self.qpts**2
                        x = np.dot(i_q, bl_u[:, n, l])


                        new_vals[n, cs, l, m] = x
        self.vals = new_vals



    def calc_iqlm_prime(self, bl_u):
        #initiailize new values
        new_vals = []
        for iq in range(self.nq):
            new_vals.append(np.zeros((2,self.nl,self.nl)))
        new_vals = np.stack(new_vals,0)


        for n in range(self.nq):
            for cs in range(0,2):
                for l in range(self.nl):
                    ul = bl_u[:, n,l]
                    for m in range(l):
                        kp = self.vals[n,cs,l,m]
                        ku = np.dot(ul, kp)

                        new_vals[:, cs, l, m] = ku
        self.vals = new_vals





#     def plot_qharms(self, q_ind):
        # fig, axes = plt.subplots(1,2)


        # axes[0].imshow(self.vals[q_ind, 0, :,:], aspect='equal')
        # axes[0].set_title('Positive M')

        # axes[1].imshow(self.vals[q_ind, 1, :,:],aspect ='equal')
        # axes[1].set_title('Negative M')











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
