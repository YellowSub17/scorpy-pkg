
import numpy as np



from ...utils.utils import angle_between_pol, angle_between_sph, angle_between_rect, index_x, verbose_dec

class CorrelationVolCorr:


    @verbose_dec
    def correlate_convolve(self, qt, verbose=0):

        f_qt = np.fft.fft(qt, axis=1)
        print(f_qt.shape)

        for i, f_qtrowi in enumerate(f_qt):
            for j, f_qtrowj in enumerate(f_qt[i:]):

                convolved_rows = f_qtrowi*f_qtrowj.conjugate()
                ###todo add inverse fft


                self.vol[i, j+i,:] += np.real(convolved_rows)
                if j >0:
                    self.vol[j+i, i,:] += np.real(convolved_rows)




    @verbose_dec
    def correlate_scat_pol(self, qti,chopf=0, verbose=0 ):
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



#  DEBUG
        nscats = nscats - int(chopf*nscats)
        np.random.shuffle(qti)
        qti = qti[:nscats]



        ite = np.ones(nscats)
        q_inds = list(map(index_x, qti[:, 0], self.qmin * ite, self.qmax * ite, self.nq * ite))




        for i, q1 in enumerate(qti):
            print(f'Peak: {i+1}/{nscats}')
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



    @verbose_dec
    def correlate_scat_rect(self, qxyzi, chopf=0, verbose=0):
        '''
        scorpy.CorrelationVol.correlate_scat_pol():
            Correlate diffraction peaks in 3D rectilinear coordinates.
        Arguments:
            qxyzi : numpy.ndarray
                n by 4 array of n peaks to correlate. First 3 columns of array
                should be the reciprocal space coordinates of peaks (qx,qy,qz),
                and the last coloumn should be the intensity of the peak.
        '''
        qmags = np.linalg.norm(qxyzi[:, :3], axis=1)
        # only correlate less than qmax
        le_qmax = np.where(qmags <= self.qmax)[0]
        qxyzi = qxyzi[le_qmax]
        qmags = qmags[le_qmax]

        # only correlate greater than qmin
        ge_qmin = np.where(qmags >= self.qmin)[0]
        qxyzi = qxyzi[ge_qmin]
        qmags = qmags[ge_qmin]


        
        # only correlate intensity greater then 0
        Igt0_loc = np.where(qxyzi[:,-1]>0)[0]
        qxyzi = qxyzi[Igt0_loc]
        qmags = qmags[Igt0_loc]


        nscats = qxyzi.shape[0]

#  DEBUG
        nscats = nscats - int(chopf*nscats)
        np.random.shuffle(qxyzi)
        qxyzi = qxyzi[:nscats]

        # calculate q indices of every scattering vector
        ite = np.ones(nscats)
        q_inds = list(map(index_x, qmags, self.qmin * ite, self.qmax * ite, self.nq * ite))


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

##  DEBUG
        # nscats_chop = int((1-chopf)*nscats)
        # np.random.shuffle(qtpi)
        # qtpi = qtpi[:nscats_chop]
        # nscats = nscats_chop

        # calculate q indices of every scattering vector 
        ite = np.ones(nscats)
        q_inds = list(map(index_x, qtpi[:, 0], self.qmin * ite, self.qmax * ite, self.nq * ite))




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





