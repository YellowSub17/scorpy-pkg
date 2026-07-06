import numpy as np



from ...utils.convert_funcs import index_x_nowrap
from ...utils.decorator_funcs import verbose_dec



class CorrelationVolCorr:
    """
    Mixin class providing correlation routines for CorrelationVol.

    Methods correlate scattering vectors or detector data and sum the
    results into the parent object's ``vol`` array.
    """

    def correlate_convolve(self, qt):
        """
        Correlate q-t detector data via FFT convolution.

        Computes the angular autocorrelation of each row of ``qt`` (and
        cross-correlation between rows) using the convolution theorem, and
        accumulates the real part of the result into ``self.vol``.

        Parameters
        ----------
        qt : numpy.ndarray
            2D array of intensities in polar (q, theta) coordinates, with
            shape (nq, ntheta). Each row corresponds to a q-ring.

        Returns
        -------
        None
            ``self.vol`` is updated in place.
        """
        f_qt = np.fft.fft(qt, axis=1)
        for i, f_qtrowi in enumerate(f_qt):
            for j, f_qtrowj in enumerate(f_qt[i:]):

                convolved_rows = np.fft.ifft(f_qtrowi*f_qtrowj.conjugate(), axis=0)
                self.vol[i, j+i, :] += np.real(convolved_rows)
                if j>0:
                    self.vol[j+i, i, : ] += np.real(convolved_rows)




    @verbose_dec
    def correlate_3D(self, xyz, I, nchunks=1, verbose=0):
        """
        Correlate a set of 3D scattering vectors.

        Splits the vectors into chunks and, for every pair of vectors
        (q1, q2) between and within chunks, computes the magnitudes of
        each vector and the angle (or cosine of the angle) between them,
        then sums the intensity products into ``self.vol`` via
        ``correlate_via_sum``.

        Parameters
        ----------
        xyz : numpy.ndarray
            Array of shape (nvec, 3) giving the Cartesian scattering
            vector coordinates.
        I : numpy.ndarray
            Array of shape (nvec,) giving the intensity of each
            scattering vector.
        nchunks : int, optional
            Number of chunks to split ``xyz`` and ``I`` into, to limit
            memory usage for large vector sets (default 1, i.e. no
            splitting).
        verbose : int, optional
            Verbosity level for progress printing (default 0).

        Returns
        -------
        None
            ``self.vol`` is updated in place.
        """

        xyz_q2s = np.array_split(xyz, nchunks)
        I_q2s = np.array_split(I, nchunks)


        q2_counter=0
        for i_chunk,  (xyz_q2, I_q2) in enumerate(zip( xyz_q2s, I_q2s)):

            if nchunks>1:
                print(f'Chunk: {i_chunk+1}/{nchunks}')

            xyz_q1 = xyz[q2_counter:]
            I_q1 = I[q2_counter:]


            nvec_q1 = xyz_q1.shape[0]
            nvec_q2 = xyz_q2.shape[0]
            q2_counter+= nvec_q2




            norms_q1 = np.linalg.norm(xyz_q1, axis=1)
            norms_q2 = np.linalg.norm(xyz_q2, axis=1)

            xyz_dot_xyz = xyz_q1@xyz_q2.T

            q1_sqr = np.outer(norms_q1, np.ones(nvec_q2))
            q2_sqr = np.outer(np.ones(nvec_q1), norms_q2)

            # del norms_q1
            # del norms_q2


            q1q2_sqr = q1_sqr*q2_sqr

            psi_sqr = xyz_dot_xyz/q1q2_sqr
            # psi_sqr = xyz_dot_xyz/(q1_sqr*q2_sqr)


            I_sqr = np.outer(I_q1, I_q2)

            psi_sqr[np.where(psi_sqr < -1)] = -1
            psi_sqr[np.where(psi_sqr > 1)] = 1


            if not self.cos_sample:
                psi_sqr = np.arccos(psi_sqr)

            self.correlate_via_sum(q1_sqr, q2_sqr, psi_sqr, I_sqr, verbose=verbose-1)




    @verbose_dec
    def correlate_2D(self, q, t, I, verbose=0):
        """
        Correlate a set of 2D (q, theta) scattering peaks.

        For every pair of peaks, computes the pairwise q magnitudes and
        the (wrapped) angular separation, then sums the intensity
        products into ``self.vol`` via ``correlate_via_sum``.

        Parameters
        ----------
        q : numpy.ndarray
            Array of shape (nvec,) giving the q magnitude of each peak.
        t : numpy.ndarray
            Array of shape (nvec,) giving the angular (theta) position of
            each peak, in radians.
        I : numpy.ndarray
            Array of shape (nvec,) giving the intensity of each peak.
        verbose : int, optional
            Verbosity level for progress printing (default 0).

        Returns
        -------
        None
            ``self.vol`` is updated in place.
        """

        nvec = q.shape[0]


        q1_sqr = np.outer(q, np.ones(nvec))
        q2_sqr = np.outer(np.ones(nvec), q)

        t1_sqr = np.outer(t, np.ones(nvec))
        t2_sqr = np.outer(np.ones(nvec), t)
        psi_sqr = np.abs( (t1_sqr - t2_sqr + np.pi) % (np.pi*2) - np.pi)

        I_sqr = np.outer(I, I.T)

        if self.cos_sample:
            psi_sqr = np.cos(psi_sqr)
            psi_sqr[np.where(psi_sqr > 1)] = 1
            psi_sqr[np.where(psi_sqr < -1)] = -1

        self.correlate_via_sum(q1_sqr, q2_sqr, psi_sqr, I_sqr, verbose=verbose-1)







    @verbose_dec
    def correlate_via_sum(self, q1_sqr, q2_sqr, psi_sqr, I_sqr, verbose=0):
        """
        Bin pairwise correlation values and sum them into ``self.vol``.

        Splits each pairwise (square matrix) input into its strictly
        lower-triangular part and its diagonal, converts the q1, q2 and
        psi values into voxel indices, and sums the corresponding
        intensity products into the volume for both the off-diagonal
        (symmetric) and diagonal (self-correlation) contributions.

        Parameters
        ----------
        q1_sqr : numpy.ndarray
            Square matrix of q1 magnitudes for every pair of scattering
            vectors/peaks.
        q2_sqr : numpy.ndarray
            Square matrix of q2 magnitudes for every pair of scattering
            vectors/peaks.
        psi_sqr : numpy.ndarray
            Square matrix of angular (or cosine of angular) separations
            for every pair of scattering vectors/peaks.
        I_sqr : numpy.ndarray
            Square matrix of intensity products for every pair of
            scattering vectors/peaks.
        verbose : int, optional
            Verbosity level for progress printing (default 0).

        Returns
        -------
        None
            ``self.vol`` is updated in place.
        """
        q1_tri, q1_diag = convert_sqr2trianddiag(q1_sqr)
        q1_inds_tri = self.get_indices(q1_tri, axis=0)
        del q1_tri
        q1_inds_diag = self.get_indices(q1_diag, axis=0)
        del q1_diag

        q2_tri, q2_diag = convert_sqr2trianddiag(q2_sqr)
        q2_inds_tri = self.get_indices(q2_tri, axis=1)
        del q2_tri
        q2_inds_diag = self.get_indices(q2_diag, axis=1)
        del q2_diag

        psi_tri, psi_diag = convert_sqr2trianddiag(psi_sqr)
        psi_inds_tri = self.get_indices(psi_tri, axis=2)
        del psi_tri
        psi_inds_diag = self.get_indices(psi_diag, axis=2)
        del psi_diag

        I_tri, I_diag = convert_sqr2trianddiag(I_sqr)


        self.sum_into_vol(q1_inds_tri, q2_inds_tri, psi_inds_tri, I_tri, sym=True, verbose=verbose-1)
        self.sum_into_vol(q1_inds_diag, q2_inds_diag, psi_inds_diag, I_diag, sym=False, verbose=verbose-1)




def convert_sqr2trianddiag(sqr):
    """
    Split a square matrix into its strict lower triangle and diagonal.

    Parameters
    ----------
    sqr : numpy.ndarray
        Square 2D array to split.

    Returns
    -------
    tri_flat : numpy.ndarray
        1D array of the strictly lower-triangular (k=-1) elements of
        ``sqr``, flattened in row-major order.
    diag : numpy.ndarray
        1D array of the diagonal elements of ``sqr``.
    """

    tri_flat = np.tril(sqr, k=-1).flatten()
    loc = np.where(np.tril(np.ones(sqr.shape),k=-1).flatten() !=0)
    tri_flat = tri_flat[loc]
    diag = np.diag(sqr)

    return tri_flat, diag
