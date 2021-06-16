import numpy as np






class KlnmHandlerProps:


    @property
    def nq(self):
        return int(self._nq)

    @property
    def nl(self):
        return int(self._nl)

    @property
    def qmax(self):
        return int(self._qmax)


    @property
    def qpts(self):
        return np.linspace(0, self.qmax, self.nq + 1, endpoint=True)[:-1] + self.dq / 2

    @property
    def dq(self):
        return np.abs(self.qmax / self.nq)






