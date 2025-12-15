
import numpy as np



from ...utils.convert_funcs import index_x_nowrap, convert_sqr2trianddiag
from ...utils.decorator_funcs import verbose_dec



class CorrelationVolCorr:


    def correlate_convolve(self, qt):
        f_qt = np.fft.fft(qt, axis=1)
        for i, f_qtrowi in enumerate(f_qt):
            for j, f_qtrowj in enumerate(f_qt[i:]):

                convolved_rows = np.fft.ifft(f_qtrowi*f_qtrowj.conjugate(), axis=0)
                self.vol[i, j+i, :] += np.real(convolved_rows)
                if j>0:
                    self.vol[j+i, i, : ] += np.real(convolved_rows)




    @verbose_dec
    def correlate_3D(self, xyz, I, nchunks=1, verbose=0):

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



    def correlate_via_histdd(self, q1_sqr, q2_sqr, psi_sqr, I_sqr, verbose=0):



        q1q2psi_coords = np.array( [q1_sqr.flatten(), q2_sqr.flatten(), psi_sqr.flatten()]).T


        corr, edges = np.histogramdd(q1q2psi_coords,
                                    bins = (self.nq, self.nq, self.npsi),
                                    range =[ (self.qmin, self.qmax),
                                             (self.qmin, self.qmax),
                                             (self.zmin, self.zmax)],
                                    weights = I_sqr.flatten())
        self.vol += corr

