import numpy as np
np.random.seed(1)
import time
from numba.extending import overload
from numba import jit, prange


import scipy.signal as signal
import configparser as cfp
from scipy import special
import itertools

import matplotlib.pyplot as plt
from xfelcorrel import CorrelationVol, CifData, index_x
import healpy as hp


class SphericalHandler:

    def __init__(self, nq, nl, qmax, comp=False):

        self.nl = nl
        self.nq = nq
        self.comp = comp

        self.qmax = qmax
        self.vals_lnm = []

        for l in range(self.nl):
            if self.comp:
                mn = np.zeros( (self.nq, 2*l+1), np.complex128)
            else:
                mn = np.zeros( (self.nq, 2*l+1))
            self.vals_lnm.append(mn)

    def fill_lnm(self, how='random'):
        if how.lower() == 'random':
            for l in range(0, self.nl, 2):
                self.vals_lnm[l] = np.random.randn(self.nq, 2*l+1)
                for m in range(-l, 0):
                    if m %2==1:
                        self.vals_lnm[l][:,l+m] *=-1


        elif how.lower() == 'ones':
             for l in range(0, self.nl, 2):
                self.vals_lnm[l] = np.ones((self.nq, 2*l+1))
                for m in range(-l, 0):
                    if m %2==1:
                        self.vals_lnm[l][:,l+m] *=-1



    def calc_spherical_scattering(self, spherical):
        print('Calculating Ilmn from spherical bragg peaks...')
        spherical = spherical[np.where(spherical[:,0] < self.qmax)]

        for l in range(0, self.nl, 2):
            for im, m in zip(range(2*l+1), range(-l, l+1)):
                iq = np.zeros(self.nq, self.vals_lnm[0].dtype)
                theta = spherical[:,1] # 0 -> pi
                phi = spherical[:,2] # 0 -> 2pi
                ylm = ylm_wrapper(l,m,phi,theta, comp=self.comp)
                iylm = ylm*spherical[:,-1]
                for i, q_mag in enumerate(spherical[:,0]):
                    q_index = index_x(q_mag, self.qmax, self.nq)
                    iq[q_index] +=  iylm[i]

                self.vals_lnm[l][:,im] = iq




    def calc_comp2real(self):
        if self.comp:
            new_sph = SphericalHandler(self.nq, self.nl, self.qmax, comp=False)
            for l in range(0, self.nl, 2):
                for m in range(-l, 0):
                    new_sph.vals_lnm[l][:,l+m] = np.real((np.complex(0,1)/np.sqrt(2))*( (-1)**m * self.vals_lnm[l][:,l+m] - self.vals_lnm[l][:,l-m]))
                for m in range(1, l+1):
                    new_sph.vals_lnm[l][:,l+m] = np.real((1/np.sqrt(2))*( (-1)**m * self.vals_lnm[l][:,l+m] + self.vals_lnm[l][:,l-m]))
                new_sph.vals_lnm[l][:,l] =   np.real(self.vals_lnm[l][:,l])
            return new_sph
        else:
            print('Conversion of real -> complex not implemented')
            return None




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




    def calc_ivol(self, nside):
        print('Calculating SphInten from Ilnm...')
        iv = SphericalIntenVol(self.nq, nside, qmax=self.qmax)
        theta, phi = hp.pix2ang(iv.nside, np.arange(0,iv.npix))
        for l in range(0, self.nl, 2):
            for im, m in zip(range(0, 2*l+1), range(-l,l+1)):
                ylm = ylm_wrapper(l,m,phi, theta, comp=False)
                x = np.outer(self.vals_lnm[l][:, im], ylm)

                iv.ivol +=x

        #intensity normalization
        # iv.ivol *= 1/iv.npix

        return iv




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









