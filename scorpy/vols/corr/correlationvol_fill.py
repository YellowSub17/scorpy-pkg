


from ...utils.utils import verbose_dec
from ...utils.utils import to_polar
import time
import numpy as np


import matplotlib.pyplot as plt
from scipy import special

class CorrelationVolFill:





    @verbose_dec
    def fill_from_detector_imgs(self, imgs, cenx, ceny, verbose=0):
        '''
        scorpy.CorrelationVol.fill_from_detector_imgs():
            Fill the CorrelationVol from a collection of 2D detector image

        Arguments:
            img : np.array
            rmax : int
            cenx : float
            ceny : float
        '''

        for img in imgs:
            qt = to_polar(img, rmax=self.nq, cenx=cenx, ceny=ceny)
            self.correlate_convolve(qt, verbose=verbose-1)





    @verbose_dec
    def fill_from_cif(self, cif, method='scat_rect', chopf=0, verbose=0):
        '''
        scorpy.CorrelationVol.fill_from_cif():
            Fill the CorrelationVol from a CifData object
        Arguments:
            cif : scorpy.CifData
                The CifData object to to fill the CorrelationVol
            method : str
                Method to fill the correlation volume. Either "scat_sph" or "scat_rect"
                to use the spherical or rectilinear coordinates of the CifData.
        '''

        assert self.qmax >= cif.qmax, 'cif.qmax > corr.qmax'
        assert method in ['scat_sph', 'scat_rect'], 'Invalid correlation method.'

        nscats = cif.scat_rect.shape[0]
        nscats_chopped = round(nscats*chopf)

        print('')
        print('############')
        print(f'Filling CorrelationVol from CifData via {method}.')
        if chopf >0:
            print(f'Correlating {nscats-nscats_chopped} out of {nscats} vectors, chopping {chopf*100}%.')
        else:
            print(f'Correlating {nscats} vectors.')

        print(f'Started: {time.asctime()}')
        if method == 'scat_sph':
            self.correlate_scat_sph(cif.scat_sph, chopf=chopf, verbose=verbose-1)
        elif method == 'scat_rect':
            self.correlate_scat_rect(cif.scat_rect, chopf=chopf, verbose=verbose-1)
        elif method == 'scat_pol':
            self.correlate_scat_pol(cif.scat_pol, chopf=chopf, verbose=verbose-1)
        print(f'Finished: {time.asctime()}')
        print('############')
        print('')



    @verbose_dec
    def fill_from_peakdata(self, pk, method='scat_qpol', chopf=0, verbose=0):
        '''
        scorpy.CorrelationVol.fill_from_peakdata():
            Fill the CorrelationVol from a PeakData object.
        Arguments:
            pk : scorpy.PeakData
                The PeakData object to to fill the CorrelationVol
            method : str
                Method to fill the correlation volume. Either "scat_sph" or "scat_pol"
                to use the spherical or polar coordinates of the PeakData.
            verbose : bool
                Flag for printing extra information to the screen while correlating.
        '''

        # assert self.qmax >= pk.qmax, 'pk.qmax > corr.qmax'
        assert method in ['scat_qpol', 'scat_sph'], 'Invalid correlation method.'


        nscats = cif.scat_rect.shape[0]
        nscats_chopped = round(nscats*chopf)

        print('############')
        print(f'Filling CorrelationVol from Peakdata via {method}.')
        if chopf >0:
            print(f'Correlating {nscats-nscats_chopped} out of {nscats} peaks, chopping {chopf*100}%.')
        else:
            print(f'Correlating {nscats} peaks.')

        print(f'Started: {time.asctime()}\n')
        if method=='scat_qpol':
            self.correlate_scat_pol(pk.scat_qpol, chopf=chopf, verbose=verbose-1)
        if method=='scat_sph':
            self.correlate_scat_sph(pk.scat_sph, chopf=chopf, verbose=verbose-1)
        print(f'Finished: {time.asctime()}')
        print('############')




    













    @verbose_dec
    def fill_from_blqq(self, blqq, inc_odds=True, verbose=0):
        '''
        scorpy.CorrelationVol.fill_from_blqq():
            Fill the CorrelationVol from a BlqqVol object.
        Arguments:
            blqq : BlqqVol
                The BlqqVol object to to fill the CorrelationVol.
            inc_odds : bool
                Flag for including odd order harmonics in the calculation.
        '''
        assert self.nq == blqq.nq, 'BlqqVol and CorrelationVol have different nq'
        assert self.qmax == blqq.qmax, 'BlqqVol and CorrelationVol have different qmax'

        print('')
        print('############')
        print(f'Filling CorrelationVol from BlqqVol via Matrix Multiplication.')
        print(f'Filling started: {time.asctime()}')

        if inc_odds:
            lskip = 1
        else:
            lskip = 2

        # arguments for the legendre polynomial
        if self.cos_sample:
            args = self.psipts
        else:
            args = np.cos(self.psipts[::-1])

        # initialze fmat matrix
        fmat = np.zeros((self.npsi, blqq.nl))

        # for every even spherical harmonic
        for l in range(0, blqq.nl, lskip):
            leg_vals = special.eval_legendre(l, args)
            fmat[:, l] = leg_vals

        # for every q1 and q2 position
        for q1_ind in range(self.nq):
            print(f'q index: {q1_ind+1}/{self.nq}', end='\r')
            for q2_ind in range(q1_ind, self.nq):
                blv = blqq.vol[q1_ind, q2_ind, :] # vector as a function of L
                for psi_ind in range(self.npsi):
                    ft = fmat[psi_ind, :]
                    x = np.dot(blv, ft)

                    self.vol[q1_ind, q2_ind, psi_ind] = x # fill the volume
                    if q1_ind != q2_ind:  # if not on diagonal
                        self.vol[q2_ind, q1_ind, psi_ind] = x

        print('\x1b[2K', end='\r')
        print(f'Filling ended: {time.asctime()}')
        print('############')
        print('')






