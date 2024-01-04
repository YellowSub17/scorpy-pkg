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

    @property
    def vals_m_mask(self):
        qq, cscs, ll, mm = np.meshgrid(np.arange(self.nq), np.arange(2), np.arange(self.nl), np.arange(self.nl), indexing='ij')
        mask = np.ones(self.vals.shape)
        mask[np.where(mm>ll)] = 0
        return mask


    @vals.setter
    def vals(self, new_vals):
        assert new_vals.shape == self.vals.shape, 'Cannot replace vals with different shapes'
        self._vals = new_vals*self.vals_m_mask





