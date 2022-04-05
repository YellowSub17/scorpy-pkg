
import numpy as np



from ...utils.utils import angle_between_pol, angle_between_sph, angle_between_rect, index_x, verbose_dec

class CorrelationVolCorr:


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
        le_qmax_loc = np.where(qti[:, 0] <= self.qmax)[0]
        qti = qti[le_qmax_loc]

        # only correlate intensity greater then 0
        Igt0_loc = np.where(qti[:,-1]>0)
        qti = qti[Igt0_loc]


        nscats = qti.shape[0]
        # calculate q indices of every scattering vector
        ite = np.ones(nscats)
        q_inds = list(map(index_x, qti[:, 0], 0 * ite, self.qmax * ite, self.nq * ite))




        for i, q1 in enumerate(qti):
            print(f'Peak: {i+1}/{nscats}', end='\r')
            # get q index
            q1_ind = q_inds[i]


            for j, q2 in enumerate(qti[i:]):
                # get q index
                q2_ind = q_inds[i + j]

                # get the angle between vectors
                psi = angle_between_pol(q1[1], q2[1])
                if self.cos_sample:
                    psi = np.cos(psi)

                #calculate psi index for angle between vectors
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
        
        # only correlate intensity greater then 0
        Igt0_loc = np.where(qxyzi[:,-1]>0)[0]
        qxyzi = qxyzi[Igt0_loc]
        qmags = qmags[Igt0_loc]


        nscats = qxyzi.shape[0]

        # calculate q indices of every scattering vector
        ite = np.ones(nscats)
        q_inds = list(map(index_x, qmags, 0 * ite, self.qmax * ite, self.nq * ite))


        for i, q1 in enumerate(qxyzi):
            print(f'Peak: {i+1}/{nscats}', end='\r')

            # get q index
            q1_ind = q_inds[i]

            for j, q2 in enumerate(qxyzi[i:]):
                # get q index
                q2_ind = q_inds[i + j]

                # get the angle between vectors
                psi = angle_between_rect(q1[:3], q2[:3])

                if self.cos_sample:
                    psi = np.cos(psi)

                #calculate psi index for angle between vectors
                psi_ind = index_x(psi, self.zmin, self.zmax, self.npsi, wrap=self.zwrap)

                # fill the volume
                self.vol[q1_ind, q2_ind, psi_ind] += q1[-1] * q2[-1]
                if j > 0:  # if not on diagonal
                    self.vol[q2_ind, q1_ind, psi_ind] += q1[-1] * q2[-1]

        # print('\x1b[2K', end='\r')




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

        # only correlate intensity greater then 0
        Igt0_loc = np.where(qtpi[:,-1]>0)[0]
        qtpi = qtpi[Igt0_loc]


        nscats = qtpi.shape[0]
        # calculate q indices of every scattering vector 
        ite = np.ones(nscats)
        q_inds = list(map(index_x, qtpi[:, 0], 0 * ite, self.qmax * ite, self.nq * ite))




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
                psi = angle_between_sph(theta1, theta2, phi1, phi2)

                if self.cos_sample:
                    psi = np.cos(psi)

                #calculate psi index for angle between vectors
                psi_ind = index_x(psi, self.zmin, self.zmax, self.npsi, wrap=self.zwrap)

                # fill the volume
                self.vol[q1_ind, q2_ind, psi_ind] += q1[-1] * q2[-1]

                if j > 0:  # if not on diagonal
                    self.vol[q2_ind, q1_ind, psi_ind] += q1[-1] * q2[-1]
        # print('\x1b[2K', end='\r')



    def correlate_fft_pol(self, polar):

        fpolar = np.fft.fft( polar, axis=1 )

        out = np.zeros( (polar.shape[0],polar.shape[0],polar.shape[1]), np.complex128)

        for i, fp_rowi in enumerate(fpolar):
            for j, fp_rowj in enumerate(fpolar):
                out[i,j,:] = fp_rowi*fp_rowj.conjugate()


        out = np.real(np.fft.ifft( out, axis=2 ))

        return out




