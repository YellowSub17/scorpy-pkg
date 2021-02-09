



class BlqqVol:

    def __init__(self, nq=256, nl=36, qmax=1, fromfile=False, path=None):
        Vol.__init__(self, nq,nq,nl, qmax, qmax, nl-1, fromfile=fromfile, path=path)

        self.plot_q1q2 = self.plot_xy



    def fill_from_cvol(self, cvol):
        print(f'Calculating Blqq from Cvol...')

        ntheta = cvol.shape[-1]
        q_range = np.linspace(0,self.qmax,self.nq)
        # create args of legendre eval
        args = np.cos( np.linspace(0, np.pi, ntheta))

        # initialze fmat matrix
        fmat = np.zeros( (ntheta, self.nl) )

        #for every spherical harmonic
        for l in range(0,self.nl, 2):

            leg_vals = (1/(4*np.pi))*special.eval_legendre(l, args)
            fmat[:,l] = leg_vals

        fmat_inv = np.linalg.pinv(fmat)
        # fmat_inv[1:-1:2,:] = np.zeros(ntheta)
        for iq1 in range(self.nq):
            for iq2 in range(iq1, self.nq):
                dot =  np.dot(fmat_inv,cvol[iq1,iq2,:])
                self.blvol[iq1,iq2,:] = dot
                self.blvol[iq2,iq1,:] = dot

        # times 4pi because we multi 2root(pi) in the ylm calc.
        self.blvol *= 4*np.pi

    def fill_from_sph(self, sph):
        print(f'Calculating Blqq from Sph')

        if self.comp:
            bl = np.zeros((self.nq, self.nq), dtype=np.complex128)
        else:
            bl = np.zeros((self.nq, self.nq))

        for l in range(0, self.nl,2):
            for iq1 in range(self.nq):
                for iq2 in range(iq1, self.nq):
                    bl[iq1,iq2] = np.sum(np.conj(sph.vals_lnm[l][iq1])*sph.vals_lnm[l][iq2])
                    bl[iq2,iq1] = np.sum(np.conj(sph.vals_lnm[l][iq2])*sph.vals_lnm[l][iq1])

            self.blvol[...,l] = bl


 #    def view_l(self, l):
        # plt.figure()
        # plt.title(f'fname: {self.fname.split("/")[-1]}, $l$={l}')
        # plt.imshow(self.blvol[...,l], origin='lower', extent=[0,self.nq, 0, self.nq])
        # plt.colorbar()
        # plt.xlabel('$q_1$ / \u212b')
        # plt.ylabel('$q_2$ / \u212b')


    # def view_lq(self,l,q, newfig=False, label='', log=False):

        # if newfig:
            # plt.figure()

        # if log:
            # plt.plot(np.log10(1+np.abs(self.blvol[:,q,l])), label=label)
        # else:
            # plt.plot(self.blvol[:,q,l], label=label)




    def get_eigh(self):
        #TODO fix -lam
        lams = np.zeros( (self.nq, self.nl))
        us = np.zeros( (self.nq, self.nq, self.nl))

        for l in range(0, self.nl,2):
            lam, u = np.linalg.eigh(self.blvol[...,l])

            ## force positive eigenvalues, must change eigenvectors aswell
            u[np.where(lam<0)] *= -1
            lam[np.where(lam<0)] *=-1

            lams[:,l] = lam
            us[:,:,l] = u

        return lams, us





