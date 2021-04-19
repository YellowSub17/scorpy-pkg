

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


    def __init__(self, nq=100, nangle=180, qmax=1, gridtype='GLQ', extend=False,  path=None, comp=False):
        assert nangle%2==0, 'nangle must be even'

        if gridtype=='DH1':
            if extend:
                nlat = nangle +1
                nlong = nangle +1
                self.lmax = int(nangle/2) -1
            else:
                nlat = nangle
                nlong = nangle
                self.lmax = int(nangle/2) -1


        elif gridtype=='DH2':
            if extend:
                nlat = nangle +1
                nlong = 2*nangle +1
                self.lmax = int(nangle/2) -1
            else:
                nlat = nangle
                nlong = 2*nangle
                self.lmax = int(nangle/2) -1

        else:
            if extend:
                nlat = nangle
                nlong = 2*nangle
                self.lmax = int(nangle) -1
            else:
                nlat = nangle
                nlong = 2*nangle -1
                self.lmax = int(nangle) -1

        Vol.__init__(self, nq,nlat, nlong, qmax, np.pi, 2*np.pi, comp, path=path)




        self.extend = extend
        self.gridtype = gridtype





    def pass_filter(self, lmin=None, lmax=None):
        print('Filtering')


        for iq in range(self.nx):
            print(iq)
            q_slice = self.vol[iq,...]
            if self.gridtype =='DH1' or self.gridtype =='DH2':
                sh_grid = pysh.shclasses.shgrid.DHRealGrid(q_slice)
            else:
                sh_grid = pysh.shclasses.shgrid.GLQRealGrid(q_slice)

            sh_coeffs = sh_grid.expand()

            coeffs = sh_coeffs.coeffs

            filt_coeffs = np.zeros(coeffs.shape)

            filt_coeffs[:,lmin:lmax,:] = coeffs[:,lmin:lmax,:]

            sh_coeffs = pysh.shclasses.shcoeffs.SHRealCoeffs(filt_coeffs)

            sh_grid = sh_coeffs.expand(extend = self.extend, grid=self.gridtype)

            q_slice_filt = sh_grid.data

            self.vol[iq,...] = q_slice_filt




    def fill_from_cif(self, cif):

        ite = np.ones(cif.spherical[:,0].shape)

        q_inds = list(map(index_x, cif.spherical[:,0], self.xmax*ite, self.nx*ite))
        theta_inds = list(map(index_x, cif.spherical[:,1], self.ymax*ite, self.ny*ite))
        phi_inds = list(map(index_x, cif.spherical[:,2], self.zmax*ite, self.nz*ite))


        for q_ind, theta_ind, phi_ind, I in zip(q_inds, theta_inds, phi_inds, cif.spherical[:,-1]):
            self.vol[q_ind, theta_ind, phi_ind] +=I



    def rotate(self, a,b,c):
        print('Rotating')


        djpi2 = pysh.shtools.djpi2(self.lmax)
        for iq in range(self.nx):
            print(iq)
            q_slice = self.vol[iq,...]
            if self.gridtype =='DH1' or self.gridtype =='DH2':
                sh_grid = pysh.shclasses.shgrid.DHRealGrid(q_slice)
            else:
                sh_grid = pysh.shclasses.shgrid.GLQRealGrid(q_slice)

            sh_coeffs = sh_grid.expand()

            coeffs = sh_coeffs.coeffs


            coeffs_rot = pysh.shtools.SHRotateRealCoef(coeffs, [a,b,c], djpi2)


            sh_coeffs = pysh.shclasses.shcoeffs.SHRealCoeffs(coeffs_rot)

            sh_grid = sh_coeffs.expand(extend = self.extend, grid=self.gridtype)

            q_slice_rot = sh_grid.data

            self.vol[iq,...] = q_slice_rot


    def get_angle_sampling(self):

        q_slice = self.vol[-1,...]
        if self.gridtype =='DH1' or self.gridtype =='DH2':
            sh_grid = pysh.shclasses.shgrid.DHRealGrid(q_slice)
        else:
            sh_grid = pysh.shclasses.shgrid.GLQRealGrid(q_slice)


        #fix
        lats = np.radians(sh_grid.lats())
        lons = np.radians(sh_grid.lons())

        return lats, lons



    def rm_odds(self):
        print('Removing odd harmonics.')

        for iq in range(self.nx):
            print(iq)
            q_slice = self.vol[iq,...]
            if self.gridtype =='DH1' or self.gridtype =='DH2':
                sh_grid = pysh.shclasses.shgrid.DHRealGrid(q_slice)
            else:
                sh_grid = pysh.shclasses.shgrid.GLQRealGrid(q_slice)

            sh_coeffs = sh_grid.expand()

            coeffs = sh_coeffs.coeffs

            filt_coeffs = np.zeros(coeffs.shape)

            filt_coeffs[:,::2,:] = coeffs[:,::2,:]

            sh_coeffs = pysh.shclasses.shcoeffs.SHRealCoeffs(filt_coeffs)

            sh_grid = sh_coeffs.expand(extend = self.extend, grid=self.gridtype)

            q_slice_filt = sh_grid.data

            self.vol[iq,...] = q_slice_filt


    def get_coeffs(self, iq):
        q_slice = self.vol[iq,...]

        if self.gridtype =='DH1' or self.gridtype =='DH2':
            sh_grid = pysh.shclasses.shgrid.DHRealGrid(q_slice)
        else:
            sh_grid = pysh.shclasses.shgrid.GLQRealGrid(q_slice)

        sh_coeffs = sh_grid.expand()

        coeffs = sh_coeffs.coeffs

        return coeffs


