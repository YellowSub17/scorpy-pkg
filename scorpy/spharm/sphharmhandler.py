import numpy as np
import healpy as hp
from ..utils import ylm_wrapper, index_x, index_xs


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



    def fill_from_cif(self, cif):
        print('Calculating Ilmn from spherical bragg peaks...')
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



    def fill_from_cif2(self,cif):
        import ctypes
        import os
        path = '/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/scorpy/spharm/libc/sphharmhandler.so' 
        lib = ctypes.CDLL(path)

        spherical = cif.spherical
        
        x = lib.makeValsLnmFromSpherical( self.nl, self.nq)
        

        return x







    # def calc_comp2real(self):
        # if self.comp:
            # new_sph = SphericalHandler(self.nq, self.nl, self.qmax, comp=False)
            # for l in range(0, self.nl, 2):
                # for m in range(-l, 0):
                    # new_sph.vals_lnm[l][:,l+m] = np.real((np.complex(0,1)/np.sqrt(2))*( (-1)**m * self.vals_lnm[l][:,l+m] - self.vals_lnm[l][:,l-m]))
                # for m in range(1, l+1):
                    # new_sph.vals_lnm[l][:,l+m] = np.real((1/np.sqrt(2))*( (-1)**m * self.vals_lnm[l][:,l+m] + self.vals_lnm[l][:,l-m]))
                # new_sph.vals_lnm[l][:,l] =   np.real(self.vals_lnm[l][:,l])
            # return new_sph
        # else:
            # print('Conversion of real -> complex not implemented')
            # return None




    def calc_klmn(self, unql):
        print(f'Caclulating klmn from Ilnm...')
        ## Handler for k values
        k_sph = SphericalHandler(self.nq, self.nl, self.qmax)
        ## values for q**2 scaling
        q_range = np.linspace(0, self.qmax, self.nq)
        ## for every lm value
        for l in range(0, self.nl, 2):
            for im, m in zip(range(0, 2*l+1), range(-l,l+1)):
                ## get the current estimate for Ilm and scale it
                Ilm = self.vals_lnm[l][:,im]*q_range**2
                ## for every eigen vector, find compent of Ilm(q) to that basis (dot)
                for iq in range(self.nq):
                    x = np.dot(Ilm, unql[:, iq, l])
                    ## save component to the handler
                    k_sph.vals_lnm[l][iq,im] = x
        return k_sph



    def calc_kprime(self,lam):
        print('Caclulating k\'lnm from klnm...')
        ## New handler for k` values
        kp_sph = SphericalHandler(self.nq, self.nl, self.qmax)
        ## for every lmq value (save calulation by not looping m)
        for l in range(0, self.nl, 2):
            for iq in range(self.nq):
                ## Calulate the nuemerator of the normalization scale factor
                ned = np.sqrt(lam[iq, l])
                ## Calulate the denominator of the normalization scale factor
                km = np.abs(self.vals_lnm[l][iq,:])**2
                donk = np.sqrt(np.sum(km))
                if donk==0:
                    donk=1
                ## Calcuate the k` values
                kp_sph.vals_lnm[l][iq,:] = (ned/donk)*self.vals_lnm[l][iq,:]
        return kp_sph




    # def calc_ivol(self, nside):
        # print('Calculating SphInten from Ilnm...')
        # iv = SphericalIntenVol(self.nq, nside, qmax=self.qmax)
        # theta, phi = hp.pix2ang(iv.nside, np.arange(0,iv.npix))
        # for l in range(0, self.nl, 2):
            # for im, m in zip(range(0, 2*l+1), range(-l,l+1)):
                # ylm = ylm_wrapper(l,m,phi, theta, comp=False)
                # x = np.outer(self.vals_lnm[l][:, im], ylm)

                # iv.ivol +=x

        # #intensity normalization
        # # iv.ivol *= 1/iv.npix

        # return iv




    def calc_Ilm_p(self, u):
        print(f'Calculating I\'lnm from k\'lnm...')
        ilm_p = SphericalHandler(self.nq, self.nl, self.qmax, self.comp)
        for l in range(0, self.nl, 2):
            ul = u[...,l]
            for im, m in zip(range(0, 2*l+1), range(-l,l+1)):
                k_sphm = self.vals_lnm[l][:,im]
                #ku is the I'lm
                ku = np.dot(ul, k_sphm)
                ilm_p.vals_lnm[l][:,im] = ku
        return ilm_p


