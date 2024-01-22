
import numpy as np



from ...utils.convert_funcs import index_x_nowrap, convert_sqr2trianddiag
from ...utils.decorator_funcs import verbose_dec



class CorrelationVolCorr:

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


    # @verbose_dec
    # def sum_into_vol(self, q1_inds, q2_inds, psi_inds, IIs, sym=False, verbose=0):

        # npts = len(q1_inds)
        # for i, (q1_ind, q2_ind, psi_ind, II) in enumerate(zip(q1_inds, q2_inds, psi_inds, IIs)):
            # # print(f'{i}/{npts}', end='\r')
            # self.vol[q1_ind, q2_ind, psi_ind] += II
            # if sym:
                # self.vol[q2_ind, q1_ind, psi_ind] += II



    # def get_correlation_indices(self, q1_pts, q2_pts, psi_pts):

        # ite = np.ones(q1_pts.size)

        # q1_inds = list(map(index_x_nowrap, q1_pts, self.qmin*ite, self.qmax*ite, self.nq*ite))
        # q2_inds = list(map(index_x_nowrap, q2_pts, self.qmin*ite, self.qmax*ite, self.nq*ite))
        # psi_inds = list(map(index_x_nowrap, psi_pts, self.zmin*ite, self.zmax*ite, self.npsi*ite))

        # return q1_inds, q2_inds, psi_inds












    # @verbose_dec
    # def correlate_scat_rect(self, qxyzi, verbose=0):
        # qmags = np.linalg.norm(qxyzi[:, :3], axis=1)
