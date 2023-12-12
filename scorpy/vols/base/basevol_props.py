import numpy as np


class BaseVolProps:

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
    def npts(self):
        return (self.nx, self.ny, self.nz)


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
    def mins(self):
        return (self.xmin, self.ymin, self.zmin)


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
    def maxs(self):
        return (self.xmax, self.ymax, self.zmax)

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
    def wraps(self):
        return (self.xwrap, self.ywrap, self.zwrap)

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
    def ds(self):
        return (self.dx, self.dy, self.dz)

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
        assert new_vol.shape == self.vol.shape, f'Cannot replace vols with different shapes\n{new_vol.shape}, {self.vol.shape}'
        self._vol = new_vol

