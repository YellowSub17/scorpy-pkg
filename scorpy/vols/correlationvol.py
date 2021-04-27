from ..utils import  angle_between_pol, angle_between_sph, \
                        angle_between_rect, index_x

from .vol import Vol
from scipy import special
import numpy as np
import math

from .propertymixins import CorrelationVolProps


class CorrelationVol(Vol, CorrelationVolProps):
    '''
    Representation of a scattering correlation volume.

    Arguments:
        nq (int): number of scattering magnitude bins.
        ntheta (int): number of angular bins.
        qmax (float): correlation magnitude limit [1/A].
        path (str): path to dbin (and log) if being created from memory.
    '''

    def __init__(self, nq = 100, npsi = 180, qmax = 1, \
                 path = None):
        '''
        Class constructor.
        '''
        Vol.__init__(self,  nq, nq, npsi, \
                            qmax, qmax, 180, \
                            0, 0, 0, \
                            comp = False, path = path)

        self.plot_q1q2 = self.plot_xy


    def _save_extra(self, f):
        f.write('[corr]\n')
        f.write(f'qmax = {self.qmax}\n')
        f.write(f'psimax = {180}\n')
        f.write(f'nq = {self.nq}\n')
        f.write(f'npsi = {self.npsi}\n')
        f.write(f'dq = {self.dq}\n')
        f.write(f'dpsi = {self.dpsi}\n')



    def fill_from_cif(self,cif, cords='scat_sph'):

        if cords=='scat_sph':
            self.correlate_scat_sph(cif.scat_sph)
        if cords=='scat_rect':
            self.correlate_scat_rect(cif.scat_rect)


    def fill_from_peakdata(self,peakdata):
        '''
        Fill the CorrelationVol from a BlqqVol

        Arguments:
            blqq (BlqqVol): The BlqqVol object to to fill the CorrelationVol

        Returns:
            None. Updates self.cvol
        '''
        if peakdata.frame_numbers.size >1:
            frames = peakdata.split_frames()
        else:
            frames = [peakdata]

        for frame in frames:
            self.correlate_scat_pol(frame.scat_pol)



    def fill_from_blqq(self, blqq):
        '''
        Fill the CorrelationVol from a BlqqVol

        Arguments:
            blqq (BlqqVol): The BlqqVol object to to fill the CorrelationVol

        Returns:
            None. Updates self.cvol
        '''

        #arguments for the legendre polynomial
        args = np.cos( np.linspace(0, np.pi, self.npsi))

        # initialze fmat matrix
        fmat = np.zeros( (self.npsi, blqq.nl) )

        #for every even spherical harmonic
        for l in range(0, blqq.nl, 2):

            leg_vals = (1/(4*np.pi))*special.eval_legendre(l, args)
            fmat[:,l] = leg_vals


        #for every q1 position
        for q1 in range(self.nq):
            #for every q2 position
            for q2 in range(q1, self.nq):

                #vector as a function of L
                blv = blqq.vol[q1,q2,:]
                for t1 in range(self.npsi):
                    ft = fmat[t1,:]
                    x = np.dot(blv,ft)
                    self.vol[q1,q2,t1] = x
                    if q1!=q2:
                        self.vol[q2,q1,t1] = x








    def correlate_scat_pol(self,qti):
        '''
        Correlate diffraction peaks in 2D polar coordinates.

        Arguments:
            qti (n x 3 array): list of peaks to correlate. Columns should be
                                qti[:,0] = polar radius of peak
                                qti[:,1] = polar angle of peak
                                qti[:,2] = intensity of peak
        Returns:
            None. Updates self.cvol with correlations.
        '''
        le_qmax = np.where(qti[:,0] <= self.qmax)[0]
        qti = qti[le_qmax]

        ite = np.ones(qti.shape[0])
        q_inds =list(map(index_x, qti[:,0], 0*ite, self.qmax*ite, self.nq*ite))

        for i, q1 in enumerate(qti):
            q1_ind = q_inds[i]

            for j, q2 in enumerate(qti[i:]):
                q2_ind = q_inds[i+j]

                psi = angle_between_pol(q1[1], q2[1])
                psi_ind = index_x(psi, 0, 180, self.npsi)

                self.vol[q1_ind, q2_ind, psi_ind] +=q1[-1]*q2[-1]
                if j>0:
                    self.vol[q2_ind, q1_ind, psi_ind] +=q1[-1]*q2[-1]




    def correlate_scat_rect(self,qxyzi):
        '''
        Correlate diffraction peaks in 3D rectilinear coordinates.

        Arguments:
            qxyzi (n x 4 array): list of peaks to correlate. Columns should be
                                qti[:,0] = qx coordinate of scattering vector
                                qti[:,1] = qy coordinate of scattering vector
                                qti[:,2] = qz coordinate of scattering vector
                                qti[:,3] = intensity of peak
        Returns:
            None. Updates self.cvol with correlations
        '''
        qmags = np.linalg.norm(qxyzi[:,:3], axis=1)
        le_qmax = np.where(qmags <= self.qmax)[0]
        qxyzi = qxyzi[le_qmax]
        qmags = qmags[le_qmax]

        ite = np.ones(qxyzi.shape[0])
        q_inds =list(map(index_x, qmags, 0*ite, self.qmax*ite, self.nq*ite))

        for i, q1 in enumerate(qxyzi):
            q1_ind = q_inds[i]

            for j, q2 in enumerate(qxyzi[i:]):
                q2_ind = q_inds[i+j]

                psi = angle_between_rect(q1[:3], q2[:3])
                psi_ind = index_x(psi, 0, np.pi, self.npsi)

                self.vol[q1_ind,q2_ind,psi_ind] +=q1[-1]*q2[-1]
                if j>0:
                    self.vol[q2_ind, q1_ind, psi_ind] += q1[-1]*q2[-1]







    def correlate_scat_sph(self, qtpi):
        '''
        Correlate diffraction peaks in 3D spherical coordinates.

        Arguments:
            qxyzi (n x 4 array): list of peaks to correlate. Columns should be
                                qti[:,0] = qx coordinate of scattering vector
                                qti[:,1] = qy coordinate of scattering vector
                                qti[:,2] = qz coordinate of scattering vector
                                qti[:,3] = intensity of peak
        Returns:
            None. Updates self.cvol with correlations
        '''
        le_qmax = np.where(qtpi[:,0] <= self.qmax)[0]
        qtpi = qtpi[le_qmax]

        ite = np.ones(qtpi.shape[0])
        q_inds =list(map(index_x, qtpi[:,0], 0*ite, self.qmax*ite, self.nq*ite))

        for i, q1 in enumerate(qtpi):
            q1_ind = q_inds[i]
            theta1 = q1[1]
            phi1 = q1[2]

            for j, q2 in enumerate(qtpi[i:]):
                q2_ind = q_inds[i+j]
                theta2 = q2[1]
                phi2 = q2[2]

                psi = angle_between_sph(theta1, theta2,phi1, phi2)
                psi_ind = index_x(psi,0, np.pi, self.npsi)

                self.vol[q1_ind, q2_ind, psi_ind] +=q1[-1]*q2[-1]
                if j>0:
                    self.vol[q2_ind, q2_ind, psi_ind] +=q1[-1]*q2[-1]


