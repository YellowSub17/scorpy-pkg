
import healpy as hp
import numpy as np
from ..utils import index_x, index_xs, ylm_wrapper



class SphInten:

    def __init__(self, nq=256, nside=2**6, qmax=1):

        self.nq = nq
        self.nside = nside
        self.npix  = hp.nside2npix(self.nside)
        self.ivol = np.zeros( (self.nq, self.npix ) )
        self.qmax = qmax


    def fill_from_cif(self, cif, replace=True):
        if repalce:
            self.ivol *=0
        pixels = hp.ang2pix(self.nside, cif.spherical[:,1], cif.spherical[:,2])
        q_inds = index_xs(cif.spherical[:,0], self.qmax, self.nq)

        for i, (q_ind, pixel) in enumerate(zip(q_inds, pixels)):
            self.ivol[q_ind, pixel] += cif.spherical[i, -1]

    def fill_from_sphharmhandler(self, sph):
        if repalce:
            self.ivol *=0
        theta, phi = hp.pix2ang(self.nside, np.arange(0,self.npix))
        for l in range(0, sph.nl, 2):
            for im, m in zip(range(0, 2*l+1), range(-l, l+1)):
                ylm = ylm_wrapper(l,m,phi, theta, comp=False)
                x = np.outer(sph.vals_lnm[l][:, im], ylm)
                self.ivol +=x






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


    # def calc_sph(self, sph):
        # print(f'Calculating Ilmn values from sph values...')
        # # sph = SphericalHandler(self.nq,nl, self.qmax,comp)
        # for l in range(0, sph.nl, 2):
            # for im, m in zip(range(2*l+1), range(-l, l+1)):
                # theta, phi = hp.pix2ang(self.nside, np.arange(0,self.npix))
                # ylm = ylm_wrapper(l,m,phi,theta, comp=sph.comp)
                # ylm *=1/self.npix
                # sph.vals_lnm[l][:,im] = np.dot(ylm, self.ivol.T)
        # # return sph




