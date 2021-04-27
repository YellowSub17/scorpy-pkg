

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
    def qmax(self):
        return self.xmax

    @property
    def nq(self):
        return self.nx

    @property
    def npsi(self):
        return self.nz

    @property
    def cvol(self):
        assert False, 'Error: cvol is deprecated, use vol'


    @property
    def ntheta(self):
        assert False, 'Error: ntheta is deprecated, use npsi'


class BlqqVolProps:

    @property
    def qmax(self):
        return self.xmax

    @property
    def nq(self):
        return self.nx

    @property
    def nl(self):
        return self.nz

    @property
    def blvol(self):
        assert False, 'Error: blvol is deprecated, use vol'




class SphericalVolProps:

    @property
    def qmax(self):
        return self.xmax

    @property
    def nq(self):
        return self.nx

    @property
    def ntheta(self):
        return self.ny

    @property
    def nphi(self):
        return self.nz


class PadfVolProps:

    @property
    def rmax(self):
        return self.xmax

    @property
    def nr(self):
        return self.nx

    @property
    def npsi(self):
        return self.nz


