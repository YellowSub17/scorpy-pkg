

from .vol import Vol
from ..utils import index_x
import numpy as np
from scipy import special
import matplotlib.pyplot as plt
import pyshtools as pysh
from .propertymixins import SphericalVolProps


class SphericalVol(Vol, SphericalVolProps):
    '''
    Representation of a spherical coordinate volume.

    Arguments:
        nq (int): number of scattering magnitude bins.
        n_angle: number of angluar bins
        qmax (float): scattering magnitude limit [1/A].
        grid_type: type of sampling grid. See https://shtools.oca.eu/shtools/public/grid-formats.html for info
        path (str): path to dbin (and log) if being created from memory.
    '''


    def __init__(self, nq=100, nangle=180, qmax=1, comp=False, gridtype='DH1', extend=False,  path=None):
        assert nangle%2==0, 'nangle must be even'
        assert not extend, "Only working with non-extended grids"

        if gridtype=='DH1':
            ntheta = nangle
            nphi = nangle
            nl = int(nangle/2)
            if extend:
                ntheta +=1
                nphi +=1


        elif gridtype=='DH2':
            ntheta = nangle
            nphi = 2*nangle
            nl = int(nangle/2)
            if extend:
                ntheta +=1
                nphi +=1

        else:
            print('WARNING: not using DH grid.')
            ntheta = nangle
            nphi = 2*nangle -1
            nl = int(nangle)
            if extend:
                nphi +=1

        Vol.__init__(   self, nx = nq, ny = ntheta, nz = nphi, \
                        xmax = qmax, ymax = np.pi/2, zmax = 2*np.pi, \
                        xmin = 0, ymin = -np.pi/2, zmin = 0, \
                        comp = comp, path = path)

        self._gridtype = gridtype
        self._extend = extend
        self._nl = nl


    def _save_extra(self, f):
        f.write('[sphv]\n')
        f.write(f'qmax = {self.qmax}\n')
        f.write(f'thetamax = {np.pi/2}\n')
        f.write(f'thetamin = {-np.pi/2}\n')
        f.write(f'phimax = {2*np.pi}\n')
        f.write(f'phimin = {0}\n')
        f.write(f'nq = {self.nq}\n')
        f.write(f'ntheta = {self.ntheta}\n')
        f.write(f'nphi = {self.dphi}\n')
        f.write(f'dq = {self.dq}\n')
        f.write(f'dtheta = {self.dtheta}\n')
        f.write(f'dphi = {self.dphi}\n')
        f.write(f'gridtype = {self.gridtype}\n')
        f.write(f'extend = {self.extend}\n')
        f.write(f'nl = {self.nl}\n')

    def _load_extra(self, config):
        self._gridtype = config['sphv']['gridtype']
        self._extend = config.getboolean('sphv', 'extend')
        self._nl = float(config['sphv']['nl'])









