import healpy as hp
import numpy as np
from ..utils import index_x, ylm_wrapper
import itertools
from .sphericalhandler import SphericalHandler



class SphericalIntenVol:

    def __init__(self, nq=256, nside=2**6, qmax=1, cifdata=None, qcell_vectors=None):

        self.nq = nq
        self.nside = nside
        self.npix  = hp.nside2npix(self.nside)
        self.ivol = np.zeros( (self.nq, self.npix ) )
        self.cifdata = cifdata

        if self.cifdata is not None:
            self.qmax = cifdata.qmax
            self.qcell_vectors = cifdata.qcell_vectors
            self.miller_refl = cifdata.miller_refl
            self.scattering = cifdata.scattering
            self.spherical = cifdata.spherical
            self.pixels = np.zeros((self.spherical.shape[0], 2), dtype=np.uint64)
            self.pixels[:,1] = hp.ang2pix(self.nside, self.spherical[:,1], self.spherical[:,2])
            # self.pixels[:,1] = hp.vec2pix(self.nside, self.scattering[:,0], self.scattering[:,1], self.scattering[:,2])
            if self.nq>1:
                for i, q in enumerate(self.spherical[:,0]):
                    q_ind = index_x(q, self.qmax, self.nq)
                    self.pixels[i,0] = q_ind
            else:
                self.pixels[:,0]=0



            for i,pixel in enumerate(self.pixels):
                self.ivol[pixel[0], pixel[1]] += self.miller_refl[i,-1]


        else:
            self.qmax = qmax
            self.qcell_vectors = qcell_vectors
            if qcell_vectors is not None:
                self.miller_refl, self.scattering, self.spherical = self.get_refl()
                self.pixels = np.zeros((self.spherical.shape[0], 2), dtype=np.uint64)
                self.pixels[:,1] = hp.ang2pix(self.nside, self.spherical[:,1], self.spherical[:,2])
                # self.pixels[:,1] = hp.vec2pix(self.nside, self.scattering[:,0], self.scattering[:,1], self.scattering[:,2])
                if self.nq>1:
                    for i, q in enumerate(self.spherical[:,0]):
                        q_ind = index_x(q, self.qmax, self.nq)
                        self.pixels[i,0] = q_ind
                else:
                    self.pixels[:,0]=0



                for i,pixel in enumerate(self.pixels):
                    self.ivol[pixel[0], pixel[1]] += self.miller_refl[i,-1]






    def get_refl(self):

        #maximum h, k, l for bragg h00, 0k0, 00l that is still within qmax
        ind_max = (self.qmax/np.linalg.norm(self.qcell_vectors, axis=0)).astype(np.int32)
        #range of indices that span +/- max index
        h_range = range(-ind_max[0], ind_max[0]+1)
        k_range = range(-ind_max[1], ind_max[1]+1)
        l_range = range(-ind_max[2], ind_max[2]+1)

        #cartesian product of sets of points for hkl
        points = itertools.product(h_range,k_range,l_range, [1])

        #make the generator object points into a list
        miller_refl = np.array([list(i) for i in points])

        # coordinates of bragg peaks
        scattering_pos = np.matmul(miller_refl[:,:-1], np.array(self.qcell_vectors))

        scattering = np.zeros(miller_refl.shape)
        scattering[:, :-1] = scattering_pos
        scattering[:, -1] = miller_refl[:, -1]

        q_mag = np.linalg.norm(scattering[:,:3], axis=1)
        phi = np.arctan2(scattering[:,1], scattering[:,0]) # -pi -> pi
        phi[np.where(phi<0)] = phi[np.where(phi<0)] + 2*np.pi  #0 -> 2pi
        theta = np.arctan2(np.linalg.norm(scattering[:,:2], axis=1),scattering[:,2]) #0 -> pi

        spherical  =np.array([q_mag, theta, phi, miller_refl[:,-1]]).T


        spherical = spherical[np.where(spherical[:,0] < self.qmax)]
        scattering = scattering[np.where(spherical[:,0] < self.qmax)]
        miller_refl = miller_refl[np.where(spherical[:,0] < self.qmax)]


        return miller_refl, scattering, spherical



    def calc_sph(self, nl, comp=False):
        print(f'Calculating Ilmn values from sph values...')
        sph = SphericalHandler(self.nq,nl, self.qmax,comp)

        for l in range(0, nl, 2):
            for im, m in zip(range(2*l+1), range(-l, l+1)):
                theta, phi = hp.pix2ang(self.nside, np.arange(0,self.npix))
                ylm = ylm_wrapper(l,m,phi,theta, comp=comp)
                ylm *=1/self.npix
                sph.vals_lnm[l][:,im] = np.dot(ylm, self.ivol.T)
        return sph


    def calc_Ialpha(self,blvol):
        new_i = SphericalIntenVol(self.nq, self.nside, self.qmax)
        new_i.ivol = self.ivol

        iave = self.ivol.mean(axis=1)
        iave[np.where(iave==0)] = 1

        b0 = blvol[...,0]
        b0q = np.zeros(self.nq)
        for i in range(self.nq):
            b0q[i] = b0[i,i]

        alpha = np.sqrt(b0q)/iave

        new_i.ivol *=alpha[:,None]




        return new_i

print('Submodule sphericalintenvol loaded.')


