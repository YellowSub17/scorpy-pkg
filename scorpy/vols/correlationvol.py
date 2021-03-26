from ..utils import index_x, angle_between, polar_angle_between

from .vol import Vol
import numpy as np


class CorrelationVol(Vol):
    '''
    Representation of a scattering correlation volume.

    Arguments:
        nq (int): number of scattering magnitude bins.
        ntheta (int): number of angular bins.
        qmax (float): correlation magnitude limit [1/A].
        path (str): path to dbin (and log) if being created from memory.
    '''

    def __init__(self, nq=100, ntheta=180, qmax=1,  path=None):
        '''
        Class constructor.
        '''
        Vol.__init__(self, nq,nq,ntheta, qmax, qmax, 180, comp=False, path=path)

        self.plot_q1q2 = self.plot_xy
        # self._ymax = self.xmax
        # self._qmax = self.xmax

        # self._ny = self.nx
        # self._nq = self.nx

        # self._ntheta = self.nz
        # self._cvol = self.vol


    @property
    def qmax(self):
        return self._xmax

    @property
    def nq(self):
        return self._nx

    @property
    def ntheta(self):
        return self._nz

    @property
    def cvol(self):
        return self._vol



    # @cvol.setter
    # def cvol(self, new_cvol):
        # print('setting new cvol')
        # self._vol = new_cvol

    # @vol.setter
    # def vol(self, new_vol):
        # assert new_vol.shape == self.vol.shape, 'Cannot replace vols with different shapes'
        # self._vol = new_vol







    def correlate2D(self,qti):
        '''
        Correlate 2D diffraction pattern peaks.

        Arguments:
            qti (n x 3 array): list of peaks to correlate. Columns should be
                                qti[:,0] = polar radius of peak
                                qti[:,1] = polar angle of peak
                                qti[:,2] = intensity of peak
        Returns:
            None. Updates self.cvol with correlations.
        '''
        less_than_qmax = np.where(qti[:,0] <= self.qmax)[0]      #only correlate less or equal the qmax
        qti = qti[less_than_qmax]

        for i, q in enumerate(qti):
            q_ind = index_x(q[0],self.qmax, self.nq)
            for q_prime in qti[i+1:]:
                q_prime_ind = index_x(q_prime[0],self.qmax, self.nq)
                theta = polar_angle_between(q[1], q_prime[1])
                theta_ind = index_x(theta, 180, self.ntheta)
                self.vol[q_ind,q_prime_ind,theta_ind] +=q[-1]*q_prime[-1]
                self.vol[q_prime_ind,q_ind,theta_ind] +=q[-1]*q_prime[-1]



    def correlate3D(self,qxyzi):
        '''
        Correlate 3D diffraction pattern peaks.

        Arguments:
            qxyzi (n x 4 array): list of peaks to correlate. Columns should be
                                qti[:,0] = qx coordinate of scattering vector
                                qti[:,1] = qy coordinate of scattering vector
                                qti[:,2] = qz coordinate of scattering vector
                                qti[:,3] = intensity of peak
        Returns:
            None. Updates self.cvol with correlations.
        '''
        # print('Correlating 3D')

        # calculate magnitude of vectors, only correlate less than qmax
        qmags = np.linalg.norm(qxyzi[:,:3], axis=1)
        # print(qmags)
        correl_vec_indices = np.where(qmags <= self.qmax)[0]
        qxyzi = qxyzi[correl_vec_indices]
        qmags = qmags[correl_vec_indices]
        # print(qxyzi)

        # q1 scattering
        for i, q in enumerate(qxyzi):
            # print(f'Correlating: {i}/{len(qmags)}')

            q_mag =  qmags[i]
            q_ind = index_x(q_mag,self.qmax, self.nq)

            # q2 scattering

            for j, q_prime in enumerate(qxyzi[i:]):
                q_prime_mag =  qmags[i+j]

                q_prime_ind = index_x(q_prime_mag,self.qmax, self.nq)

                theta = angle_between(q[:3]/q_mag, q_prime[:3]/q_prime_mag)

                theta_ind = index_x(theta, np.pi, self.ntheta)

                self.vol[q_ind,q_prime_ind,theta_ind] +=q[-1]*q_prime[-1]

                if j>0:
                    self.vol[q_prime_ind,q_ind,theta_ind] +=q[-1]*q_prime[-1]



    def correlate(self,c):
        if c.shape[1]==3:
            self.correlate2D(c)
        elif c.shape[1]==4:
            self.correlate3D(c)
        else:
            print('Incorrect format of scattering vectors. See documentation')


    # def sub_qmean(self,iv):
        # qmean = np.mean(iv.ivol, axis=1)
        # return qmean




