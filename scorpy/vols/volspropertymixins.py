

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
    def dx(self):
        return (self.xmax - self.xmin) / self.nx

    @property
    def dy(self):
        return (self.ymax - self.ymin) / self.ny

    @property
    def dz(self):
        return (self.zmax - self.zmin) / self.nz

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

    # @property
    # def xpts(self):
        # return np.linspace(self.xmin, self.xmax, self.nx)

    # @property
    # def ypts(self):
        # return np.linspace(self.ymin, self.ymax, self.ny)

    # @property
    # def zpts(self):
        # return np.linspace(self.zmin, self.zmax, self.nz)


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
