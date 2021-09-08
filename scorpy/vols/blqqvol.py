

from .vol import Vol
import numpy as np
from scipy import special
from .volspropertymixins import BlqqVolProps
import matplotlib.pyplot as plt


class BlqqVol(Vol, BlqqVolProps):
    """scorpy.Blqq:
    A representaion of a Harmonic Order Correlation function.
    Attributes:
        nq, nl : int
        qmax : float
        dq : float
        qpts : numpy.array
    Methods:
        BlqqVol.fill_from_corr()
        BlqqVol.fill_from_sphv()
        BlqqVol.plot_q1q2()
    """

    def __init__(self, nq=100, nl=37, qmax=1, path=None, comp=False):
        Vol.__init__(self, nx=nq, ny=nq, nz=nl,
                     xmin=0, ymin=0, zmin=0,
                     xmax=qmax, ymax=qmax, zmax=nl - 1,
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





    def fill_from_corr(self, corr, inc_odds=True, rcond=None):
        '''
        scorpy.BlqqVol.fill_from_corr():
            Fill the Blqq from a CorrelationVol object
        Arguments:
            corr : scorpy.CorrelationVol
                The CorrelationVol object to to fill from.
            inc_odds : bool
                Flag for including odd order harmonic functions in calculation.
            rcond : float
                Condition number scale for SVD calculation.
        '''

        assert corr.nq == self.nq, 'CorrelationVol and BlqqVol have different nq'
        assert corr.qmax == self.qmax, 'CorrelationVol and BlqqVol have different qmax'

        if inc_odds:
            lskip = 1
        else:
            lskip = 2

        args = corr.psipts

        # initialze fmat matrix
        fmat = np.zeros((corr.npsi, self.nl))

        # for every even spherical harmonic
        for l in range(0, self.nl, lskip):
            leg_vals = special.eval_legendre(l, args)
            # leg_vals = 4*np.pi * special.eval_legendre(l, args)
            fmat[:, l] = leg_vals

        #if rcond is given, use it, else, use default
        if rcond is not None:
            fmat_inv = np.linalg.pinv(fmat, rcond=rcond)
        else:
            fmat_inv = np.linalg.pinv(fmat)

        # fmat_inv = np.linalg.pinv(fmat)

        # calc with svd
        # so we can pull out uvs
        # reuse uvs for iteralgo
        # in iteralgo, tweak algo type/inputs + rcond

        for iq1 in range(self.nq):
            for iq2 in range(iq1, self.nq):
                dot = np.dot(fmat_inv, corr.vol[iq1, iq2, :])
                self.vol[iq1, iq2, :] = dot
                if iq2 > iq1:
                    self.vol[iq2, iq1, :] = dot





    def fill_from_iqlm(self, iqlm, inc_odds=True):
        '''
        scorpy.BlqqVol.fill_from_iqlm():
            Fill the Blqq from a IqlmHandler object
        Arguments:
            iqlm : scorpy.IqlmHandler
                The IqlmHandler object to to fill from.
            inc_odds : bool
                Flag for including odd order harmonic functions in calculation.
        '''
        assert iqlm.nq == self.nq, 'IqlmHandler and BlqqVol have different nq'
        assert iqlm.qmax == self.qmax, 'IqlmHandler and BlqqVol have different qmax'


        for i, q1_coeffs in enumerate(iqlm.vals):

            for j, q2_coeffs in enumerate(iqlm.vals[i:]):

                multi = q1_coeffs * q2_coeffs

                if not inc_odds:
                    multi[:,1::2,:] =0

                self.vol[i, j + i, :] = multi.sum(axis=0).sum(axis=1)[:self.nl]
                if j > 0:
                    self.vol[j + i, i, :] = multi.sum(axis=0).sum(axis=1)[:self.nl]




