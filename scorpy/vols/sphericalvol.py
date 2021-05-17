

from .vol import Vol
from ..utils import index_x
import numpy as np
import pyshtools as pysh
from .volspropertymixins import SphericalVolProps


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

    # def __init__(self, nq=100, nangle=180, qmax=1, comp=False, path=None):
    def __init__(self, nq=100, ntheta=180, nphi=360, qmax=1, comp=False, path=None):

        assert nphi == 2 * ntheta, 'nphi must be 2x ntheta for SphericalVol'

        self._nl = int(ntheta / 2)

        Vol.__init__(self, nx=nq, ny=ntheta, nz=nphi,
                     xmax=qmax, ymax=np.pi, zmax=2 * np.pi,
                     xmin=0, ymin=0, zmin=0,
                     xwrap=False, ywrap=True, zwrap=True,
                     comp=comp, path=path)

    def _save_extra(self, f):
        f.write('[sphv]\n')
        f.write(f'qmax = {self.qmax}\n')
        f.write(f'thetamax = {np.pi}\n')
        f.write(f'thetamin = {0}\n')
        f.write(f'phimax = {2*np.pi}\n')
        f.write(f'phimin = {0}\n')
        f.write(f'nq = {self.nq}\n')
        f.write(f'ntheta = {self.ntheta}\n')
        f.write(f'nphi = {self.dphi}\n')
        f.write(f'dq = {self.dq}\n')
        f.write(f'dtheta = {self.dtheta}\n')
        f.write(f'dphi = {self.dphi}\n')
        # f.write(f'gridtype = {self.gridtype}\n')
        # f.write(f'extend = {self.extend}\n')
        f.write(f'nl = {self.nl}\n')

    def _load_extra(self, config):
        # self._gridtype = config['sphv']['gridtype']
        # self._extend = config.getboolean('sphv', 'extend')
        self._nl = float(config['sphv']['nl'])

    def fill_from_cif(self, cif):

        assert cif.qmax == self.qmax, 'CifData and SphericalVol have different qmax'

        ite = np.ones(cif.scat_sph[:, 0].shape)

        q_inds = list(map(index_x, cif.scat_sph[:, 0], 0 * ite, self.qmax * ite, self.nq * ite))
        theta_inds = list(map(index_x, cif.scat_sph[:, 1], self.ymin * ite, self.ymax * ite, self.ny * ite, ite))
        phi_inds = list(map(index_x, cif.scat_sph[:, 2], self.zmin * ite, self.zmax * ite, self.nz * ite, ite))

        for q_ind, theta_ind, phi_ind, I in zip(q_inds, theta_inds, phi_inds, cif.scat_sph[:, -1]):
            self.vol[q_ind, theta_ind, phi_ind] += I

    def fill_from_scat_sph(self, scat_sph):

        ite = np.ones(scat_sph[:, 0].shape)

        q_inds = list(map(index_x, scat_sph[:, 0], 0 * ite, self.qmax * ite, self.nq * ite))
        theta_inds = list(map(index_x, scat_sph[:, 1], self.ymin * ite, self.ymax * ite, self.ny * ite))
        phi_inds = list(map(index_x, scat_sph[:, 2], self.zmin * ite, self.zmax * ite, self.nz * ite))

        for q_ind, theta_ind, phi_ind, I in zip(q_inds, theta_inds, phi_inds, scat_sph[:, -1]):
            self.vol[q_ind, theta_ind, phi_ind] += I

    def get_coeffs(self, q_ind):
        sh_grid = self.get_q_grid(q_ind)

        c = sh_grid.expand(normalization='4pi').coeffs

        # c[:,1::2,:] *=0

        return c

    def get_angle_sampling(self):

        sh_grid = self.get_q_grid(0)
        # fix
        lats = np.radians(sh_grid.lats())
        lons = np.radians(sh_grid.lons())

        return lats, lons

    def get_q_grid(self, q_ind):
        assert q_ind >= 0 and q_ind < self.nq, 'fail'
        q_slice = self.vol[q_ind, ...]
        sh_grid = pysh.shclasses.DHRealGrid(q_slice)

        return sh_grid

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
