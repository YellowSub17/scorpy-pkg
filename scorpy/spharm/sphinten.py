import copy
import healpy as hp
import numpy as np
import matplotlib.pyplot as plt
from ..utils import index_x, index_xs, ylm_wrapper



class SphInten:

    def __init__(self, nq=256, nside=2**6, qmax=1):

        self.nq = nq
        self.nside = nside
        self.npix  = hp.nside2npix(self.nside)
        self.ivol = np.zeros( (self.nq, self.npix ) )
        self.qmax = qmax

    def copy(self):
        return copy.deepcopy(self)

    def fill_from_cif(self, cif, replace=True):
        if replace:
            self.ivol *=0
        pixels = hp.ang2pix(self.nside, cif.spherical[:,1], cif.spherical[:,2])
        q_inds = index_xs(cif.spherical[:,0], self.qmax, self.nq)

        for q_ind, pixel, inten in zip(q_inds, pixels, cif.spherical[:,-1]):
            self.ivol[q_ind, pixel] += inten
        return self

    def fill_from_sph(self, sph, replace=True):
        print('Filling SphInten from SphHarmHandler\n')
        if replace:
            self.ivol *=0
        theta, phi = hp.pix2ang(self.nside, np.arange(0,self.npix))
        for l in range(0, sph.nl, 2):
            for im, m in zip(range(0, 2*l+1), range(-l, l+1)):
                ylm = ylm_wrapper(l,m,phi, theta, comp=False)
                x = np.outer(sph.vals_lnm[l][:, im], ylm)
                self.ivol +=x

        # self.ivol[np.where(self.ivol <0.1)] =0

        return self


    def plot_sphere(self, iq, show_np=False, show_grat=False):
        fig = plt.figure(figsize=(4,5))
        figint = plt.gcf().number
        # hp.orthview(self.ivol[iq,:], half_sky=True, rot=[23,45,60], fig=figint)
        sphere = self.ivol[iq,:]
        if show_np:
            NP = hp.ang2pix(self.nside, 0, 90, lonlat=True)
            sphere[NP] = np.nan
        hp.orthview(sphere, half_sky=True, rot=[45,45,45], fig=figint)
        if show_grat:
            hp.graticule()

    def make_mask(self, invert=False):
        inten_loc = np.where(self.ivol !=0)
        if invert:
            self.ivol = np.ones(self.ivol.shape)
            self.ivol[inten_loc] = 0
        else:
            self.ivol = np.zeros(self.ivol.shape)
            self.ivol[inten_loc] = 1
        return self

    def calc_blnorm(self, bl):

        iave = self.ivol.mean(axis=1)
        iave[np.where(iave==0)] = 1

        b0 = bl.blvol[...,0]
        b0q = np.diag(b0)

        alpha = np.sqrt(b0q)/iave

        self.ivol *= alpha[:,None]
        return self





