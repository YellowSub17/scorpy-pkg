import numpy as np






class IqlmHandlerProps:


    @property
    def nq(self):
        return int(self._nq)

    @property
    def nl(self):
        return int(self._nl)

    @property
    def qmax(self):
        return self._qmax

    @property
    def qmin(self):
        return self._qmin

    @property
    def qpts(self):
        return np.linspace(self.qmin, self.qmax, self.nq + 1, endpoint=True)[:-1] + self.dq / 2

    @property
    def lpts(self):
        return np.arange(0,self.nl)

    @property
    def dq(self):
        return np.abs( (self.qmax-self.qmin) / self.nq)

    @property
    def vals(self):
        return self._vals

    @vals.setter
    def vals(self, new_vals):
        assert new_vals.shape == self.vals.shape, 'Cannot replace vals with different shapes'
        self._vals = new_vals


    @property
    def inc_odds(self):
        return self._inc_odds



