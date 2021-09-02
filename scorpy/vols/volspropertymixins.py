import numpy as np


class VolProps:

    @property
    def nx(self):
        '''
	scorpy.Vol.nx:
            Number of voxels in x-axis direction.
        '''
        return int(self._nx)

    @property
    def ny(self):
        '''
	scorpy.Vol.ny:
            Number of voxels in y-axis direction.
        '''
        return int(self._ny)

    @property
    def nz(self):
        '''
	scorpy.Vol.nz:
            Number of voxels in z-axis direction.
        '''
        return int(self._nz)

    @property
    def xmin(self):
        '''
	scorpy.Vol.xmin:
            Minimum value of x-axis.
        '''
        return self._xmin

    @property
    def ymin(self):
        '''
	scorpy.Vol.ymin:
            Minimum value of y-axis.
        '''
        return self._ymin

    @property
    def zmin(self):
        '''
	scorpy.Vol.zmin:
            Minimum value of z-axis.
        '''
        return self._zmin

    @property
    def xmax(self):
        '''
	scorpy.Vol.xmax:
            Maximum value of x-axis.
        '''
        return self._xmax

    @property
    def ymax(self):
        '''
	scorpy.Vol.ymax:
            Maximum value of y-axis.
        '''
        return self._ymax

    @property
    def zmax(self):
        '''
	scorpy.Vol.zmax:
            Maximum value of z-axis.
        '''
        return self._zmax

    @property
    def xwrap(self):
        '''
	scorpy.Vol.xwrap:
            Describes if x-axis is periodic or not.
        '''
        return self._xwrap

    @property
    def ywrap(self):
        '''
	scorpy.Vol.ywrap:
            Describes if y-axis is periodic or not.
        '''
        return self._ywrap

    @property
    def zwrap(self):
        '''
	scorpy.Vol.zwrap:
            Describes if z-axis is periodic or not.
        '''
        return self._zwrap

    @property
    def dx(self):
        '''
	scorpy.Vol.dx:
            Size of voxel in x-axis
        '''
        return np.abs((self.xmax - self.xmin) / (self.nx))

    @property
    def dy(self):
        '''
	scorpy.Vol.dy:
            Size of voxel in y-axis
        '''
        return np.abs((self.ymax - self.ymin) / (self.ny))

    @property
    def dz(self):
        '''
	scorpy.Vol.dz:
            Size of voxel in y-axis
        '''
        return np.abs((self.zmax - self.zmin) / (self.nz))

    @property
    def xpts(self):
        '''
	scorpy.Vol.xpts:
            Array of sample points on the x-axis. Dependant on wrapping.
        '''
        if self.xwrap:
            return np.linspace(self.xmin, self.xmax, self.nx, endpoint=False)
        else:
            return np.linspace(self.xmin, self.xmax, self.nx + 1, endpoint=True)[:-1] + self.dx / 2

    @property
    def ypts(self):
        '''
	scorpy.Vol.ypts:
            Array of sample points on the y-axis. Dependant on wrapping.
        '''
        if self.ywrap:
            return np.linspace(self.ymin, self.ymax, self.ny, endpoint=False)
        else:
            return np.linspace(self.ymin, self.ymax, self.ny + 1, endpoint=True)[:-1] + self.dy / 2

    @property
    def zpts(self):
        '''
	scorpy.Vol.zpts:
            Array of sample points on the z-axis. Dependant on wrapping
        '''
        if self.zwrap:
            return np.linspace(self.zmin, self.zmax, self.nz, endpoint=False)
        else:
            return np.linspace(self.zmin, self.zmax, self.nz + 1, endpoint=True)[:-1] + self.dz / 2

    @property
    def comp(self):
        '''
	scorpy.Vol.comp:
            Describes dtype of volume, complex or real.
        '''
        return self._comp

    @property
    def vol(self):
        '''
	scorpy.Vol.vol:
            Array holding values of the function.
        '''
        return self._vol

    @vol.setter
    def vol(self, new_vol):
        assert new_vol.shape == self.vol.shape, 'Cannot replace vols with different shapes'
        self._vol = new_vol


