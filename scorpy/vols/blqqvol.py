

from .vol import Vol
import numpy as np
from scipy import special
from .volspropertymixins import BlqqVolProps
import matplotlib.pyplot as plt


class BlqqVol(Vol, BlqqVolProps):
    '''
    Representation of the B_l(q1,q2) volume, an invertible correlation matrix.

    Arguments:
        nq (int): number of scattering magnitude bins.
        nl (int): number of spherical harmonics (inc. 0th harmonic, so 1+lmax).
        qmax (float): correlation magnitude limit [1/A].
        path (str): path to dbin (and log) if being created from memory.
    '''

    def __init__(self, nq=100, nl=37, qmax=1, path=None, comp=False):
        Vol.__init__(self, nx=nq, ny=nq, nz=nl,
                     xmax=qmax, ymax=qmax, zmax=nl - 1,
                     xmin=0, ymin=0, zmin=0,
                     xwrap=False, ywrap=False, zwrap=False,
                     comp=False, path=path)

        self.plot_q1q2 = self.plot_xy

    def _save_extra(self, f):
        f.write('[blqq]\n')
        f.write(f'qmax = {self.qmax}\n')
        f.write(f'nq = {self.nq}\n')
        f.write(f'nl = {self.nl}\n')
        f.write(f'lmax = {self.lmax}\n')
        f.write(f'dq = {self.dq}\n')

    def fill_from_corr(self, corr, inc_odds=False):
        assert corr.nq == self.nq, 'CorrelationVol and BlqqVol have different nq'
        assert corr.qmax == self.qmax, 'CorrelationVol and BlqqVol have different qmax'

        if inc_odds:
            lskip = 1
        else:
            lskip = 2


        # #TODO compensate for ewald sphere
        # q_range = np.linspace(0,self.qmax, self.nq)

        # create args of legendre eval
        # args = np.cos(np.linspace(0, np.pi, corr.npsi))
        # args = np.cos(np.radians(corr.psipts))
        args = corr.psipts

        # initialze fmat matrix
        fmat = np.zeros((corr.npsi, self.nl))

        # for every even spherical harmonic
        for l in range(0, self.nl, lskip):
            leg_vals = special.eval_legendre(l, args)
            # leg_vals = 4*np.pi * special.eval_legendre(l, args)
            fmat[:, l] = leg_vals

        fmat_inv = np.linalg.pinv(fmat, rcond=1e-3)

        # TODO check svd
        # plt.figure()
        # plt.imshow(np.matmul(fmat_inv, fmat))
        # plt.title('fmat inv * fmat')
        # u, s, vh = np.linalg.svd(fmat)
        # print('min s:', s.min())
        # print('max s:', s.max())
        # plt.figure()
        # plt.plot(s)

        for iq1 in range(self.nq):
            for iq2 in range(iq1, self.nq):
                dot = np.dot(fmat_inv, corr.vol[iq1, iq2, :])
                self.vol[iq1, iq2, :] = dot
                if iq2 > iq1:
                    self.vol[iq2, iq1, :] = dot

    def fill_from_sphv(self, sphv):
        assert sphv.nq == self.nq, 'SphericalVol and BlqqVol have different nq'
        assert sphv.qmax == self.qmax, 'SphericalVol and BlqqVol have different nq'

        all_q_coeffs = list(map(sphv.get_q_coeffs, range(self.nq)))

        for i, q1_coeffs in enumerate(all_q_coeffs):

            for j, q2_coeffs in enumerate(all_q_coeffs[i:]):

                multi = np.conj(q1_coeffs) * q2_coeffs

                self.vol[i, j + i, :] = multi.sum(axis=0).sum(axis=1)[:self.nl]
                if j > 0:
                    self.vol[j + i, i, :] = multi.sum(axis=0).sum(axis=1)[:self.nl]

    # def fill_from_sph(self, sph):

        # if self.comp:
            # bl = np.zeros((self.nq, self.nq), dtype=np.complex128)
        # else:
            # bl = np.zeros((self.nq, self.nq))

        # for l in range(0, self.nl, 2):
            # for iq1 in range(self.nq):
                # for iq2 in range(iq1, self.nq):
                    # bl[iq1,iq2] = np.sum(np.conj(sph.vals_lnm[l][iq1])*sph.vals_lnm[l][iq2])

                    # if iq1 !=iq2:
                    # bl[iq2,iq1] = np.sum(np.conj(sph.vals_lnm[l][iq2])*sph.vals_lnm[l][iq1])

            # self.vol[...,l] = bl
