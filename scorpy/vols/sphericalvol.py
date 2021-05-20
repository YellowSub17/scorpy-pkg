

from .vol import Vol
from ..utils import index_x
import numpy as np
import pyshtools as pysh
from .volspropertymixins import SphericalVolProps
import matplotlib.pyplot as plt


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
                     xmax=qmax, ymax=-np.pi / 2, zmax=2 * np.pi,
                     xmin=0, ymin=np.pi / 2, zmin=0,
                     xwrap=False, ywrap=True, zwrap=True,
                     comp=comp, path=path)

    def _save_extra(self, f):
        f.write('[sphv]\n')
        f.write(f'qmax = {self.qmax}\n')
        f.write(f'nq = {self.nq}\n')
        f.write(f'ntheta = {self.ntheta}\n')
        f.write(f'nphi = {self.dphi}\n')
        f.write(f'dq = {self.dq}\n')
        f.write(f'dtheta = {self.dtheta}\n')
        f.write(f'dphi = {self.dphi}\n')
        f.write(f'nl = {self.nl}\n')

    def _load_extra(self, config):
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
        theta_inds = list(map(index_x, scat_sph[:, 1], self.ymin * ite, self.ymax * ite, self.ny * ite, ite))
        phi_inds = list(map(index_x, scat_sph[:, 2], self.zmin * ite, self.zmax * ite, self.nz * ite, ite))

        for q_ind, theta_ind, phi_ind, I in zip(q_inds, theta_inds, phi_inds, scat_sph[:, -1]):
            self.vol[q_ind, theta_ind, phi_ind] += I

    def get_q_coeffs(self, q_ind):
        q_slice = self.vol[q_ind, ...]
        pysh_grid = pysh.shclasses.DHRealGrid(q_slice)
        c = pysh_grid.expand().coeffs
        return c

    def set_q_coeffs(self, q_ind, coeffs):
        pysh_coeffs = pysh.shclasses.SHCoeffs.from_array(coeffs)
        pysh_grid = pysh_coeffs.expand()
        self.vol[q_ind, ...] = pysh_grid.to_array()[:-1, :-1]

    # def fill_random(self, lmax):

        # degrees = np.arange(self.nl, dtype=float)
        # power = degrees
        # power += 0

        # for q_ind in range(self.nq):
            # # coeffs = pysh.SHCoeffs.from_random(power, seed=q_ind).to_array()

            # # coeffs = np.zeros( (2, self.nl, self.nl))
            # # coeffs[0,0, 0] = 1

            # coeffs1 = np.zeros((2, self.nl, self.nl))
            # cs = np.random.randint(0, 2)
            # l = np.random.randint(0, lmax + 1)
            # m = np.random.randint(0, l + 1)
            # coeffs1[cs, l, m] = 1
            # if q_ind in [30]:
                # print(cs,l,m)
                # plt.figure()
                # plt.imshow(pysh.SHCoeffs.from_array(coeffs1).expand().to_array()[:-1,:-1])
                # plt.title(f"{cs}, {l}, {m}")

            # coeffs2 = np.zeros((2, self.nl, self.nl))
         # #    cs = np.random.randint(0, 2)
            # # l = np.random.randint(0, lmax + 1)
            # # m = np.random.randint(0, l + 1)
            # # coeffs2[cs, l, m] = 1
            # # if q_ind in [30]:
                # # print(cs,l,m)
                # # plt.figure()
                # # plt.imshow(pysh.SHCoeffs.from_array(coeffs2).expand().to_array()[:-1,:-1])
                # # plt.title(f"{cs}, {l}, {m}")

            # coeffs = coeffs1+coeffs2
            # coeffs[:, lmax:, :] *= 0
            # coeffs = pysh.SHCoeffs.from_array(coeffs)

            # q_slice = coeffs.expand().to_array()[:-1, :-1]

            # self.vol[q_ind, ...] = q_slice

        # return bink


#     def fill_random_sh(self, q, lmax=999999):
        # for q_ind in range(self.nq):
            # sh = np.random.random((2, int(self.ntheta / 2), int(self.ntheta / 2)))
            # sh[:, lmax:, :] *= 0
            # sh[1, 0, :] *= 0

            # sh[0] = np.tril(sh[0])
            # sh[1] = np.tril(sh[1])

            # sh = pysh.SHCoeffs.from_array(sh)
            # grid = sh.expand()
            # print(grid.lats().shape)

        # # sh_coeffs = pysh.shclasses.shcoeffs.SHRealCoeffs(filt_coeffs)

        # return sh

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