#     def pass_filter(self, lmin=None, lmax=None):
        # print('Filtering')


        # for iq in range(self.nx):
            # print(iq)
            # q_slice = self.vol[iq,...]
            # if self.gridtype =='DH1' or self.gridtype =='DH2':
                # sh_grid = pysh.shclasses.shgrid.DHRealGrid(q_slice)
            # else:
                # sh_grid = pysh.shclasses.shgrid.GLQRealGrid(q_slice)

            # sh_coeffs = sh_grid.expand()

            # coeffs = sh_coeffs.coeffs

            # filt_coeffs = np.zeros(coeffs.shape)

            # filt_coeffs[:,lmin:lmax,:] = coeffs[:,lmin:lmax,:]

            # sh_coeffs = pysh.shclasses.shcoeffs.SHRealCoeffs(filt_coeffs)

            # sh_grid = sh_coeffs.expand(extend = self.extend, grid=self.gridtype)

            # q_slice_filt = sh_grid.data

            # self.vol[iq,...] = q_slice_filt




    def fill_from_cif(self, cif):

        ite = np.ones(cif.scat_sph[:,0].shape)

        q_inds = list(map(index_x, cif.scat_sph[:,0], 0*ite, self.qmax*ite, self.nq*ite))
        theta_inds = list(map(index_x, cif.scat_sph[:,1], self.ymin*ite, self.ymax*ite, self.ny*ite))
        phi_inds = list(map(index_x, cif.scat_sph[:,2], self.zmin*ite, self.zmax*ite, self.nz*ite))


        for q_ind, theta_ind, phi_ind, I in zip(q_inds, theta_inds, phi_inds, cif.scat_sph[:,-1]):
            self.vol[q_ind, theta_ind, phi_ind] +=I

    def get_coeffs(self, q_ind):
        assert q_ind >= 0 and q_ind < self.nq, 'fail'

        q_slice = self.vol[q_ind,...]
        if self.gridtype=='DH1' or self.gridtype=='DH2':
            sh_grid = pysh.shclasses.DHRealGrid(q_slice)
        else:
            sh_grid = pysh.shclasses.GLQRealGrid(q_slice)

        return sh_grid.expand(normalization='ortho', csphase=1).coeffs



        


    # def rotate(self, a,b,c):
        # print('Rotating')


        # djpi2 = pysh.shtools.djpi2(self.lmax)
        # for iq in range(self.nx):
            # print(iq)
            # q_slice = self.vol[iq,...]
            # if self.gridtype =='DH1' or self.gridtype =='DH2':
                # sh_grid = pysh.shclasses.shgrid.DHRealGrid(q_slice)
            # else:
                # sh_grid = pysh.shclasses.shgrid.GLQRealGrid(q_slice)

            # sh_coeffs = sh_grid.expand()

            # coeffs = sh_coeffs.coeffs


            # coeffs_rot = pysh.shtools.SHRotateRealCoef(coeffs, [a,b,c], djpi2)


            # sh_coeffs = pysh.shclasses.shcoeffs.SHRealCoeffs(coeffs_rot)

            # sh_grid = sh_coeffs.expand(extend = self.extend, grid=self.gridtype)

            # q_slice_rot = sh_grid.data

            # self.vol[iq,...] = q_slice_rot


    # def get_angle_sampling(self):

        # q_slice = self.vol[-1,...]
        # if self.gridtype =='DH1' or self.gridtype =='DH2':
            # sh_grid = pysh.shclasses.shgrid.DHRealGrid(q_slice)
        # else:
            # sh_grid = pysh.shclasses.shgrid.GLQRealGrid(q_slice)


        # #fix
        # lats = np.radians(sh_grid.lats())
        # lons = np.radians(sh_grid.lons())

        # return lats, lons



    # def rm_odds(self):
        # print('Removing odd harmonics.')

        # for iq in range(self.nx):
            # print(iq)
            # q_slice = self.vol[iq,...]
            # if self.gridtype =='DH1' or self.gridtype =='DH2':
                # sh_grid = pysh.shclasses.shgrid.DHRealGrid(q_slice)
            # else:
                # sh_grid = pysh.shclasses.shgrid.GLQRealGrid(q_slice)

            # sh_coeffs = sh_grid.expand()

            # coeffs = sh_coeffs.coeffs

            # filt_coeffs = np.zeros(coeffs.shape)

            # filt_coeffs[:,::2,:] = coeffs[:,::2,:]

            # sh_coeffs = pysh.shclasses.shcoeffs.SHRealCoeffs(filt_coeffs)

            # sh_grid = sh_coeffs.expand(extend = self.extend, grid=self.gridtype)

            # q_slice_filt = sh_grid.data

            # self.vol[iq,...] = q_slice_filt


    # def get_coeffs(self, iq):
        # q_slice = self.vol[iq,...]

        # if self.gridtype =='DH1' or self.gridtype =='DH2':
            # sh_grid = pysh.shclasses.shgrid.DHRealGrid(q_slice)
        # else:
            # sh_grid = pysh.shclasses.shgrid.GLQRealGrid(q_slice)

        # sh_coeffs = sh_grid.expand()

        # coeffs = sh_coeffs.coeffs

        # return coeffs


