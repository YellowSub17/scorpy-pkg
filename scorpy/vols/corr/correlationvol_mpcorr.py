
import numpy as np

from multiprocessing import Process

from multiprocessing.managers import SharedMemoryManager

from multiprocessing.shared_memory import SharedMemory




from ...utils.convert_funcs import index_x_nowrap
from ...utils.decorator_funcs import verbose_dec
from ...utils.angle_between_funcs import *



def create_np_array_from_shared_mem(shared_mem, shared_data_type, shared_data_shape):
    arr = np.frombuffer(shared_mem.buf, dtype=shared_data_dtype)
    arr = arr.reshape(shared_data_shape)
    return arr



# def child_process(shared_mem, shared_data_type, shared_data_type):
    # pass



class CorrelationVolMPCorr:

    @verbose_dec
    def correlate_scat_rect_mp(self, qxyzi, nprocs=4, verbose=0):
        '''
        scorpy.CorrelationVol.correlate_scat_pol():
            Correlate diffraction peaks in 3D rectilinear coordinates.
        Arguments:
            qxyzi : numpy.ndarray
                n by 4 array of n peaks to correlate. First 3 columns of array
                should be the reciprocal space coordinates of peaks (qx,qy,qz),
                and the last coloumn should be the intensity of the peak.
        '''
        print('xoxoxoxo scatrectmp')
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

        # calculate q indices of every scattering vector
        ite = np.ones(nscats)
        q_inds = list(map(index_x_nowrap, qmags, self.qmin * ite, self.qmax * ite, self.nq * ite))

        angle_between_fn = angle_between_rect_cos_x if self.cos_sample else angle_between_rect_x


        # procs_chunks= nscat/nprocs






        for i, q1 in enumerate(qxyzi):
            print(f'Peak: {i+1}/{nscats}', end='\r')

            # get q index
            q1_ind = q_inds[i]

            for j, q2 in enumerate(qxyzi[i:]):
                # get q index
                q2_ind = q_inds[i + j]

                # get the angle between vectors
                psi = angle_between_fn(q1[0], q1[1], q1[2], q2[0], q2[1], q2[2])

                #calculate psi index for angle between vectors
                psi_ind = index_x_nowrap(psi, self.zmin, self.zmax, self.npsi)

                # fill the volume
                self.vol[q1_ind, q2_ind, psi_ind] += q1[-1] * q2[-1]
                if j > 0:  # if not on diagonal
                    self.vol[q2_ind, q1_ind, psi_ind] += q1[-1] * q2[-1]