class CorrelationVolProps:

    @property
    def nq(self):
        '''
	scorpy.CorrelationVol.nx:
            Number of voxels in q-axis directions.
        '''
        return self.nx

    @property
    def npsi(self):
        '''
	scorpy.CorrelationVol.npsi:
            Number of voxels in psi-axis direction.
        '''
        return self.nz

    @property
    def qmax(self):
        '''
	scorpy.CorrelationVol.qmax:
            Maximum value of q-axes.
        '''
        return self.xmax

    @property
    def dq(self):
        '''
	scorpy.CorrelationVol.dq:
            Size of a voxel in q-axis
        '''
        return self.dx

    @property
    def dpsi(self):
        '''
	scorpy.CorrelationVol.dpsi:
            Size of a voxel in psi-axis
        '''
        return self.dz

    @property
    def qpts(self):
        '''
	scorpy.CorrelationVol.qpts:
            Array of sample points on the q-axis.
        '''
        return self.xpts

    @property
    def psipts(self):
        '''
	scorpy.CorrelationVol.psipts:
            Array of sample points on the psi-axis.
        '''
        return self.zpts


class BlqqVolProps:

    @property
    def nq(self):
        '''
	scorpy.BlqqVol.nx:
            Number of voxels in q-axis directions.
        '''
        return self.nx

    @property
    def nl(self):
        '''
	scorpy.BlqqVol.dq:
            Number of spherical harmonics.
        '''
        return self.nz

    @property
    def qmax(self):
        '''
	scorpy.BlqqVol.qmax:
            Maximum value of q-axes.
        '''
        return self.xmax

    @property
    def dq(self):
        '''
	scorpy.BlqqVol.dq:
            Size of a voxel in q-axis
        '''
        return self.dx

    @property
    def qpts(self):
        '''
	scorpy.CorrelationVol.qpts:
            Array of sample points on the q-axis.
        '''
        return self.xpts


class SphericalVolProps:

    @property
    def nq(self):
        '''
	scorpy.SphericalVol.nq:
            Number of voxels in q-axis directions.
        '''
        return self.nx

    @property
    def ntheta(self):
        '''
	scorpy.SphericalVol.ntheta:
            Number of voxels in theta-axis direction.
        '''
        return self.ny

    @property
    def nphi(self):
        '''
	scorpy.SphericalVol.nphi:
            Number of voxels in phi-axis direction.
        '''
        return self.nz

    @property
    def qmax(self):
        '''
	scorpy.SphericalVol.qmax:
            Maximum value of q-axes.
        '''
        return self.xmax

    @property
    def dq(self):
        '''
	scorpy.SphericalVol.dq:
            Size of a voxel in q-axis
        '''
        return self.dx

    @property
    def dtheta(self):
        '''
	scorpy.SphericalVol.dtheta:
            Size of a voxel in theta-axis
        '''
        return self.dy

    @property
    def dphi(self):
        '''
	scorpy.SphericalVol.dphi:
            Size of a voxel in phi-axis
        '''
        return self.dz

    @property
    def nl(self):
        '''
	scorpy.SphericalVol.nl:
            Number of spherical harmonics to satisfy sampling.
        '''
        return int(self._nl)

    @property
    def qpts(self):
        '''
	scorpy.SphericalVol.qpts:
            Array of sample points on the q-axis.
        '''
        return self.xpts

    @property
    def thetapts(self):
        '''
	scorpy.SphericalVol.thetapts:
            Array of sample points on the theta-axis.
        '''
        return self.ypts

    @property
    def phipts(self):
        '''
	scorpy.SphericalVol.phipts:
            Array of sample points on the phi-axis.
        '''
        return self.zpts


class PadfVolProps:

    @property
    def nr(self):
        '''
	scorpy.PadfVol.nr:
            Number of voxels in r-axis directions.
        '''
        return self.nx

    @property
    def npsi(self):
        '''
	scorpy.PadfVol.nr:
            Number of voxels in psi-axis direction.
        '''
        return self.nz

    @property
    def rmax(self):
        '''
	scorpy.PadfVol.rmax:
            Maximum value of r-axes.
        '''
        return self.xmax

    @property
    def dr(self):
        '''
	scorpy.PadfVol.dr:
            Size of a voxel in r-axis
        '''
        return self.dx

    @property
    def dpsi(self):
        '''
	scorpy.PadfVol.dpsi:
            Size of a voxel in psi-axis
        '''
        return self.dz

    @property
    def nl(self):
        '''
	scorpy.PadfVol.nl:
            Number of spherical harmonics in calculation.
        '''
        return self._nl


    @property
    def rpts(self):
        '''
	scorpy.PadfVol.rpts:
            Array of sample points on the r-axis.
        '''
        return self.xpts

    @property
    def psipts(self):
        '''
	scorpy.PadfVol.psipts:
            Array of sample points on the psi-axis.
        '''
        return self.zpts

    @property
    def wavelength(self):
        '''
	scorpy.PadfVol.wavelength:
            wavelength of experiment, used in PADF calculation.
        '''
        return self._wavelength


