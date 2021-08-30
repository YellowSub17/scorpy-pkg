import numpy as np


class VolProps:

    @property
    def nx(self):
        '''scorpy.Vol.nx: Number of voxels in x-axis direction.'''
        return int(self._nx)

    @property
    def ny(self):
        '''scorpy.Vol.ny: Number of voxels in y-axis direction.'''
        return int(self._ny)

    @property
    def nz(self):
        '''scorpy.Vol.nz: Number of voxels in z-axis direction.'''
        return int(self._nz)

    @property
    def xmin(self):
        '''scorpy.Vol.xmin: Minimum value of x-axis.'''
        return self._xmin

    @property
    def ymin(self):
        '''scorpy.Vol.ymin: Minimum value of y-axis.'''
        return self._ymin

    @property
    def zmin(self):
        '''scorpy.Vol.zmin: Minimum value of z-axis.'''
        return self._zmin

    @property
    def xmax(self):
        '''scorpy.Vol.xmax: Maximum value of x-axis.'''
        return self._xmax

    @property
    def ymax(self):
        '''scorpy.Vol.ymax: Maximum value of y-axis.'''
        return self._ymax

    @property
    def zmax(self):
        '''scorpy.Vol.zmax: Maximum value of z-axis.'''
        return self._zmax

    @property
    def xwrap(self):
        '''scorpy.Vol.xwrap: Describes if x-axis is periodic or not.'''
        return self._xwrap

    @property
    def ywrap(self):
        '''scorpy.Vol.ywrap: Describes if y-axis is periodic or not.'''
        return self._ywrap

    @property
    def zwrap(self):
        '''scorpy.Vol.zwrap: Describes if z-axis is periodic or not.'''
        return self._zwrap

    @property
    def dx(self):
        '''scorpy.Vol.dx: Size of voxel in x-axis'''
        return np.abs((self.xmax - self.xmin) / (self.nx))

    @property
    def dy(self):
        '''scorpy.Vol.dy: Size of voxel in y-axis'''
        return np.abs((self.ymax - self.ymin) / (self.ny))

    @property
    def dz(self):
        '''scorpy.Vol.dz: Size of voxel in y-axis'''
        return np.abs((self.zmax - self.zmin) / (self.nz))


    # '''Array of sample points on the axis. If no wrapping, sample points
    # are at the centre of each voxel. If wrapping, sample points are at the
    # start of each voxel.'''
    @property
    def xpts(self):
        '''scorpy.Vol.xpts: Array of sample points on the x-axis. Dependant on wrapping.'''
        if self.xwrap:
            return np.linspace(self.xmin, self.xmax, self.nx, endpoint=False)
        else:
            return np.linspace(self.xmin, self.xmax, self.nx + 1, endpoint=True)[:-1] + self.dx / 2

    @property
    def ypts(self):
        '''scorpy.Vol.ypts: Array of sample points on the y-axis. Dependant on wrapping.'''
        if self.ywrap:
            return np.linspace(self.ymin, self.ymax, self.ny, endpoint=False)
        else:
            return np.linspace(self.ymin, self.ymax, self.ny + 1, endpoint=True)[:-1] + self.dy / 2

    @property
    def zpts(self):
        '''scorpy.Vol.zpts: Array of sample points on the z-axis. Dependant on wrapping'''
        if self.zwrap:
            return np.linspace(self.zmin, self.zmax, self.nz, endpoint=False)
        else:
            return np.linspace(self.zmin, self.zmax, self.nz + 1, endpoint=True)[:-1] + self.dz / 2

    @property
    def comp(self):
        '''scorpy.Vol.comp: Describes dtype of volume, complex or real.'''
        return self._comp

    @property
    def vol(self):
        '''scorpy.Vol.vol: Array holding values of the function.'''
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

#     @property
    # def lmax(self):
        # return self.nl - 1

    @property
    def dq(self):
        return self.dx

    @property
    def qpts(self):
        return self.xpts


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
    def nl(self):
        return int(self._nl)

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

    @property
    def normalization(self):
        return self._normaization


