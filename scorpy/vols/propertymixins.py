

class VolProperties:



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

   

class CorrelationVolProperties:

    @property
    def qmax(self):
        return self._xmax

    @property
    def nq(self):
        return self._nx

    @property
    def npsi(self):
        return self._nz

    @property
    def cvol(self):
        return self._vol

    @cvol.setter
    def cvol(self, new_vol):
        self.vol = new_vol

    @property
    def ntheta(self):
        print('warning: ntheta is deprecated. all hail npsi')
        return self._nz