class BlqqVol:

    def __init__(self, nq=256, nl=11, qmax=1, fromfile=False, fname='', comp=False):

       if fromfile:
           self.fname=fname
           config = cfp.ConfigParser()
           config.read(f'{self.fname}_log.txt')

           self.qmax=float(config['params']['qmax'])
           self.nq= int(config['params']['nq'])
           self.nl = int(config['params']['nl'])
           self.comp = config['params']['comp'] == 'True'
           if self.comp:
               file_vol = np.fromfile(f'{self.fname}.dbin', dtype=np.complex128)
           else:
               file_vol = np.fromfile(f'{self.fname}.dbin')
           self.blvol = file_vol.reshape(self.nq,self.nq, self.nl)

       else:
           self.qmax = qmax
           self.nq = nq
           self.nl = nl
           self.fname = fname
           self.comp = comp
           if self.comp:
               self.blvol = np.zeros((nq,nq,nl), dtype=np.complex128)     #init correlation volume space
           else:
               self.blvol =  np.zeros((nq,nq,nl))

    def save_dbin(self,fname, log=True):
        self.fname = fname
        vol = self.blvol.flatten()
        vol.tofile(f'{self.fname}.dbin')
        if log:
           self.save_log(f'{self.fname}_log.txt')

    def save_log(self,fname):
        f = open(fname, 'w')
        f.write('## Blqq Log File\n\n')
        f.write('[params]\n')

        f.write(f'fname = {self.fname}\n')
        f.write(f'qmax = {self.qmax}\n')
        f.write(f'nq = {self.nq}\n')
        f.write(f'nl = {self.nl}\n')
        f.write(f'comp = {self.comp}')
        f.close()

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


    def view_l(self, l):
        plt.figure()
        plt.title(f'fname: {self.fname.split("/")[-1]}, $l$={l}')
        plt.imshow(self.blvol[...,l], origin='lower', extent=[0,self.nq, 0, self.nq])
        plt.colorbar()
        plt.xlabel('$q_1$ / \u212b')
        plt.ylabel('$q_2$ / \u212b')


    def view_lq(self,l,q, newfig=False, label='', log=False):

        if newfig:
            plt.figure()

        if log:
            plt.plot(np.log10(1+np.abs(self.blvol[:,q,l])), label=label)
        else:
            plt.plot(self.blvol[:,q,l], label=label)




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


    def convolve(self,  kern_L=2, kern_size =5, std_q = 1, std_l=1):

        q_space = np.linspace(-kern_L,kern_L, kern_size )
        l_space = np.linspace(-kern_L,kern_L, kern_size )

        kq1, kq2, kl = np.meshgrid(q_space,q_space, l_space)

        K = np.zeros( (kern_size, kern_size, kern_size))

        K = np.exp(- ( kq1**2/(2*std_q**2) + kq2**2/(2*std_q**2) + kl**2/(2*std_l**2)))
        blur = signal.fftconvolve(self.blvol, K)

        return blur










def ylm_wrapper(l,m, phi,theta, comp=False):
    if comp:
        # COMPLEX BASIS
        ylm = special.sph_harm(m,l, phi , theta)
    else:
        ## REAL BASIS
        if m < 0:
            ylm = (np.sqrt(2)*(-1)**m)*np.imag(special.sph_harm(np.abs(m),l, phi,theta))
        elif m > 0:
            ylm = (np.sqrt(2)*(-1)**m)*np.real(special.sph_harm(m,l, phi,theta))
        else:
            ylm = np.real(special.sph_harm(m,l, phi, theta))

    #2*sqrt(pi) ensures orthogonality
    ylm *= 2*np.sqrt(np.pi)
    return ylm








