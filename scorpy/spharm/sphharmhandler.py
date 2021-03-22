import numpy as np
import healpy as hp
from ..utils import ylm_wrapper, index_x
from scipy import special
import copy


class SphHarmHandler:

    def __init__(self, nq, nl, qmax, comp=False):

        self.nl = nl
        self.nq = nq
        self.comp = comp

        self.qmax = qmax
        self.vals_lnm = []

        if self.comp:
            dtype=np.complex128
        else:
            dtype=np.float64

        for l in range(self.nl):
            mn = np.zeros( (self.nq, 2*l+1), dtype)
            self.vals_lnm.append(mn)




    def copy(self):
        return copy.deepcopy(self)



    def fill_from_cif(self, cif):
        print('Filling SphHarmHandler from CifData\n')
        spherical = cif.spherical[np.where(cif.spherical[:,0] <=self.qmax)]

        q_ite = np.ones(len(spherical[:,0]))
        q_inds = np.array(list(map(index_x, spherical[:,0], self.qmax*q_ite, self.nq*q_ite)))

        for l in range(0, self.nl, 2):

            ls = []
            ms = []
            phis = []
            thetas = []
            comps = []

            for im, m in zip(range(2*l+1), range(-l,l+1)):
                ls.append(l)
                ms.append(m)
                phis.append(spherical[:,2])
                thetas.append(spherical[:,1])
                comps.append(self.comp)


            ylms = np.array(list(map(ylm_wrapper, ls, ms, phis, thetas, comps)))

            iylm = ylms*np.outer(np.ones(2*l+1), spherical[:,-1])

            val_ilm = np.zeros( (self.nq, 2*l+1))

            for i, q_index in enumerate(q_inds):
                val_ilm[q_index,:] += iylm[:,i]

            self.vals_lnm[l] = val_ilm

        return self








    def fill_from_ivol(self, iv):
        print('Filling SphHarmHandler from SphInten\n')
        assert self.nq == iv.nq
        assert self.qmax == iv.qmax


        theta, phi = hp.pix2ang(iv.nside, np.arange(0, iv.npix))

        for l in range(0, self.nl, 2):


            ls = np.ones(2*l+1)*l
            ms = np.arange(-l, l+1).astype(float)
            phis = np.outer(np.ones(2*l+1), phi)
            thetas = np.outer(np.ones(2*l+1), theta)
            comps = [self.comp]*(2*l+1)

            ylms = np.array(list(map(ylm_wrapper, ls, ms, phis, thetas, comps)))

            self.vals_lnm[l] = np.dot(ylms, iv.ivol.T).T

        return self







    def calc_klnm(self, unql):
        print('Calculating k\n')
        ## values for q**2 scaling
        q_range = np.linspace(0, self.qmax, self.nq)
        ## for every lm value
        for l in range(0, self.nl, 2):
            for im, m in zip(range(0, 2*l+1), range(-l,l+1)):
                ## get the current estimate for Ilm and scale it
                Ilm = self.vals_lnm[l][:,im]*q_range**2
                ## for every eigen vector, find compent of Ilm(q) to that basis (dot)
                for iq in range(self.nq):
                    x = np.dot(Ilm, unql[:,iq, l])

                    ## save component to the handler
                    self.vals_lnm[l][iq,im] = x

        return self








    def calc_kprime(self,lam_ql):
        print('Calculating k\'\n')

        for l in range(0, self.nl, 2):

            lam_q = lam_ql[:,l]
            lam_min = np.min(np.abs(lam_q[np.where(lam_q != 0)]))
            lam_max = np.max(np.abs(lam_q))

            for iq in range(self.nq):

                ## Calulate the nuemerator of the normalization scale factor
                ned = np.sqrt(np.abs(lam_ql[iq, l]))

                ## Calulate the denominator of the normalization scale factor
                km = self.vals_lnm[l][iq,:]

                donk = np.sqrt(np.sum(km**2))

                ## Calcuate the k` values
                if donk == 0 and ned == 0:
                    donk=1
                    ned =1

                # if np.abs(lam_ql[iq,l]) < 0.001*lam_max:
                    # ned = 1
                    # donk = 1

                # if np.abs(lam_ql[iq,l])< 1.5*lam_min:
                    # donk=1
                    # ned =1

                self.vals_lnm[l][iq,:] *= (ned/donk)


        return self






    def calc_Ilm_p(self, unql):
        print('Calculating Ilm\'\n')
        qs = np.linspace(0,self.qmax, self.nq)**2
        qs[0]=1
        for l in range(0, self.nl, 2):
            ul = unql[...,l]
            for im, m in zip(range(0, 2*l+1), range(-l,l+1)):
                k_sphm = self.vals_lnm[l][:,im]
                #ku is the I'lm
                ku = np.dot(ul, k_sphm)
                self.vals_lnm[l][:,im] = ku

            sf = np.outer(1/qs, np.ones(2*l+1))
            sf[0,:] = 0
            self.vals_lnm[l] *= sf

        return self

