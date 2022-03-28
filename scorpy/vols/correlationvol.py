from scipy import special
import numpy as np
import time

from ..utils import angle_between_pol, angle_between_sph, angle_between_rect, index_x, verbose_dec
from .vol import Vol
from .volsprops import CorrelationVolProps


class CorrelationVol(Vol, CorrelationVolProps):
    """scorpy.CorrelationVol:
    A representaion of the scattering correlation function.
    Attributes:
        nq, npsi : int
        qmax : float
        dq,dpsi : float
        qpts,psipts : numpy.array
    Methods:
        CorrelationVol.fill_from_cif()
        CorrelationVol.fill_from_blqq()
        CorrelationVol.fill_from_peakdata()
        CorrelationVol.correlate_scat_rect()
        CorrelationVol.correlate_scat_pol()
        CorrelationVol.correlate_scat_sph()
        CorrelationVol.plot_q1q2()
    """

    def __init__(self, nq=100, npsi=180, qmax=1, cos_sample=True, inc_self_corr=True, path=None):




        if path is not None:
            Vol.__init__(self, path=path)
        else:

            if cos_sample:
                Vol.__init__(self, nq, nq, npsi, 0, 0, -1, qmax, qmax, 1, False, False, False, comp=False, path=path)
            else:
                Vol.__init__(self, nq, nq, npsi, 0, 0, 0, qmax, qmax, np.pi, False, False, False, comp=False, path=path)

            self._cos_sample = cos_sample
            self._inc_self_corr = inc_self_corr

        self.plot_q1q2 = self.plot_xy

    def _save_extra(self, f):
        f.write('[corr]\n')
        f.write(f'qmax = {self.qmax}\n')
        f.write(f'nq = {self.nq}\n')
        f.write(f'npsi = {self.npsi}\n')
        f.write(f'dq = {self.dq}\n')
        f.write(f'dpsi = {self.dpsi}\n')
        f.write(f'cos_sample = {self.cos_sample}\n')
        f.write(f'inc_self_corr = {self.inc_self_corr}\n')

    def _load_extra(self, config):
        self._cos_sample = config.getboolean('corr', 'cos_sample')
        self._inc_self_corr = config.getboolean('corr', 'inc_self_corr')




    def qpsi_correction(self):

        q1q1, q2q2, psipsi = np.meshgrid(self.qpts, self.qpts, self.psipts)

        self.vol *= np.sin(psipsi)
        self.vol *= (q1q1*q2q2)





######## FILL FROM

    @verbose_dec
    def fill_from_cif(self, cif, method='scat_rect', verbose=0):
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
        assert method in ['scat_sph', 'scat_rect', 'scat_pol'], 'Invalid correlation method.'

        print('')
        print('############')
        print(f'Filling CorrelationVol from CifData via {method}.')
        print(f'Correlating {cif.scat_rect.shape[0]} vectors.')
        print(f'Started: {time.asctime()}')

        if method == 'scat_sph':
            # print('', end='\n')
            self.correlate_scat_sph(cif.scat_sph, verbose=verbose-1)
        elif method == 'scat_rect':
            # print('', end='\n')
            self.correlate_scat_rect(cif.scat_rect, verbose=verbose-1)
        elif method == 'scat_pol':
            # print('', end='\n')
            self.correlate_scat_pol(cif.scat_pol, verbose=verbose-1)

        print(f'Finished: {time.asctime()}')
        print('############')
        print('')




    @verbose_dec
    def fill_from_peakdata(self, pk, method='scat_pol', verbose=0):
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

        assert self.qmax >= pk.qmax, 'pk.qmax > corr.qmax'
        assert method in ['scat_pol', 'scat_sph'], 'Invalid correlation method.'


        frames = pk.split_frames()
        nframes = len(frames)

        print('############')
        print(f'Filling CorrelationVol from Peakdata via {method}.')
        print(f'Correlation started: {time.asctime()}\n')

        if method=='scat_pol':
            for i, frame in enumerate(frames):
                print(f'Frame: {i+1}/{nframes}', end='\n')
                self.correlate_scat_pol(frame.scat_pol[:,1:], verbose=verbose-1)
                print('\x1b[2A\x1b[2K', end='\n')

        if method=='scat_sph':
            for i, frame in enumerate(frames):
                print(f'Frame: {i+1}/{nframes}', end='\n')
                self.correlate_scat_sph(frame.scat_sph[:,1:])
                print('\x1b[2A\x1b[2K', end='\n')

        print(f'Correlation ended: {time.asctime()}\n')
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



