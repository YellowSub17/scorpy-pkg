import numpy as np

class IqlmHandlerProps:
    """Properties and masking utilities for managing IQLM internal shapes and grids."""

    @property
    def nq(self):
        """The number of sample points along the q-axis.

        Returns
        -------
        int
            The number of sample points.
        """
        return int(self._nq)

    @property
    def nl(self):
        """The number of spherical harmonics degrees in this IqlmHandler (lmax +1).

        Returns
        -------
        int
            The number of spherical harmonic degrees
        """
        return int(self._nl)

    @property
    def qmax(self):
        """The maximum value bound of the q-axis.

        Returns
        -------
        float
            The upper limit of the q-axis range.
        """
        return self._qmax

    @property
    def qmin(self):
        """The minimum value bound of the q-axis.

        Returns
        -------
        float
            The lower limit of the q-axis range.
        """
        return self._qmin

    @property
    def qpts(self):
        """Linearly spaced midpoint coordinates along the q-axis.

        Returns
        -------
        numpy.ndarray
            1D array containing coordinates of the midpoints.
        """
        return np.linspace(self.qmin, self.qmax, self.nq + 1, endpoint=True)[:-1] + self.dq / 2

    @property
    def lpts(self):
        """Integer sequence representing the degrees along the l-axis.

        Returns
        -------
        numpy.ndarray
            1D array containing sequence from 0 up to nl-1.
        """
        return np.arange(0, self.nl)

    @property
    def dq(self):
        """The step size/resolution along the q-axis.

        Returns
        -------
        float
            The absolute distance between consecutive q-points.
        """
        return np.abs((self.qmax - self.qmin) / self.nq)

    @property
    def vals(self):
        """The 4D data array containing Iqlm values. Indices are for q, cosine/sine, degree, order.

        Returns
        -------
        numpy.ndarray
            The 4D data array structured as (nq, 2, nl, nl).
        """
        return self._vals

    @property
    def vals_m_mask(self):
        """A boolean/binary mask ensuring m <= l physically valid constraints.

        Zeroes out any elements where the order (m) exceeds the degree (l).

        Returns
        -------
        numpy.ndarray
            A 4D binary mask matching the shape of `vals`.
        """
        qq, cscs, ll, mm = np.meshgrid(np.arange(self.nq), np.arange(2), np.arange(self.nl), np.arange(self.nl), indexing='ij')
        mask = np.ones(self.vals.shape)
        mask[np.where(mm > ll)] = 0
        return mask

    @vals.setter
    def vals(self, new_vals):
        """Set new data values while enforcing array shape consistency and the m <= l mask.

        Parameters
        ----------
        new_vals : numpy.ndarray
            The new array to replace the existing values. Must match `vals.shape`.

        Raises
        ------
        AssertionError
            If the shape of `new_vals` does not match the shape of `self.vals`.
        """
        assert new_vals.shape == self.vals.shape, 'Cannot replace vals with different shapes'
        self._vals = new_vals * self.vals_m_mask
