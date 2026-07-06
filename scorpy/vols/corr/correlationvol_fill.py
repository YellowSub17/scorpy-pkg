

from ...utils.decorator_funcs import verbose_dec
import time
import numpy as np


import matplotlib.pyplot as plt
from scipy import special
import h5py

class CorrelationVolFill:
    """
    Mixin class providing methods to fill a CorrelationVol from various
    data sources (detector images, dragonfly photon files, CIF data,
    peak data, and BlqqVol objects).
    """






    @verbose_dec
    def fill_from_detector_imgs(self, imgs, cenx, ceny, verbose=0):
        """
        Fill the CorrelationVol from a collection of 2D detector images.

        Each image is converted to polar (q, theta) coordinates and
        correlated via FFT convolution.

        Parameters
        ----------
        imgs : iterable of numpy.ndarray
            Collection of 2D detector images to correlate.
        cenx : float
            x-coordinate of the beam center on the detector.
        ceny : float
            y-coordinate of the beam center on the detector.
        verbose : int, optional
            Verbosity level for progress printing (default 0).

        Returns
        -------
        None
            ``self.vol`` is updated in place.
        """

        for img in imgs:
            qt = to_polar(img, rmax=self.nq, cenx=cenx, ceny=ceny)
            self.correlate_convolve(qt, verbose=verbose-1)

        


    @verbose_dec
    def fill_from_dragonfly_photons(self, photons_h5, det_h5, frame_max=None, verbose=0):
        """
        Fill the CorrelationVol from Dragonfly photon and detector files.

        Loads sparse photon-count data from a Dragonfly-format photons
        HDF5 file and geometry from a detector HDF5 file, reconstructs
        per-frame peak lists of Cartesian scattering vectors and
        intensities, and correlates each frame via ``correlate_3D``.

        Parameters
        ----------
        photons_h5 : str
            Path to the Dragonfly-format photons HDF5 file, containing
            ``num_pix``, ``place_ones``, ``count_multi`` and
            ``place_multi`` datasets.
        det_h5 : str
            Path to the detector geometry HDF5 file, containing
            ``corr``, ``detd``, ``ewald_rad``, ``mask``, ``qx``, ``qy``
            and ``qz`` datasets.
        frame_max : int, optional
            Maximum number of frames to process. If None, all frames in
            the photons file are processed (default None).
        verbose : int, optional
            Verbosity level for progress printing (default 0).

        Returns
        -------
        None
            ``self.vol`` is updated in place.
        """
        print('Loading photons')
        f = h5py.File(photons_h5)
        num_pix = f['/num_pix'][...]
        place_ones = f['/place_ones'][...]
        count_multi = f['/count_multi'][...]
        place_multi = f['/place_multi'][...]
        f.close()

        print('Loading detector')
        f = h5py.File(det_h5)
        corr = f['/corr'][...]
        detd = f['/detd'][...]
        ewald_rad = f['/ewald_rad'][...]
        mask = f['/mask'][...]
        qx = f['/qx'][...]
        qy = f['/qy'][...]
        qz = f['/qz'][...]
        f.close()

        if frame_max is None:
            frame_max=len(place_ones)

        for i_frame, (frame_place_ones, frame_place_multi, frame_counts_multi) in enumerate(zip(place_ones[:frame_max], place_multi[:frame_max], count_multi[:frame_max])):
            print(f'Frame: \t\t{i_frame}/{frame_max}', end='\r')

            npeaks_frame = frame_place_ones.size + frame_place_multi.size
            peak_list = np.zeros( (npeaks_frame, 4) )

            for i_peak, peak_pix_i in enumerate(place_ones[i_frame]):
                peak_list[i_peak, :3] = [qx[peak_pix_i], qy[peak_pix_i], qz[peak_pix_i]]
                peak_list[i_peak, -1] = 1

            for j_peak, peak_pix_i in enumerate(place_multi[i_frame]):
                peak_list[i_peak+j_peak+1,:3] = [qx[peak_pix_i], qy[peak_pix_i], qz[peak_pix_i]]
                peak_list[i_peak+j_peak+1, -1] = count_multi[i_frame][j_peak]

            self.correlate_3D(peak_list[:,:-1], peak_list[:,-1], verbose=verbose-1)










    @verbose_dec
    def fill_from_cif(self, cif, nchunks=1, verbose=0):
        """
        Fill the CorrelationVol from a CifData object.

        Filters the scattering vectors in ``cif`` to those with q
        magnitude between ``self.qmin`` and ``self.qmax`` and intensity
        greater than zero, then correlates the remaining vectors via
        ``correlate_3D``.

        Parameters
        ----------
        cif : CifData
            The CifData object providing scattering vectors
            (``scat_rect``) and magnitudes (``scat_sph``) to correlate.
        nchunks : int, optional
            Number of chunks to split the vectors into during
            correlation, to limit memory usage (default 1).
        verbose : int, optional
            Verbosity level for progress printing (default 0).

        Returns
        -------
        None
            ``self.vol`` is updated in place.
        """


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
        """
        Fill the CorrelationVol from a PeakData object (2D peaks).

        Filters the peaks in ``pk`` to those with q magnitude between
        ``self.qmin`` and ``self.qmax`` and intensity greater than zero,
        then correlates the remaining peaks via ``correlate_2D``.

        Parameters
        ----------
        pk : PeakData
            The PeakData object providing peaks in (q, theta, I) polar
            form (``scat_qpol``) to correlate.
        verbose : int, optional
            Verbosity level for progress printing (default 0).

        Returns
        -------
        None
            ``self.vol`` is updated in place.
        """

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
        """
        Fill the CorrelationVol from a PeakData object (Saldin-style, 3D).

        Filters the peaks in ``pk`` to those with q magnitude between
        ``self.qmin`` and ``self.qmax`` and intensity greater than zero,
        then correlates the remaining peaks' Cartesian scattering
        vectors via ``correlate_3D``.

        Parameters
        ----------
        pk : PeakData
            The PeakData object providing Cartesian scattering vectors
            (``scat_qxyz``) and spherical magnitudes (``scat_sph``) to
            correlate.
        nchunks : int, optional
            Number of chunks to split the vectors into during
            correlation, to limit memory usage (default 1).
        verbose : int, optional
            Verbosity level for progress printing (default 0).

        Returns
        -------
        None
            ``self.vol`` is updated in place.
        """


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
        """
        Fill the CorrelationVol from a BlqqVol object.

        Reconstructs the correlation volume from the spherical harmonic
        expansion coefficients stored in ``blqq`` via matrix
        multiplication with Legendre polynomial values.

        Parameters
        ----------
        blqq : BlqqVol
            The BlqqVol object used to fill the CorrelationVol. Must
            have the same ``nq`` and ``qmax`` as ``self``.
        inc_odds : bool, optional
            Flag for including odd order harmonics in the calculation
            (default True).
        verbose : int, optional
            Verbosity level for progress printing (default 0).

        Returns
        -------
        None
            ``self.vol`` is updated in place.
        """
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