if __name__ == '__main__':
    plt.close('all')

  #   # name = 'adamsite'
    # # qq = 87
    # # rot = (90,0,0)

    # name = '1al1'
    # qq = 87
    # rot = (90,0,0)



    # cif = CifData(f'data/xtal/{name}-sf.cif')
    # bl = BlqqVol(fromfile=True, fname=f'data/dbins/blqq/{name}_bl_pin')

    # iv_goal = SphericalIntenVol(bl.nq, 2**5, cifdata=cif)

    # iv_mask = SphericalIntenVol(bl.nq, 2**5, cifdata=cif)

    # iv_mask.ivol[np.where(iv_goal.ivol != 0)] = 1



    # hp.orthview(iv_goal.ivol[qq], title='Target Intensity', rot=rot)
    # plt.savefig('data/saved_plots/target_inten.png')
    # hp.orthview(iv_mask.ivol[qq], title='Support Constraint Mask', rot=rot)
    # plt.savefig('data/saved_plots/support.png')


    # ## Get the eigen values and eigenvectors of the bl matrix
    # bl_lam, bl_u = bl.get_eigh()



    # Ilm_sph = iv_goal.calc_sph(bl.nl)

    # iv_start = Ilm_sph.calc_ivol(2**5)
    # iv_start.ivol = np.random.random(iv_start.ivol.shape)
    # hp.orthview(iv_start.ivol[qq], title='Starting Intensity', rot=rot)
    # plt.savefig('data/saved_plots/init_inten.png')


    # loop_end = -1

    # for i in range(4):

        # loop_start = time.time()
        # print(f'\n\n')
        # print(f'Loop {i}')
        # print(f'Last loop took {loop_end} seconds.')
        # print(f'\n\n')


        # ###### CORRELATION CONSTRAINT
        # ##calculate the klmn values from the Ilm values and bl eigenvectors
        # k_sph = Ilm_sph.calc_klmn(bl_u)
        # ## scale kprime values from klmn and bl eigenvalues
        # kp_sph = k_sph.calc_kprime(bl_lam)
        # ## modify the Ilm values with the bl eigenvectors kprime values
        # Ilm_p_sph = kp_sph.calc_Ilm_p(bl_u)
        # ## recompose intensity from Ilm values
        # Ip = Ilm_p_sph.calc_ivol(iv_mask.nside)



        # #### plot result of correlation constraint
        # hp.orthview(Ip.ivol[qq], title=f'iteration {i}', rot=rot)
        # plt.savefig(f'data/saved_plots/iter_{i}.png')
        # # plt.close('all')




        # ###### SUPPORT CONSTRAINT
        # ## mask q position that are not on bragg peaks
        # Ip.ivol *= iv_mask.ivol
        # ## Only consider positive magnitudes
        # Ip.ivol = np.max((Ip.ivol, np.zeros(Ip.ivol.shape)), axis=0)



        # ###### NORMALISATION CONSTRAINT
        # Ia = Ip.calc_Ialpha(bl.blvol)
        # # Ia = Ip

        # hp.orthview(Ia.ivol[qq], title=f'iteration masked {i}', rot=rot)
        # plt.savefig(f'data/saved_plots/iter_masked_{i}.png')

        # ## Decompose masked intensity into Ilm
        # Ilm_sph = Ia.calc_sph(Ilm_sph.nl)


        # loop_end = time.time() - loop_start




    # Ip.ivol[qq]  = Ip.ivol[qq]
    # ## plot final result of the masked intensity
    # hp.orthview(Ip.ivol[qq], title='final_inten', rot=rot)
    # plt.savefig(f'data/saved_plots/final_inten.png')

    # plt.show()




























    # # # MAKE BLQQ FROM CORREL + CIF
    # names = ['1al1', '1vds', '5lf5', 'CuCN', 'diamond', 'adamsite']




    # nl = 61

    # for name in names:

        # correl = CorrelationVol(fromfile=True, fname=f'data/dbins/{name}_qcor')
        # cif = CifData(f'data/xtal/{name}-sf.cif', qmax=correl.qmax)
        # iv = SphericalIntenVol(nq=correl.nq,nside=2**6, cifdata=cif)

        # print(f'{name} sph1')
        # sph1 = SphericalHandler(correl.nq, nl, correl.qmax)
        # sph1.calc_spherical_scattering(cif.spherical)
        # print(f'{name} bl1')
        # bl1 = BlqqVol(correl.nq, nl, correl.qmax)
        # bl1.fill_from_sph(sph1)
        # bl1.save_dbin(f'data/dbins/blqq/{name}_bl_Ilm')


        # print(f'{name} bl4')
        # bl4 = BlqqVol(correl.nq, nl, correl.qmax, comp=False)
        # bl4.fill_from_cvol(correl.cvol)
        # bl4.save_dbin(f'data/dbins/blqq/{name}_bl_pin')


        # print(f'{name} sph2')
        # sph2 = SphericalHandler(correl.nq, nl, correl.qmax, comp=True)
        # sph2.fill_lnm_spherical_scattering(cif.spherical)
        # print(f'{name} bl2')
        # bl2 = BlqqVol(correl.nq, nl, correl.qmax, comp=True)
        # bl2.fill_from_sph(sph2)
        # bl2.save_dbin(f'data/dbins/blqq/{name}_bl_Ilm_comp')



        # print(f'{name} sph3')
        # sph3 = SphericalHandler(correl.nq, nl, correl.qmax, comp=True)
        # sph3.fill_lnm_ivol(iv.ivol)
        # print(f'{name} bl3')
        # bl3 = BlqqVol(correl.nq, nl, correl.qmax, comp=True)
        # bl3.fill_from_sph(sph3)
        # bl3.save_dbin(f'data/dbins/blqq/{name}_bl_hp')



        # print(f'{name} sph5')
        # sph5 = sph2.convert_comp2real()
        # print(f'{name} bl5')
        # bl5 = BlqqVol(correl.nq, nl, correl.qmax, comp=False)
        # bl5.fill_from_sph(sph5)
        # bl5.save_dbin(f'data/dbins/blqq/{name}_bl_Ilm_comp2real')



        # print(f'{name} sph6')
        # sph6 = sph3.convert_comp2real()
        # print(f'{name} bl6')
        # bl6 = BlqqVol(correl.nq, nl, correl.qmax, comp=False)
        # bl6.fill_from_sph(sph6)
        # bl6.save_dbin(f'data/dbins/blqq/{name}_bl_hp_comp2real')
