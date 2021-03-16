import numpy as np
import healpy as hp
from ..utils import ylm_wrapper, index_x, index_xs
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
        print('filling sph from cif')
        spherical = cif.spherical[np.where(cif.spherical[:,0] < self.qmax)]

        for l in range(0, self.nl, 2):
            print(l)
            for im, m in zip(range(2*l+1), range(-l, l+1)):
                iq = np.zeros(self.nq, self.vals_lnm[0].dtype)
                ylm = ylm_wrapper(l,m,spherical[:,2],spherical[:,1], comp=self.comp)
                iylm = ylm*spherical[:,-1]
                for i, q_mag in enumerate(spherical[:,0]):
                    q_index = index_x(q_mag, self.qmax, self.nq)
                    iq[q_index] +=  iylm[i]

                self.vals_lnm[l][:,im] = iq
        return self


    def fill_from_ivol(self, iv):
        print('filling sph from ivol')
        assert self.nq == iv.nq
        assert self.qmax == iv.qmax


        theta, phi = hp.pix2ang(iv.nside, np.arange(0, iv.npix))
        for l in range(0, self.nl, 2):
            print(l)
            for im, m in zip(range(2*l+1), range(-l, l+1)):
                ylm = ylm_wrapper(l,m,phi, theta, comp=self.comp)
                # ylm *= 1/iv.npix
                self.vals_lnm[l][:, im] = np.dot(ylm, iv.ivol.T)
        return self





    def calc_klnm(self, unql, lam_ql):
        print('calc_klnm')
        ## values for q**2 scaling
        q_range = np.linspace(0, self.qmax, self.nq)
        ## for every lm value
        for l in range(0, self.nl, 2):
            print(l)
            for im, m in zip(range(0, 2*l+1), range(-l,l+1)):
                ## get the current estimate for Ilm and scale it
                Ilm = self.vals_lnm[l][:,im]*q_range**2
                ## for every eigen vector, find compent of Ilm(q) to that basis (dot)
                for iq in range(self.nq):
                    x = np.dot(Ilm, unql[:, iq, l])

                    ## save component to the handler
                    self.vals_lnm[l][iq,im] = x

        return self







    def calc_kprime(self,unql, lam_ql):
        print('calc_kprime')
        ## for every lmq value (save calulation by not looping m)
        for l in range(0, self.nl, 2):
            print(f'L = {l}')
            for iq in range(self.nq):

                ## Calulate the nuemerator of the normalization scale factor
                ned = np.sqrt(np.abs(lam_ql[iq, l]))

                # ned = np.abs(lam[iq, l])

                ## Calulate the denominator of the normalization scale factor
                km = self.vals_lnm[l][iq,:]

                donk = np.sqrt(np.sum(km**2))

                ## Calcuate the k` values
                if donk == 0 and ned == 0:
                    donk=1
                    ned =1

                # print(f'n: {np.format_float_scientific(ned,2)}, d: {np.format_float_scientific(donk,2)}, n/d: {ned/donk}')
                # ned = 1e6
                self.vals_lnm[l][iq,:] *= (ned/donk)
                # self.vals_lnm[l][iq,:] *= (1)


        return self






    def calc_Ilm_p(self, unql, lam_ql):
        print('calc_Ilm_p')
        for l in range(0, self.nl, 2):
            print(l)
            ul = unql[...,l]
            for im, m in zip(range(0, 2*l+1), range(-l,l+1)):
                k_sphm = self.vals_lnm[l][:,im]
                #ku is the I'lm
                ku = np.dot(ul, k_sphm)
                self.vals_lnm[l][:,im] = ku

            sf = np.outer(1/np.linspace(0, self.qmax, self.nq)**2, np.ones(2*l+1))
            sf[0,:] = 0
            self.vals_lnm[l] *= sf

        return self