# #         # only correlate less than qmax
        # # le_qmax = np.where(qmags <= self.qmax)[0]
        # # qxyzi = qxyzi[le_qmax]
        # # qmags = qmags[le_qmax]

        # # # only correlate greater than qmin
        # # ge_qmin = np.where(qmags >= self.qmin)[0]
        # # qxyzi = qxyzi[ge_qmin]
        # # qmags = qmags[ge_qmin]


        # # # only correlate intensity greater then 0
        # # Igt0_loc = np.where(qxyzi[:,-1]>0)[0]
        # # qxyzi = qxyzi[Igt0_loc]
        # # qmags = qmags[Igt0_loc]

        # nscats = qxyzi.shape[0]

        # # calculate q indices of every scattering vector
        # ite = np.ones(nscats)
        # q_inds = list(map(index_x_nowrap, qmags, self.qmin * ite, self.qmax * ite, self.nq * ite))

        # angle_between_fn = angle_between_rect_cos if self.cos_sample else angle_between_rect




        # for i, q1 in enumerate(qxyzi):
            # print(f'Peak: {i+1}/{nscats}', end='\r')

            # # get q index
            # q1_ind = q_inds[i]

            # for j, q2 in enumerate(qxyzi[i:]):
                # # get q index
                # q2_ind = q_inds[i + j]

                # # get the angle between vectors
                # psi = angle_between_fn(q1[:3], q2[:3])

                # #calculate psi index for angle between vectors
                # psi_ind = index_x_nowrap(psi, self.zmin, self.zmax, self.npsi)

                # # fill the volume
                # self.vol[q1_ind, q2_ind, psi_ind] += q1[-1] * q2[-1]
                # if j > 0:  # if not on diagonal
                    # self.vol[q2_ind, q1_ind, psi_ind] += q1[-1] * q2[-1]





    # @verbose_dec
    # def correlate_scat_pol(self, qti, verbose=0 ):


        # # only correlate less than qmax
        # le_qmax_loc = np.where(qti[:, 0] <= self.qmax)[0]
        # qti = qti[le_qmax_loc]

        # # only correlate more than qmin
        # ge_qmin_loc = np.where(qti[:, 0] >= self.qmin)[0]
        # qti = qti[ge_qmin_loc]

        # # only correlate intensity greater then 0
        # Igt0_loc = np.where(qti[:,-1]>0)
        # qti = qti[Igt0_loc]


        # # calculate q indices of every scattering vector
        # nscats = qti.shape[0]


        # ite = np.ones(nscats)
        # q_inds = list(map(index_x_nowrap, qti[:, 0], self.qmin * ite, self.qmax * ite, self.nq * ite))


        # angle_between_fn = angle_between_pol_cos if self.cos_sample else angle_between_pol



        # for i, q1 in enumerate(qti):
            # print(f'Peak: {i+1}/{nscats}')
            # q1_ind = q_inds[i]

            # for j, q2 in enumerate(qti[i:]):
                # # get q index
                # q2_ind = q_inds[i + j]

                # # get the angle between vectors
                # psi = angle_between_fn(q1[1], q2[1])

                # #calculate psi index for angle between vectors
                # psi_ind = index_x_nowrap(psi, self.zmin, self.zmax, self.npsi)

                # # fill the volume
                # self.vol[q1_ind, q2_ind, psi_ind] += q1[-1] * q2[-1]
                # if j > 0:  # if not on diagonal
                    # self.vol[q2_ind, q1_ind, psi_ind] += q1[-1] * q2[-1]




    # @verbose_dec
    # def correlate_scat_sph(self, qtpi, verbose=0):
        # '''
        # scorpy.CorrelationVol.correlate_scat_sph():
            # Correlate diffraction peaks in 3D spherical coordinates.
        # Arguments:
            # qtpi : numpy.ndarray
                # n by 4 array of n peaks to correlate. Columns of the array should
                # be the spherical radius of the peak (A-1), polar angle of the peak
                # (theta, radians), and the azimuthial angle of the peak (phi, radians).
        # '''
        # # only correlate less than qmax
        # le_qmax = np.where(qtpi[:, 0] <= self.qmax)[0]
        # qtpi = qtpi[le_qmax]

        # # only correlate greater than qmin
        # ge_qmin = np.where(qtpi[:, 0] >= self.qmin)[0]
        # qtpi = qtpi[ge_qmin]

        # # only correlate intensity greater then 0
        # Igt0_loc = np.where(qtpi[:,-1]>0)[0]
        # qtpi = qtpi[Igt0_loc]


        # nscats = qtpi.shape[0]


        # # calculate q indices of every scattering vector 
        # ite = np.ones(nscats)
        # q_inds = list(map(index_x_nowrap, qtpi[:, 0], self.qmin * ite, self.qmax * ite, self.nq * ite))


        # angle_between_fn = angle_between_sph_cos if self.cos_sample else angle_between_sph



        # for i, q1 in enumerate(qtpi):

            # print(f'Peak: {i+1}/{nscats}', end='\r')
            # # get q index, theta and phi
            # q1_ind = q_inds[i]
            # theta1 = q1[1]
            # phi1 = q1[2]

            # for j, q2 in enumerate(qtpi[i:]):

                # # get q index, theta and phi
                # q2_ind = q_inds[i + j]
                # theta2 = q2[1]
                # phi2 = q2[2]

                # # get the angle between angluar coordinates
                # psi = angle_between_fn(theta1, theta2, phi1, phi2)


                # #calculate psi index for angle between vectors
                # psi_ind = index_x_nowrap(psi, self.zmin, self.zmax, self.npsi)

                # # fill the volume
                # self.vol[q1_ind, q2_ind, psi_ind] += q1[-1] * q2[-1]

                # if j > 0:  # if not on diagonal
                    # self.vol[q2_ind, q1_ind, psi_ind] += q1[-1] * q2[-1]





    # @verbose_dec
    # def correlate_convolve(self, qt, verbose=0):

        # f_qt = np.fft.fft(qt, axis=1)
        # print(f_qt.shape)

        # for i, f_qtrowi in enumerate(f_qt):
            # for j, f_qtrowj in enumerate(f_qt[i:]):

                # convolved_rows = f_qtrowi*f_qtrowj.conjugate()

                # self.vol[i, j+i,:] += np.real(convolved_rows)
                # if j >0:
                    # self.vol[j+i, i,:] += np.real(convolved_rows)




    # @verbose_dec
    # def correlate_3D(self, xyz, I, verbose=0):

        # print(f'Not chunking.')

        # nvec = xyz.shape[0]

        # norms = np.linalg.norm(xyz, axis=1)
        # xyz_dot_xyz = xyz@xyz.T


        # q1_sqr = np.outer(norms, np.ones(nvec))
        # q2_sqr = np.outer(np.ones(nvec), norms)
        # psi_sqr = xyz_dot_xyz/(q1_sqr*q2_sqr)
        # I_sqr = np.outer(I, I.T)


        # psi_sqr[np.where(psi_sqr < -1)] = -1
        # psi_sqr[np.where(psi_sqr > 1)] = 1


        # if not self.cos_sample:
            # psi_sqr = np.arccos(psi_sqr)


        # self.correlate_via_sum(q1_sqr, q2_sqr, psi_sqr, I_sqr, verbose=verbose-1)


