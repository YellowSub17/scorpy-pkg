
import numpy as np



from ...utils.convert_funcs import index_x_nowrap
from ...utils.decorator_funcs import verbose_dec
from ...utils.angle_between_funcs import *



class CorrelationVolCorr:



    @verbose_dec
    def correlate_scat_rect(self, qxyzi, verbose=0):

        #magnitudes of the scattering list
        qmags = np.linalg.norm(qxyzi[:,1:3], axis=1)

        print(f'Removing vectors q>{self.qmax}.')
        # only correlate less then qmax
        le_qmax = np.where(qmags <= self.qmax)[0]
        qxyzi = qxyzi[le_qmax]

        print(f'Removing vectors q<{self.qmin}.')
        # only correlate greater than qmin
        ge_qmin = np.where(qmags >= self.qmin)[0]
        qxyzi = qxyzi[ge_qmin]


        print(f'Removing vectors I<=0.')
        # only correlate intensity greater then 0
        Igt0_loc = np.where(qxyzi[:,-1]>0)[0]
        qxyzi = qxyzi[Igt0_loc]

        #number of vectors
        nvec = qxyzi.shape[0]
        print(f'Remaining vectors {nvec}.')

        xyz = qxyzi[:,1:3]
        I = qxyzi[:,-1]


        norms = np.linalg.norm(xyz, axis=1)
        xyz_dot_xyz = xyz@xyz.T

        q1_sqr = np.outer(norms, np.ones(nvec))
        q2_sqr = np.outer(np.ones(nvec), norms)
        psi_sqr = xyz_dot_xyz/(q1_sqr*q2_sqr)
        II_sqr = np.outer(I, I.T)

        if not self.cos_sample:
            psi_sqr = np.acos(psi_sqr)


        q1_flat = np.triu(q1_sqr, k=1).flatten()
        q2_flat = np.triu(q2_sqr, k=1).flatten()
        psi_flat= np.triu(psi_sqr, k=1).flatten()
        II_flat= np.triu(II_sqr, k=1).flatten()

        loc = np.where(q1_flat !=0)

        q1_flat = q1_flat[loc]
        q2_flat = q2_flat[loc]
        psi_flat = psi_flat[loc]
        II_flat = II_flat[loc]

        ite = np.ones(q1_flat.size)

        q1_inds = list(map(index_x_nowrap, q1_flat, self.qmin*ite, self.qmax*ite, self.nq*ite))
        q2_inds = list(map(index_x_nowrap, q2_flat, self.qmin*ite, self.qmax*ite, self.nq*ite))
        psi_inds = list(map(index_x_nowrap, psi_flat, self.zmin*ite, self.zmax*ite, self.npsi*ite))

        print(f'Filling q1 != q2')
        for q1_ind, q2_ind, psi_ind, inten in zip(q1_inds, q2_inds, psi_inds, II_flat):

            self.vol[q1_ind, q2_ind, psi_ind] += inten
            self.vol[q2_ind, q1_ind, psi_ind] += inten

        q1_diag = np.diag(q1_sqr)
        q2_diag = np.diag(q2_sqr)
        psi_diag = np.diag(psi_sqr)
        II_diag = np.diag(II_sqr)

        ite = np.ones(q1_diag.size)

        q1_inds = list(map(index_x_nowrap, q1_diag, self.qmin*ite, self.qmax*ite, self.nq*ite))
        q2_inds = list(map(index_x_nowrap, q2_diag, self.qmin*ite, self.qmax*ite, self.nq*ite))
        psi_inds = list(map(index_x_nowrap, psi_diag, self.zmin*ite, self.zmax*ite, self.npsi*ite))

        print(f'Filling q1 = q2')
        for q1_ind, q2_ind, psi_ind, inten in zip(q1_inds, q2_inds, psi_inds, II_flat):
            self.vol[q1_ind, q2_ind, psi_ind] += inten











    # @verbose_dec
    # def correlate_scat_rect(self, qxyzi, verbose=0):
        # '''
        # scorpy.CorrelationVol.correlate_scat_pol():
            # Correlate diffraction peaks in 3D rectilinear coordinates.
        # Arguments:
            # qxyzi : numpy.ndarray
                # n by 4 array of n peaks to correlate. First 3 columns of array
                # should be the reciprocal space coordinates of peaks (qx,qy,qz),
                # and the last coloumn should be the intensity of the peak.
        # '''
        # qmags = np.linalg.norm(qxyzi[:, :3], axis=1)
        # # only correlate less than qmax
        # le_qmax = np.where(qmags <= self.qmax)[0]
        # qxyzi = qxyzi[le_qmax]
        # qmags = qmags[le_qmax]

        # # only correlate greater than qmin
        # ge_qmin = np.where(qmags >= self.qmin)[0]
        # qxyzi = qxyzi[ge_qmin]
        # qmags = qmags[ge_qmin]


        # # only correlate intensity greater then 0
        # Igt0_loc = np.where(qxyzi[:,-1]>0)[0]
        # qxyzi = qxyzi[Igt0_loc]
        # qmags = qmags[Igt0_loc]

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





    @verbose_dec
    def correlate_scat_pol(self, qti, verbose=0 ):
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
        le_qmax_loc = np.where(qti[:, 0] <= self.qmax)[0]
        qti = qti[le_qmax_loc]

        # only correlate more than qmin
        ge_qmin_loc = np.where(qti[:, 0] >= self.qmin)[0]
        qti = qti[ge_qmin_loc]

        # only correlate intensity greater then 0
        Igt0_loc = np.where(qti[:,-1]>0)
        qti = qti[Igt0_loc]


        # calculate q indices of every scattering vector
        nscats = qti.shape[0]


        ite = np.ones(nscats)
        q_inds = list(map(index_x_nowrap, qti[:, 0], self.qmin * ite, self.qmax * ite, self.nq * ite))


        angle_between_fn = angle_between_pol_cos if self.cos_sample else angle_between_pol



        for i, q1 in enumerate(qti):
            print(f'Peak: {i+1}/{nscats}')
            q1_ind = q_inds[i]

            for j, q2 in enumerate(qti[i:]):
                # get q index
                q2_ind = q_inds[i + j]

                # get the angle between vectors
                psi = angle_between_fn(q1[1], q2[1])

                #calculate psi index for angle between vectors
                psi_ind = index_x_nowrap(psi, self.zmin, self.zmax, self.npsi)

                # fill the volume
                self.vol[q1_ind, q2_ind, psi_ind] += q1[-1] * q2[-1]
                if j > 0:  # if not on diagonal
                    self.vol[q2_ind, q1_ind, psi_ind] += q1[-1] * q2[-1]




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

        # only correlate greater than qmin
        ge_qmin = np.where(qtpi[:, 0] >= self.qmin)[0]
        qtpi = qtpi[ge_qmin]

        # only correlate intensity greater then 0
        Igt0_loc = np.where(qtpi[:,-1]>0)[0]
        qtpi = qtpi[Igt0_loc]


        nscats = qtpi.shape[0]


        # calculate q indices of every scattering vector 
        ite = np.ones(nscats)
        q_inds = list(map(index_x_nowrap, qtpi[:, 0], self.qmin * ite, self.qmax * ite, self.nq * ite))


        angle_between_fn = angle_between_sph_cos if self.cos_sample else angle_between_sph



        for i, q1 in enumerate(qtpi):

            print(f'Peak: {i+1}/{nscats}', end='\r')
            # get q index, theta and phi
            q1_ind = q_inds[i]
            theta1 = q1[1]
            phi1 = q1[2]

            for j, q2 in enumerate(qtpi[i:]):

                # get q index, theta and phi
                q2_ind = q_inds[i + j]
                theta2 = q2[1]
                phi2 = q2[2]

                # get the angle between angluar coordinates
                psi = angle_between_fn(theta1, theta2, phi1, phi2)


                #calculate psi index for angle between vectors
                psi_ind = index_x_nowrap(psi, self.zmin, self.zmax, self.npsi)

                # fill the volume
                self.vol[q1_ind, q2_ind, psi_ind] += q1[-1] * q2[-1]

                if j > 0:  # if not on diagonal
                    self.vol[q2_ind, q1_ind, psi_ind] += q1[-1] * q2[-1]





    @verbose_dec
    def correlate_convolve(self, qt, verbose=0):

        f_qt = np.fft.fft(qt, axis=1)
        print(f_qt.shape)

        for i, f_qtrowi in enumerate(f_qt):
            for j, f_qtrowj in enumerate(f_qt[i:]):

                convolved_rows = f_qtrowi*f_qtrowj.conjugate()

                self.vol[i, j+i,:] += np.real(convolved_rows)
                if j >0:
                    self.vol[j+i, i,:] += np.real(convolved_rows)