######## CORRELATE



    @verbose_dec
    def correlate_scat_pol(self, qti, verbose=0):
        '''
        scorpy.CorrelationVol.correlate_scat_pol():
            Correlate diffraction peaks in 2D polar coordinates.
        Arguments:
            qti : numpy.ndarray
                n by 3 array of n peaks to correlate. Columns of array should be
                polar radius or peak (A-1), polar angle of peak (degrees), and
                intensity of the peak.
        '''
        # only correlate less than qmax

        le_qmax = np.where(qti[:, 0] <= self.qmax)[0]
        qti = qti[le_qmax]

        qti[:,1] = np.degrees(qti[:,1])

        nscats = qti.shape[0]
        # calculate q indices of every scattering vector outside of loop
        ite = np.ones(nscats)
        q_inds = list(map(index_x, qti[:, 0], 0 * ite, self.qmax * ite, self.nq * ite))



        # calc start and end positions if inlcuding self correlation
        if self.inc_self_corr:
            q2start_term, q2end_term = 0, None
        else:
            q2start_term, q2end_term = 1, None


        for i, q1 in enumerate(qti):
            print(f'Peak: {i+1}/{nscats}', end='\r')
            # get q index
            q1_ind = q_inds[i]


            for j, q2 in enumerate(qti[i+q2start_term:q2end_term]):
                # get q index
                q2_ind = q_inds[i + j+q2start_term]

                # get the angle between vectors, and index it
                psi = angle_between_pol(q1[1], q2[1])

                if self.cos_sample:
                    psi = np.cos(np.radians(psi))
                else:
                    psi = np.radians(psi)

                psi_ind = index_x(psi, self.zmin, self.zmax, self.npsi, wrap=self.zwrap)

                # fill the volume
                self.vol[q1_ind, q2_ind, psi_ind] += q1[-1] * q2[-1]
                if j > 0:  # if not on diagonal
                    self.vol[q2_ind, q1_ind, psi_ind] += q1[-1] * q2[-1]
        print('\x1b[2K', end='\r')



    @verbose_dec
    def correlate_scat_rect(self, qxyzi, verbose=0):
        '''
        scorpy.CorrelationVol.correlate_scat_pol():
            Correlate diffraction peaks in 3D rectilinear coordinates.
        Arguments:
            qxyzi : numpy.ndarray
                n by 4 array of n peaks to correlate. First 3 columns of array
                should be the reciprocal space coordinates of peaks (qx,qy,qz),
                and the last coloumn should be the intensity of the peak.
        '''
        # only correlate less than qmax
        qmags = np.linalg.norm(qxyzi[:, :3], axis=1)
        le_qmax = np.where(qmags <= self.qmax)[0]
        qxyzi = qxyzi[le_qmax]
        qmags = qmags[le_qmax]

        nscats = qxyzi.shape[0]

        # calculate q indices of every scattering vector outside of loop
        ite = np.ones(nscats)
        q_inds = list(map(index_x, qmags, 0 * ite, self.qmax * ite, self.nq * ite))

        # calc start and end positions if inlcuding self correlation
        if self.inc_self_corr:
            q2start_term, q2end_term = 0, None
        else:
            q2start_term, q2end_term = 1, None


        for i, q1 in enumerate(qxyzi):
            print(f'Peak: {i+1}/{nscats}', end='\r')

            # get q index
            q1_ind = q_inds[i]

            for j, q2 in enumerate(qxyzi[i+q2start_term:q2end_term]):
                # get q index
                q2_ind = q_inds[i + j+q2start_term]

                # get the angle between vectors, and index it
                psi = angle_between_rect(q1[:3], q2[:3])

                if not self.cos_sample:
                    psi = np.arccos(psi)

                psi_ind = index_x(psi, self.zmin, self.zmax, self.npsi, wrap=self.zwrap)

                # fill the volume
                self.vol[q1_ind, q2_ind, psi_ind] += q1[-1] * q2[-1]
                if j > 0:  # if not on diagonal
                    self.vol[q2_ind, q1_ind, psi_ind] += q1[-1] * q2[-1]

        print('\x1b[2K', end='\r')




    @verbose_dec
    def correlate_scat_sph(self, qtpi, verbose=0):
        '''
        scorpy.CorrelationVol.correlate_scat_sph():
            Correlate diffraction peaks in 3D spherical coordinates.
        Arguments:
            qtpi : numpy.ndarray
                n by 4 array of n peaks to correlate. Columns of the array should
                be the spherical radius of the peak (A-1), polar angle of the peak
                (theta, radians), and the azimuthial angle of the peak (phi, radians).
        '''
        # only correlate less than qmax
        le_qmax = np.where(qtpi[:, 0] <= self.qmax)[0]
        qtpi = qtpi[le_qmax]


        nscats = qtpi.shape[0]
        # calculate q indices of every scattering vector outside of loop
        ite = np.ones(nscats)
        q_inds = list(map(index_x, qtpi[:, 0], 0 * ite, self.qmax * ite, self.nq * ite))

        # calc start and end positions if inlcuding self correlation
        if self.inc_self_corr:
            q2start_term, q2end_term = 0, None
        else:
            q2start_term, q2end_term = 1, -1




        for i, q1 in enumerate(qtpi):

            print(f'Peak: {i+1}/{nscats}', end='\r')
            # get q index, theta and phi
            q1_ind = q_inds[i]
            theta1 = q1[1]
            phi1 = q1[2]

            for j, q2 in enumerate(qtpi[i+q2start_term:q2end_term]):

                # get q index, theta and phi
                q2_ind = q_inds[i + j+q2start_term]
                theta2 = q2[1]
                phi2 = q2[2]

                # get the angle between angluar coordinates, and index it
                psi = angle_between_sph(theta1, theta2, phi1, phi2)

                if not self.cos_sample:
                    psi = np.arccos(psi)

                psi_ind = index_x(psi, self.zmin, self.zmax, self.npsi, wrap=self.zwrap)

                # fill the volume
                self.vol[q1_ind, q2_ind, psi_ind] += q1[-1] * q2[-1]

                if j > 0:  # if not on diagonal
                    self.vol[q2_ind, q1_ind, psi_ind] += q1[-1] * q2[-1]


        print('\x1b[2K', end='\r')



    def correlate_fft_pol(self, polar):

        fpolar = np.fft.fft( polar, axis=1 )

        out = np.zeros( (polar.shape[0],polar.shape[0],polar.shape[1]), np.complex128)

        for i, fp_rowi in enumerate(fpolar):
            for j, fp_rowj in enumerate(fpolar):
                out[i,j,:] = fp_rowi*fp_rowj.conjugate()


        out = np.real(np.fft.ifft( out, axis=2 ))

        return out

