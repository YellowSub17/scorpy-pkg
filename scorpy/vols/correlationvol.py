from scipy import special
import numpy as np
import time

from ..utils import angle_between_pol, angle_between_sph, angle_between_rect, index_x
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






    def fill_from_cif(self, cif, method='scat_rect', verbose=True):
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

        if verbose:
            print('############')
            print(f'Filling CorrelationVol from CifData via {method}.')
            print(f'Correlating {cif.scat_rect.shape[0]} vectors.')
            print(f'Correlation started: {time.asctime()}\n')

        if method == 'scat_sph':
            self.correlate_scat_sph(cif.scat_sph)
        elif method == 'scat_rect':
            self.correlate_scat_rect(cif.scat_rect)

        if verbose:
            print(f'Correlation finished: {time.asctime()}')
            print('############')




    def fill_from_peakdata(self, pk, method='scat_pol', verbose=True, npeakmax=-1):
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


        frames = pk.split_frames(npeakmax=npeakmax)
        nframes = len(frames)

        if verbose:
            print('')
            print('############')
            print(f'Filling CorrelationVol from Peakdata via {method}.')
            print(f'Correlating {nframes} frames.')
            print(f'Correlation started: {time.asctime()}\n')

        if method=='scat_pol':
            for i, frame in enumerate(frames):
                print(f'Frame: {i+1}/{nframes}', end='\r')
                self.correlate_scat_pol(frame.scat_pol)
                print('', end='')

        if method=='scat_sph':
            for i, frame in enumerate(frames):
                print(f'Frame: {i+1}/{nframes}', end='\r')
                self.correlate_scat_sph(frame.scat_sph)
                print('', end='')

        if verbose:
            print(f'Correlation finished: {time.asctime()}')
            print('############')
            print('')











    def fill_from_blqq(self, blqq, inc_odds=True):
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
            for q2_ind in range(q1_ind, self.nq):
                blv = blqq.vol[q1_ind, q2_ind, :] # vector as a function of L
                for psi_ind in range(self.npsi):
                    ft = fmat[psi_ind, :]
                    x = np.dot(blv, ft)

                    self.vol[q1_ind, q2_ind, psi_ind] = x # fill the volume
                    if q1_ind != q2_ind:  # if not on diagonal
                        self.vol[q2_ind, q1_ind, psi_ind] = x


    def fill_from_sphv(self, sphv):
        '''
        scorpy.CorrelationVol.fill_from_sphv):
            Fill the CorrelationVol from a SphericalVol object.
        Arguments:
            sphv : SphericalVol
                The SphericalVol object to to fill the CorrelationVol.
            inc_odds : bool
                Flag for including odd order harmonics in the calculation.
        '''
        # mesh grid of phi and theta


        assert self.nq == sphv.nq, 'SphericalVol and CorrelationVol have different nq'
        assert self.qmax == sphv.qmax, 'SphericalVol and CorrelationVol have different qmax'
        assert self.inc_self_corr, 'self correlation must be included to fill from sphv'

        pp, tt = np.meshgrid(sphv.phipts, sphv.thetapts)
        zero_slice = np.zeros( (sphv.ntheta, sphv.nphi))

        print('Started: ', time.asctime())
        # for every pair of q1 and q2 shells...
        for q1_ind in range(0, sphv.nq):
            q1_slice = sphv.vol[q1_ind, ...]
            #if the slice is 0, the correlation is 0
            if np.all(q1_slice == zero_slice):
                continue
            for q2_ind in range(q1_ind, sphv.nq):
                q2_slice = sphv.vol[q2_ind, ...]
                #if the slice is 0, the correlation is 0
                if np.all(q2_slice == zero_slice):
                    continue

                print('q1_ind:', q1_ind, 'q2ind:', q2_ind, end='\r')
                # for every orientation of shell
                for theta_ind in range(0, sphv.ntheta):
                    for phi_ind in range(0, sphv.nphi):

                        # change the orienation of shell
                        pp_rolled = np.roll(pp, (theta_ind, phi_ind), (0, 1))
                        tt_rolled = np.roll(tt, (theta_ind, phi_ind), (0, 1))

                        # correlate the intensities, where q2 is oritented
                        II1 = q1_slice * np.roll(q2_slice, (theta_ind, phi_ind), (0, 1))
                        II1 *=  np.sin(tt_rolled) * np.sin(tt)

                        II2 = q2_slice * np.roll(q1_slice, (theta_ind, phi_ind), (0, 1))
                        II2 *=  np.sin(tt_rolled) * np.sin(tt)

                        if II1.max()==0 and II2.max()==0:
                            continue

                        # find the angle between unorientated and new orientation
                        angle_between_flat = list(map(angle_between_sph,
                                                      tt.flatten(), tt_rolled.flatten(),
                                                      pp.flatten(), pp_rolled.flatten()))

                        if not self.cos_sample:
                            angle_between_flat = np.arccos(angle_between_flat)

                        ite = np.ones(len(angle_between_flat))

                        # find the index of psi, the angle between orientated shells
                        angle_between_ind = list(map(index_x, angle_between_flat, -1 * ite, ite, sphv.nphi * ite, ite))

                        # reshape the flattens array (flat arrays work well with map() )
                        angle_between_rolled = np.array(angle_between_ind).reshape(sphv.ntheta, sphv.nphi)


                        # cut positions where I=0
                        locII1 = np.where(II1.flatten()!=0)
                        locII2 = np.where(II2.flatten()!=0)


                        # for every pair of psi index and inntensity values, add them to the correlation volume
                        if q1_ind == q2_ind:
                            for angle_ind, II_val in zip(angle_between_rolled.flatten()[locII1], II1.flatten()[locII2]):
                                self.vol[q1_ind, q2_ind, angle_ind] += II_val

                        else:
                            for angle_ind, II_val in zip(angle_between_rolled.flatten(), II1.flatten()):
                                self.vol[q1_ind, q2_ind, angle_ind] += II_val

                            for angle_ind, II_val in zip(angle_between_rolled.flatten(), II2.flatten()):
                                self.vol[q2_ind, q1_ind, angle_ind] += II_val



    def fill_from_xfmh5(self, xfmh5):
        pass



    def correlate_fft_pol(self, polar):

        fpolar = np.fft.fft( polar, axis=1 )

        out = np.zeros( (polar.shape[0],polar.shape[0],polar.shape[1]), np.complex128)

        for i, fp_rowi in enumerate(fpolar):
            for j, fp_rowj in enumerate(fpolar):
                out[i,j,:] = fp_rowi*fp_rowj.conjugate()


        out = np.real(np.fft.ifft( out, axis=2 ))

        return out


    def correlate_scat_pol(self, qti):
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

        # calculate q indices of every scattering vector outside of loop
        ite = np.ones(qti.shape[0])
        q_inds = list(map(index_x, qti[:, 0], 0 * ite, self.qmax * ite, self.nq * ite))


        # calc start and end positions if inlcuding self correlation
        if self.inc_self_corr:
            q2start_term, q2end_term = 0, None
        else:
            q2start_term, q2end_term = 1, -1


        for i, q1 in enumerate(qti):
            # get q index
            q1_ind = q_inds[i]

            for j, q2 in enumerate(qti[i+q2start_term:q2end_term]):
                # get q index
                q2_ind = q_inds[i + j]

                # get the angle between vectors, and index it
                psi = angle_between_pol(q1[1], q2[1])

                if not self.cos_sample:
                    psi = np.arccos(psi)

                psi_ind = index_x(psi, self.zmin, self.zmax, self.npsi, wrap=self.zwrap)

                # fill the volume
                self.vol[q1_ind, q2_ind, psi_ind] += q1[-1] * q2[-1]
                if j > 0:  # if not on diagonal
                    self.vol[q2_ind, q1_ind, psi_ind] += q1[-1] * q2[-1]





    def correlate_scat_rect(self, qxyzi):
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
            q2start_term, q2end_term = 1, -1


        for i, q1 in enumerate(qxyzi):

            # get q index
            q1_ind = q_inds[i]
            # print(f'{i}/{nscats}', end='\r')

            for j, q2 in enumerate(qxyzi[i+q2start_term:q2end_term]):
                # get q index
                q2_ind = q_inds[i + j]

                # get the angle between vectors, and index it
                psi = angle_between_rect(q1[:3], q2[:3])

                if not self.cos_sample:
                    psi = np.arccos(psi)

                psi_ind = index_x(psi, self.zmin, self.zmax, self.npsi, wrap=self.zwrap)

                # fill the volume
                self.vol[q1_ind, q2_ind, psi_ind] += q1[-1] * q2[-1]
                if j > 0:  # if not on diagonal
                    self.vol[q2_ind, q1_ind, psi_ind] += q1[-1] * q2[-1]




    def correlate_scat_sph(self, qtpi):
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

        # calculate q indices of every scattering vector outside of loop
        ite = np.ones(qtpi.shape[0])
        q_inds = list(map(index_x, qtpi[:, 0], 0 * ite, self.qmax * ite, self.nq * ite))

        # calc start and end positions if inlcuding self correlation
        if self.inc_self_corr:
            q2start_term, q2end_term = 0, None
        else:
            q2start_term, q2end_term = 1, -1



        for i, q1 in enumerate(qtpi):
            # get q index, theta and phi
            q1_ind = q_inds[i]
            theta1 = q1[1]
            phi1 = q1[2]

            for j, q2 in enumerate(qtpi[i+q2start_term:q2end_term]):
                # get q index, theta and phi
                q2_ind = q_inds[i + j]
                theta2 = q2[1]
                phi2 = q2[2]

                # get the angle between angluar coordinates, and index it
                psi = angle_between_sph(theta1, theta2, phi1, phi2)

                if not self.cos_sample:
                    psi = np.arccos(psi)

                psi_ind = index_x(psi, self.zmin, self.zmax, self.npsi, wrap=self.zwrap)

                # fill the volume
                try:
                    self.vol[q1_ind, q2_ind, psi_ind] += q1[-1] * q2[-1]
                except IndexError:
                    print(q1_ind, q2_ind, psi_ind)
                    print(q1[0])
                    print(q2[0])
                    exit()

                if j > 0:  # if not on diagonal
                    self.vol[q2_ind, q1_ind, psi_ind] += q1[-1] * q2[-1]







