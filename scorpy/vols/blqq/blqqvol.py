import numpy as np
from scipy import special
import matplotlib.pyplot as plt
from ..base.basevol import BaseVol
from .blqqvol_props import BlqqVolProps
from .blqqvol_plot import BlqqVolPlot
from .blqqvol_saveload import BlqqVolSaveLoad
from ...utils.decorator_funcs import verbose_dec
from ...utils.calc_funcs import saldin_theta
import time


class BlqqVol(BaseVol, BlqqVolProps):
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

    def __init__(self, nq=100, nl=90, qmax=1, qmin=0, path=None, comp=False):

        BaseVol.__init__(self, nx=nq, ny=nq, nz=nl,
                     xmin=qmin, ymin=qmin, zmin=0,
                     xmax=qmax, ymax=qmax, zmax=nl - 1,
                     xwrap=False, ywrap=False, zwrap=False,
                     comp=False, path=path)

        self.plot_q1q2 = self.plot_xy






    @verbose_dec
    def fill_from_corr(self, corr, rcond=None, verbose=0):
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
        assert corr.qmin == self.qmin, 'CorrelationVol and BlqqVol have different qmin'

        print('')
        print('############')
        print(f'Filling BlqqVol from CorrelationVol via Pseudo Matrix Inversion.')
        print(f'Started: {time.asctime()}')


        ## legendre argument is -1 to 1
        if corr.cos_sample:
            args = corr.psipts
        else:
            args = np.cos(corr.psipts)

        # initialze fmat matrix
        fmat = np.zeros((corr.npsi, self.nl))

        # for every spherical harmonic
        for l in range(0, self.nl):
            leg_vals = special.eval_legendre(l, args)
            fmat[:, l] = leg_vals

        #if rcond is given, use it, else, use default
        if rcond is not None:
            fmat_inv = np.linalg.pinv(fmat, rcond=rcond)
        else:
            fmat_inv = np.linalg.pinv(fmat)


        for iq1 in range(self.nq):
            print(f'q index: {iq1+1}/{self.nq}', end='\r')
            for iq2 in range(iq1, self.nq):

                dot = np.dot(fmat_inv, corr.vol[iq1, iq2, :])
                self.vol[iq1, iq2, :] = dot
                if iq2 > iq1:
                    self.vol[iq2, iq1, :] = dot

        print('\x1b[2K', end='\r')
        print(f'Ended: {time.asctime()}')
        print('############')
        print('')

    @verbose_dec
    def fill_from_corr_ews_fmat(self, corr, k=0.107, rcond=None, verbose=0):
        '''
        scorpy.BlqqVol.fill_from_corr():
            Fill the Blqq from a CorrelationVol object, accounting for ews
        Arguments:
            corr : scorpy.CorrelationVol
                The CorrelationVol object to to fill from.
            k : wavenumber
                default is 1.33keV -> 9.322 A -> k=0.107
            inc_odds : bool
                Flag for including odd order harmonic functions in calculation.
            rcond : float
                Condition number scale for SVD calculation.
        '''

        assert corr.nq == self.nq, 'CorrelationVol and BlqqVol have different nq'
        assert corr.qmax == self.qmax, 'CorrelationVol and BlqqVol have different qmax'
        assert corr.qmin == self.qmin, 'CorrelationVol and BlqqVol have different qmin'

        print('')
        print('############')
        print(f'Filling BlqqVol from CorrelationVol via Pseudo Matrix Inversion.')
        print(f'F matrix will include EWS correction.')
        print(f'Started: {time.asctime()}')




        t1s = saldin_theta(np.linspace(corr.qmin, corr.qmax, corr.npsi), k)
        t2s = saldin_theta(np.linspace(corr.qmin, corr.qmax, corr.npsi), k)

        ## legendre argument is -1 to 1
        if corr.cos_sample:
            phis = np.arccos(corr.psipts)
        else:
            phi =corr.psipts

    
        
        psi = np.cos(t1s)*np.cos(t2s) + np.sin(t1s)*np.sin(t2s)*np.cos(phis)
        args = np.cos(psi)

        # initialze fmat matrix
        fmat = np.zeros((corr.npsi, self.nl))

        # for every spherical harmonic
        for l in range(0, self.nl,2):
            leg_vals = special.eval_legendre(l, args)
            fmat[:, l] = leg_vals

        #if rcond is given, use it, else, use default
        if rcond is not None:
            fmat_inv = np.linalg.pinv(fmat, rcond=rcond)
        else:
            fmat_inv = np.linalg.pinv(fmat)

        return fmat




        # for iq1 in range(self.nq):
            # print(f'q index: {iq1+1}/{self.nq}', end='\r')
            # for iq2 in range(iq1, self.nq):

                # # t1 = saldin_theta(corr.qpts[

                # ####TODO:
                # #### FMATRIX WITH EWS correlation needs to be calculated at every 

                # dot = np.dot(fmat_inv, corr.vol[iq1, iq2, :])
                # self.vol[iq1, iq2, :] = dot
                # if iq2 > iq1:
                    # self.vol[iq2, iq1, :] = dot

        # print('\x1b[2K', end='\r')
        # print(f'Ended: {time.asctime()}')
        # print('############')
        # print('')







    def fill_from_iqlm(self, iqlm, verbose=0):
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
        assert iqlm.qmin == self.qmin, 'IqlmHandler and BlqqVol have different qmin'




        for i, q1_coeffs in enumerate(iqlm.vals):

            for j, q2_coeffs in enumerate(iqlm.vals[i:]):

                multi = q1_coeffs * q2_coeffs


                self.vol[i, j + i, :] = multi.sum(axis=0).sum(axis=1)[:self.nl]
                if j > 0:
                    self.vol[j + i, i, :] = multi.sum(axis=0).sum(axis=1)[:self.nl]






