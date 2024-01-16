
import numpy as np
import pyshtools as pysh
import matplotlib.pyplot as plt
import time

from ..base.basevol import BaseVol
from ...utils.convert_funcs import index_x_wrap, index_x_nowrap
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
    def __init__(self, nq=100, ntheta=180, nphi=360, qmax=1, qmin=0, comp=False, path=None):

        assert nphi == 2 * ntheta, 'nphi must be 2x ntheta for SphericalVol'

        self._nl = int(ntheta / 2)


        if path is not None:
            BaseVol.__init__(self, path=path)
        else:
            BaseVol.__init__(self, nx=nq, ny=ntheta, nz=nphi,
                     xmin=qmin, ymin=0, zmin=0,
                     xmax=qmax, ymax=np.pi, zmax=2 * np.pi,
                     xwrap=False, ywrap=True, zwrap=True,
                     comp=comp, path=path)

    def _save_extra(self, f):
        f.write('[sphv]\n')
        f.write(f'qmax = {self.qmax}\n')
        f.write(f'qmin = {self.qmin}\n')
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


        q_inds = self.get_indices(cif.scat_sph[:,0], axis=0)
        theta_inds = self.get_indices(cif.scat_sph[:,1], axis=1)
        phi_inds = self.get_indices(cif.scat_sph[:,2], axis=2)




        intens = cif.scat_sph[:, -1]
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
        assert iqlm.qmin==self.qmin, 'IqlmHandler and SphericalVol have different qmin'
        assert iqlm.nq==self.nq, 'IqlmHandler and SphericalVol have different nq'


        if iqlm.nl<self.nl:
            vals = np.zeros((self.nq, 2, self.nl, self.nl))
            vals[:, :, :iqlm.nl, :iqlm.nl] = iqlm.vals
        else:
            vals = iqlm.vals[:,:,:self.nl, :self.nl]

        for q_ind, q_coeffs in enumerate(vals):
            # coeffs = iqlm.vals[q_ind, :, :self.nl, :self.nl]
            # print(coeffs.shape)
            pysh_grid =pysh.shclasses.SHCoeffs.from_array(q_coeffs).expand()
            self.vol[q_ind,...] = pysh_grid.to_array()[:-1,:-1]





    def expand_bragg_peaks(self, dpix):

        new_vol = np.zeros(self.vol.shape)

        for pti in self.ls_pts(inds=True):
            xul = int(pti[0]-dpix), int(pti[0]+dpix+1)
            yul = int(pti[1]-dpix), int(pti[1]+dpix+1)
            zul = int(pti[2]-dpix), int(pti[2]+dpix+1)

            new_vol[xul[0]:xul[1], yul[0]:yul[1], zul[0]:zul[1]] += 1

            #wrap support around phi axis
            if zul[1]>self.nz:
                new_vol[xul[0]:xul[1], yul[0]:yul[1], 0:zul[1]-self.nz] += 1

            if zul[0]<0:
                new_vol[xul[0]:xul[1], yul[0]:yul[1], zul[0]:] += 1
                new_vol[xul[0]:xul[1], yul[0]:yul[1], 0:zul[1]] += 1

        self.vol = new_vol




    def integrate_bragg_peaks(self, mask_vol, dpix):

        new_vol = np.zeros(self.vol.shape)
        for xi, yi, zi, I in mask_vol.ls_pts(inds=True):
            xul = int(xi-dpix), int(xi+dpix+1)
            yul = int(yi-dpix), int(yi+dpix+1)
            zul = int(zi-dpix), int(zi+dpix+1)

            sf = np.sin(self.zpts[int(yi)])


            intenI = 0
            if zul[1]>self.nz:
                intenI +=self.vol[ xul[0]:xul[1], yul[0]:yul[1], zul[0]:zul[1] ].sum()*sf
                intenI +=self.vol[ xul[0]:xul[1], yul[0]:yul[1], 0:zul[1]-self.nz].sum()*sf

            elif zul[0] < 0:
                intenI +=self.vol[xul[0]:xul[1], yul[0]:yul[1], zul[0]].sum()*sf
                intenI +=self.vol[ xul[0]:xul[1], yul[0]:yul[1], 0:zul[1]].sum()*sf
            else:
                intenI = self.vol[ xul[0]:xul[1], yul[0]:yul[1], zul[0]:zul[1] ].sum()*sf


            new_vol[int(xi), int(yi), int(zi)] += intenI



        self.vol = new_vol



