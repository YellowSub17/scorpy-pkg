

from .vol import Vol
from ..utils import index_x
import numpy as np
import pyshtools as pysh
from .volspropertymixins import SphericalVolProps
import matplotlib.pyplot as plt
import time



class SphericalVol(Vol, SphericalVolProps):
    """scorpy.SphericalVol:
    A representaion of the spherical coordinate function.
    Attributes:
        nq, ntheta, nphi : int
        qmax : float
        dq, dtheta, dphi : float
        qpts, thetapts, phipts : numpy.array
    Methods:
         SphericalVol.fill_from_cif()
         SphericalVol.fill_from_scat_sph()
    """
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
        f.write(f'nq = {self.nq}\n')
        f.write(f'ntheta = {self.ntheta}\n')
        f.write(f'nphi = {self.nphi}\n')
        f.write(f'dq = {self.dq}\n')
        f.write(f'dtheta = {self.dtheta}\n')
        f.write(f'dphi = {self.dphi}\n')
        f.write(f'nl = {self.nl}\n')

    def _load_extra(self, config):
        self._nl = float(config['sphv']['nl'])



    def fill_from_cif(self, cif):
        '''scorpy.SphericalVol.fill_from_cif():
        Fill the SphericalVol from a CifData object
        Arguments:
            cif : scorpy.CifData
                The CifData object to to fill the CorrelationVol
        '''
        assert cif.qmax == self.qmax, 'CifData and SphericalVol have different qmax'
        self.fill_from_scat_sph(cif.scat_sph)

    def fill_from_iqlm(self, iqlm):
        '''scorpy.SphericalVol.fill_from_iqlm():

        '''

        for q_ind in range(self.nq):
            coeffs = iqlm.vals[q_ind]
            pysh_grid =pysh.shclasses.SHCoeffs.from_array(coeffs).expand()
            self.vol[q_ind,...] = pysh_grid.to_array()[:-1,:-1]


    # def set_q_coeffs(self, q_ind, coeffs):
        # pysh_coeffs = pysh.shclasses.SHCoeffs.from_array(coeffs)
        # pysh_grid = pysh_coeffs.expand()
        # self.vol[q_ind, ...] = pysh_grid.to_array()[:-1, :-1]





    def fill_from_scat_sph(self, scat_sph):
        '''scorpy.SphericalVol.fill_from_scat_sph():
        Fill the SphericalVol from a list of peaks in spherical coordinates.
        Arguments:
            scat_sph : numpy.ndarray
                n by 4 array of n peaks to fill from. Columns of the array should
                be the spherical radius of the peak (A-1), polar angle of the peak
                (theta, radians), and the azimuthial angle of the peak (phi, radians).
        '''
        ite = np.ones(scat_sph[:, 0].shape)
        q_inds = list(map(index_x, scat_sph[:, 0], 0 * ite, self.qmax * ite, self.nq * ite))
        theta_inds = list(map(index_x, scat_sph[:, 1], self.ymin * ite, self.ymax * ite, self.ny * ite))
        phi_inds = list(map(index_x, scat_sph[:, 2], self.zmin * ite, self.zmax * ite, self.nz * ite, ite))
        for q_ind, theta_ind, phi_ind, I in zip(q_inds, theta_inds, phi_inds, scat_sph[:, -1]):
            self.vol[q_ind, theta_ind, phi_ind] += I








    # def get_all_q_coeffs(self):
        # all_coeffs = []
        # for q_slice in self.vol:
            # pysh_grid = pysh.shclasses.DHRealGrid(q_slice)
            # coeffs = pysh_grid.expand().coeffs
            # all_coeffs.append(coeffs)
        # return all_coeffs



    # def get_q_coeffs(self, q_ind):
        # q_slice = self.vol[q_ind, ...]
        # pysh_grid = pysh.shclasses.DHRealGrid(q_slice)
        # c = pysh_grid.expand().coeffs
        # return c


    # def set_q_coeffs(self, q_ind, coeffs):
        # pysh_coeffs = pysh.shclasses.SHCoeffs.from_array(coeffs)
        # pysh_grid = pysh_coeffs.expand()
        # self.vol[q_ind, ...] = pysh_grid.to_array()[:-1, :-1]

