import numpy as np


class VolProps:

    @property
    def nx(self):
        return self._nx

    @property
    def ny(self):
        return self._ny

    @property
    def nz(self):
        return self._nz

    @property
    def xmin(self):
        return self._xmin

    @property
    def ymin(self):
        return self._ymin

    @property
    def zmin(self):
        return self._zmin

    @property
    def xmax(self):
        return self._xmax

    @property
    def ymax(self):
        return self._ymax

    @property
    def zmax(self):
        return self._zmax

    @property
    def xwrap(self):
        return self._xwrap

    @property
    def ywrap(self):
        return self._ywrap

    @property
    def zwrap(self):
        return self._zwrap

    @property
    def dx(self):
        return (self.xmax - self.xmin) / (self.nx)

    @property
    def dy(self):
        return (self.ymax - self.ymin) / (self.ny)

    @property
    def dz(self):
        return (self.zmax - self.zmin) / (self.nz)

    @property
    def xbins(self):
        return np.linspace(self.xmin, self.xmax, self.nx + 1)

    @property
    def ybins(self):
        return np.linspace(self.ymin, self.ymax, self.ny + 1)

    @property
    def zbins(self):
        return np.linspace(self.zmin, self.zmax, self.nz + 1)

    @property
    def xpts(self):
        return self.xbins[:-1] + self.dx / 2

    @property
    def ypts(self):
        return self.ybins[:-1] + self.dy / 2

    @property
    def zpts(self):
        return self.zbins[:-1] + self.dz / 2

    @property
    def comp(self):
        return self._comp

    @property
    def vol(self):
        return self._vol

    @vol.setter
    def vol(self, new_vol):
        assert new_vol.shape == self.vol.shape, 'Cannot replace vols with different shapes'
        self._vol = new_vol


class CorrelationVolProps:

    @property
    def nq(self):
        return self.nx

    @property
    def npsi(self):
        return self.nz

    @property
    def qmax(self):
        return self.xmax

    @property
    def dq(self):
        return self.dx

    @property
    def dpsi(self):
        return self.dz

    @property
    def qpts(self):
        return self.xpts

    @property
    def psipts(self):
        return self.zpts


class BlqqVolProps:

    @property
    def nq(self):
        return self.nx

    @property
    def nl(self):
        return self.nz

    @property
    def qmax(self):
        return self.xmax

    @property
    def lmax(self):
        return self.nl - 1

    @property
    def dq(self):
        return self.dx

    @property
    def qpts(self):
        return self.xpts

    @property
    def lpts(self):
        return self.zpts


class PadfVolProps:

    @property
    def nr(self):
        return self.nx

    @property
    def npsi(self):
        return self.nz

    @property
    def rmax(self):
        return self.xmax

    @property
    def dr(self):
        return self.dx

    @property
    def dpsi(self):
        return self.dz

    @property
    def nl(self):
        return self._nl

    @property
    def wavelength(self):
        return self._wavelength

    @property
    def rpts(self):
        return self.xpts

    @property
    def psipts(self):
        return self.zpts


class SphericalVolProps:

    @property
    def nq(self):
        return self.nx

    @property
    def ntheta(self):
        return self.ny

    @property
    def nphi(self):
        return self.nz

    @property
    def qmax(self):
        return self.xmax

    @property
    def dq(self):
        return self.dx

    @property
    def dtheta(self):
        return self.dy

    @property
    def dphi(self):
        return self.dz

    @property
    def gridtype(self):
        return self._gridtype

    @property
    def extend(self):
        return self._extend

    @property
    def nl(self):
        return self._nl

    @property
    def lmax(self):
        return self.nl - 1

    @property
    def qpts(self):
        return self.xpts

    @property
    def thetapts(self):
        return self.ypts

    @property
    def phipts(self):
        return self.zpts