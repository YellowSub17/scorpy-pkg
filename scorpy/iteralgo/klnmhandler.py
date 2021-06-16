import numpy as np
import copy
from .iteralgopropertymixins import KlnmHandlerProps


class KlnmHandler(KlnmHandlerProps):

    def __init__(self, nl, nq, qmax):
        self._nq = nq
        self._nl = nl
        self._qmax = qmax
        self.vals = []

        for l in range(nl):
            self.vals.append(np.zeros((nq, 2 * l + 1)))

    def copy(self):
        return copy.deepcopy(self)

    def fill_ilm(self, sphv):
        coeffs = sphv.get_all_q_coeffs()

        for l in range(self.nl):

            klnm_vals = np.zeros((self.nq, 2 * l + 1))
            for q_ind in range(self.nq):
                q_coeffs = coeffs[q_ind]

                for im, m in zip(range(0, 2 * l + 1), range(-l, l + 1)):
                    if m < 0:
                        klnm_vals[q_ind, im] = q_coeffs[1, l, abs(m)]
                    else:
                        klnm_vals[q_ind, im] = q_coeffs[0, l, abs(m)]

            self.vals[l] = np.round(klnm_vals, 15)

    def fill_klnm(self, bl_u):

        for l in range(0, self.nl, 2):
            new_vals = np.zeros(self.vals[l].shape)
            for im, m in zip(range(0, 2 * l + 1), range(-l, l + 1)):
                ilm = self.vals[l][:, im] * self.qpts**2

                for iq in range(self.nq):
                    x = np.dot(ilm, bl_u[:, iq, l])
                    new_vals[iq, m] = x
            self.vals[l] = new_vals

    def fill_kprime(self, bl_l):
        for l in range(0, self.nl, 2):
            new_vals = np.zeros(self.vals[l].shape)
            # for im, m in zip(range(0, 2*l+1), range(-l, l+1)):
            for iq in range(self.nq):

                ned = np.sqrt(np.abs(bl_l[iq, l]))
                km = np.abs(self.vals[l][iq, :])**2
                donk = np.sqrt(np.sum(km))

                if donk == 0:
                    donk = 1

                ned = 1
                donk = 1
                new_vals[iq, :] = (ned / donk) * self.vals[l][iq, :]

            self.vals[l] = new_vals

    def fill_ilmprime(self, bl_u):

        for l in range(0, self.nl, 2):
            ul = bl_u[..., l]
            for im, m in zip(range(0, 2 * l + 1), range(-l, l + 1)):
                kp = self.vals[l][:, im]
                ku = np.dot(ul, kp)
                self.vals[l][:, im] = ku
