
import numpy as np
import pyshtools as pysh
import matplotlib.pyplot as plt
import time

from ..base.basevol import BaseVol
from ...utils.convert_funcs import index_x
from .sphericalvol_props import SphericalVolProps
from .sphericalvol_plot import SphericalVolPlot
from .sphericalvol_saveload import SphericalVolSaveLoad



class SphericalVol(BaseVol, SphericalVolProps, SphericalVolPlot, SphericalVolSaveLoad):
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



        if path is not None:
            BaseVol.__init__(self, path=path)
        else:
            BaseVol.__init__(self, nx=nq, ny=ntheta, nz=nphi,
                     xmin=0, ymin=0, zmin=0,
                     xmax=qmax, ymax=np.pi, zmax=2 * np.pi,
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
                The CifData object to to fill the SphericalVol
        '''
        assert self.qmax >= cif.qmax, 'cif.qmax > sphv.qmax'
        scat_sph = cif.scat_sph
        ite = np.ones(scat_sph[:, 0].shape)

        q_inds = list(map(index_x, scat_sph[:, 0], 0 * ite, self.qmax * ite, self.nq * ite))
        theta_inds = list(map(index_x, scat_sph[:, 1], self.ymin * ite, self.ymax * ite, self.ny * ite))
        phi_inds = list(map(index_x, scat_sph[:, 2], self.zmin * ite, self.zmax * ite, self.nz * ite, ite))

        intens = scat_sph[:, -1]
        for q_ind, theta_ind, phi_ind, I in zip(q_inds, theta_inds, phi_inds, intens):
            self.vol[q_ind, theta_ind, phi_ind] += I





    def fill_from_iqlm(self, iqlm):
        '''scorpy.SphericalVol.fill_from_iqlm():
        Fill the SphericalVol from a IqlmHandler object
        Arguments:
            iqlm : scorpy.Iqlm
                The IqlmHandler object to to fill the SphericalVol
        '''
        assert iqlm.qmax==self.qmax, 'IqlmHandler and SphericalVol have different qmax'
        assert iqlm.nl==self.nl, 'IqlmHandler and SphericalVol have different nl'
        assert iqlm.nq==self.nq, 'IqlmHandler and SphericalVol have different nq'

        for q_ind in range(self.nq):
            coeffs = iqlm.vals[q_ind]
            pysh_grid =pysh.shclasses.SHCoeffs.from_array(coeffs).expand()
            self.vol[q_ind,...] = pysh_grid.to_array()[:-1,:-1]









