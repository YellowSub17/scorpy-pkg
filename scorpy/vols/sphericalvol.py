

from .vol import Vol
from ..utils import index_x
import numpy as np
from scipy import special
import matplotlib.pyplot as plt
import pyshtools as pysh



class SphericalVol(Vol):
    '''
    Representation of a spherical coordinate volume.

    Arguments:
        nq (int): number of scattering magnitude bins.
        n_angle: number of angluar bins
        qmax (float): scattering magnitude limit [1/A].
        grid_type: type of sampling grid. See https://shtools.oca.eu/shtools/public/grid-formats.html for info
        path (str): path to dbin (and log) if being created from memory.
    '''


    def __init__(self, nq=100, n_angle=180, qmax=1, grid_type='GLQ', extend=False,  path=None, comp=False):
        assert n_angle%2==0, 'n_angle must be even'

        if grid_type=='DH1':
            if extend:
                N_lat = n_angle +1
                N_long = n_angle +1
                self.lmax = int(n_angle/2) -1
            else:
                N_lat = n_angle
                N_long = n_angle
                self.lmax = int(n_angle/2) -1


        elif grid_type=='DH2':
            if extend:
                N_lat = n_angle +1
                N_long = 2*n_angle +1
                self.lmax = int(n_angle/2) -1
            else:
                N_lat = n_angle
                N_long = 2*n_angle
                self.lmax = int(n_angle/2) -1

        else:
            if extend:
                N_lat = n_angle
                N_long = 2*n_angle 
                self.lmax = int(n_angle) -1
            else:
                N_lat = n_angle
                N_long = 2*n_angle -1
                self.lmax = int(n_angle) -1

        Vol.__init__(self, nq,N_lat, N_long, qmax, np.pi, 2*np.pi, comp, path=path)


#         self.vol = np.random.random(self.vol.shape)

        # apple=40
        # bink = (int(self.ny/2-apple), int(self.ny/2 + apple))
        # bonk = (int(self.nz/2-apple), int(self.nz/2 + apple))

        # self.vol[:,bink[0]:bink[1], bonk[0]:bonk[1]] = 1

        self.extend = extend
        self.grid_type = grid_type





    def pass_filter(self, lmin=None, lmax=None):
        print('Filtering')


        for iq in range(self.nx):
            print(iq)
            q_slice = self.vol[iq,...]
            if self.grid_type =='DH1' or self.grid_type =='DH2':
                sh_grid = pysh.shclasses.shgrid.DHRealGrid(q_slice)
            else:
                sh_grid = pysh.shclasses.shgrid.GLQRealGrid(q_slice)

            sh_coeffs = sh_grid.expand()

            coeffs = sh_coeffs.coeffs

            filt_coeffs = np.zeros(coeffs.shape)

            filt_coeffs[:,lmin:lmax,:] = coeffs[:,lmin:lmax,:]

            sh_coeffs = pysh.shclasses.shcoeffs.SHRealCoeffs(filt_coeffs)

            sh_grid = sh_coeffs.expand(extend = self.extend, grid=self.grid_type)

            q_slice_filt = sh_grid.data

            self.vol[iq,...] = q_slice_filt




    def fill_from_cif(self, cif):

        ite = np.ones(cif.spherical[:,0].shape)

        q_inds = list(map(index_x, cif.spherical[:,0], self.xmax*ite, self.nx*ite))
        theta_inds = list(map(index_x, cif.spherical[:,1], self.ymax*ite, self.ny*ite))
        phi_inds = list(map(index_x, cif.spherical[:,2], self.zmax*ite, self.nz*ite))


        for q_ind, theta_ind, phi_ind, I in zip(q_inds, theta_inds, phi_inds, cif.spherical[:,-1]):
            self.vol[q_ind, theta_ind, phi_ind] +=I

        # self.pass_filter()


    def rotate(self, a,b,c):
        print('Rotating')


        djpi2 = pysh.shtools.djpi2(self.lmax)
        for iq in range(self.nx):
            print(iq)
            q_slice = self.vol[iq,...]
            if self.grid_type =='DH1' or self.grid_type =='DH2':
                sh_grid = pysh.shclasses.shgrid.DHRealGrid(q_slice)
            else:
                sh_grid = pysh.shclasses.shgrid.GLQRealGrid(q_slice)

            sh_coeffs = sh_grid.expand()

            coeffs = sh_coeffs.coeffs


            coeffs_rot = pysh.shtools.SHRotateRealCoef(coeffs, [a,b,c], djpi2)


            sh_coeffs = pysh.shclasses.shcoeffs.SHRealCoeffs(coeffs_rot)

            sh_grid = sh_coeffs.expand(extend = self.extend, grid=self.grid_type)

            q_slice_rot = sh_grid.data

            self.vol[iq,...] = q_slice_rot



