


from ...utils.decorator_funcs import verbose_dec
from ...utils.convert_funcs import to_polar
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


    def fill_from_dragonfly_photons(self, photons_h5, det_h5):
        pass




    @verbose_dec
    def fill_from_cif(self, cif, nchunks=1, verbose=0):


        qxyzi = cif.scat_rect[:]

        qmags = cif.scat_sph[:,0]

        # only correlate less then qmax
        le_qmax_loc = np.where(qmags <= self.qmax)[0]
        qxyzi = qxyzi[le_qmax_loc]
        qmags = qmags[le_qmax_loc]

        # only correlate greater than qmin
        ge_qmin_loc = np.where(qmags >= self.qmin)[0]
        qxyzi = qxyzi[ge_qmin_loc]
        qmags = qmags[ge_qmin_loc]


        # only correlate intensity greater then 0
        Igt0_loc = np.where(qxyzi[:,-1]>0)[0]
        qxyzi = qxyzi[Igt0_loc]
        qmags = qmags[Igt0_loc]




        print(f'Filling CorrelationVol from CifData.')
        print(f'Started: {time.asctime()}')
        print(f'Correlating {qxyzi.shape[0]} vectors.')

        self.correlate_3D(qxyzi[:,:-1], qxyzi[:,-1], nchunks=nchunks, verbose=verbose-1)

        print(f'Finished: {time.asctime()}')



    @verbose_dec
    def fill_from_peakdata(self, pk, verbose=0):

        qti = pk.scat_qpol[:]
        qmags = qti[:,0]

        # only correlate less then qmax
        le_qmax_loc = np.where(qmags <= self.qmax)[0]
        qti = qti[le_qmax_loc]
        qmags = qmags[le_qmax_loc]

        # only correlate greater than qmin
        ge_qmin_loc = np.where(qmags >= self.qmin)[0]
        qti = qti[ge_qmin_loc]
        qmags = qmags[ge_qmin_loc]


        # only correlate intensity greater then 0
        Igt0_loc = np.where(qti[:,-1]>0)[0]
        qti = qti[Igt0_loc]
        qmags = qmags[Igt0_loc]



        print(f'Filling CorrelationVol from Peakdata.')
        print(f'Started: {time.asctime()}')
        print(f'Correlating {qti.shape[0]} peaks.')

        self.correlate_2D(qti[:,0], qti[:,1], qti[:,2], verbose=verbose-1)

        print(f'Finished: {time.asctime()}')





    @verbose_dec
    def fill_from_peakdata_saldin(self, pk, nchunks=1, verbose=0):


        qxyzi = pk.scat_qxyz[:]
        qmags = pk.scat_sph[:,0]

        # only correlate less then qmax
        le_qmax_loc = np.where(qmags <= self.qmax)[0]
        qxyzi = qxyzi[le_qmax_loc]
        qmags = qmags[le_qmax_loc]

        # only correlate greater than qmin
        ge_qmin_loc = np.where(qmags >= self.qmin)[0]
        qxyzi = qxyzi[ge_qmin_loc]
        qmags = qmags[ge_qmin_loc]


        # only correlate intensity greater then 0
        Igt0_loc = np.where(qxyzi[:,-1]>0)[0]
        qxyzi = qxyzi[Igt0_loc]
        qmags = qmags[Igt0_loc]




        print(f'Filling CorrelationVol from PeakData (Saldin Style).')
        print(f'Started: {time.asctime()}')
        print(f'Correlating {qxyzi.shape[0]} vectors.')

        self.correlate_3D(qxyzi[:,:-1], qxyzi[:,-1], nchunks=nchunks, verbose=verbose-1)

        print(f'Finished: {time.asctime()}')




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

        # print('\x1b[2K', end='\r')
        print(f'Filling ended: {time.asctime()}')
        print('############')
        print('')






