
from .Vol import Vol

class CorrelationVol(Vol):

    def __init__(self, nq=256, ntheta=360, qmax=1, fromfile=False, path=None):
        Vol.__init__(self, nq,nq,ntheta, qmax, qmax, 180, fromfile=fromfile, path=path)

        self.plot_q1q2 = self.plot_xy






    def correlate(self, qti):
        '''
        correlate a list vectors qti = [ [q_mag,theta, inten.],...]
        double for loop implemented so  vectors are not correlated with self
        and uses C(q1,q2,t)=C(q2,q1,t)
        '''

        #correlating 2D diffraction patterns (|q|, theta, intensity)
        if qti.shape[1] == 3:
            # print('Correlating 2D diffraction pattern...')
            less_than_qmax = np.where(qti[:,0] < self.qmax)[0]      #only correlate less the qmax
            qti = qti[less_than_qmax]
            #for every vector
            for i, q in enumerate(qti):

                q_ind = index_x(q[0],self.qmax, self.nq)

                #start q_prime counting ahead of q (i+1)
                for q_prime in qti[i+1:]:
                    q_prime_ind = index_x(q_prime[0],self.qmax, self.nq)
                    theta = polar_angle_between(q[1], q_prime[1])
                    theta_ind = index_x(theta, 180, self.ntheta)

                    # add values to the corrlation and histograms
                    # in (q1,q2,t) and (q2,q1,t) positions
                    if self.hflag:
                        self.cvol[q_ind,q_prime_ind,theta_ind] +=1
                        self.cvol[q_prime_ind,q_ind,theta_ind] +=1
                    else:
                        self.cvol[q_ind,q_prime_ind,theta_ind] +=q[-1]*q_prime[-1]
                        self.cvol[q_prime_ind,q_ind,theta_ind] +=q[-1]*q_prime[-1]

        #correlating 3D vectors (qx,qy,qz, intensity)
        elif qti.shape[1] == 4:
            # print('Correlating 3D diffraction volume...')

            # get indices where q is less then qmax
            qmags = np.linalg.norm(qti[:,:3], axis=1) #q magnitudes
            correl_vec_indices = np.where(qmags < self.qmax)[0]

            # remove scattering vectors with magnitude less then qmax
            qti = qti[correl_vec_indices]
            qmags = qmags[correl_vec_indices]

            for i, q in enumerate(qti):
                q_mag =  qmags[i]  # np.linalg.norm(q[:3])
                q_ind = index_x(q_mag,self.qmax, self.nq)

                #start q_prime counting ahead of q (i+1)
                for j, q_prime in enumerate(qti[i+1:]):
                    q_prime_mag =  qmags[i+j+1] # np.linalg.norm(q[:3])
                    q_prime_ind = index_x(q_prime_mag,self.qmax, self.nq)

                    theta = angle_between(q[:3]/q_mag, q_prime[:3]/q_prime_mag)

                    theta_ind = index_x(theta, np.pi, self.ntheta)

                    # add values to the corrlation and histograms
                    # in (q1,q2,t) and (q2,q1,t) positions
                    if self.hflag:
                        self.cvol[q_ind,q_prime_ind,theta_ind] +=1
                        self.cvol[q_prime_ind,q_ind,theta_ind] +=1
                    else:
                        self.cvol[q_ind,q_prime_ind,theta_ind] +=q[-1]*q_prime[-1]
                        self.cvol[q_prime_ind,q_ind,theta_ind] +=q[-1]*q_prime[-1]










# if __name__=='__main__':

    # v = Vol(20,20,20,1,2,3)

    # c = CorrelationVol(20,30,1)



    # for i in range(c.nx):
        # for j in range(c.ny):
            # for k in range(c.nz):

                # if i%5==0 and k%5==0:
                    # c.vol[i,j,k] +=1



    # c.plot_xy()

    # c.vol = c.convolve()

    # c.plot_q1q2()

    # plt.show()



    # print(v.vol)
    # v.vol += 33

    # v.save_dbin('testdata/x')
    # print(v.vol)
    # print(v.fname)


    # v2 = Vol(fromfile=True, path='testdata/x')








    


