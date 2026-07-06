import numpy as np
import copy
import pyshtools as pysh
import matplotlib.pyplot as plt

from .iqlmhandler_props import IqlmHandlerProps
from .iqlmhandler_plot import IqlmHandlerPlot

class IqlmHandler(IqlmHandlerProps, IqlmHandlerPlot):
    """Handler for transforming, evaluating, and plotting data mapped to spherical harmonics.

    Parameters
    ----------
    nq : int
        Number of grid points on the q-axis.
    nl : int
        Maximum degree limit for spherical harmonics.
    qmax : float
        Maximum bound of the q-axis range.
    qmin : float, optional
        Minimum bound of the q-axis range. Default is 0.
    """

    def __init__(self, nq, nl, qmax, qmin=0):
        self._nq = nq
        self._nl = nl
        self._qmax = qmax
        self._qmin = qmin
        self._vals = np.zeros((self.nq, 2, self.nl, self.nl))

    def copy(self):
        """Create a deep copy of the current IqlmHandler instance.

        Returns
        -------
        IqlmHandler
            A fully decoupled duplicate instance of the current object.
        """
        return copy.deepcopy(self)

    def fill_from_sphv(self, sphv):
        """Populate values by expanding a SphericalVol volume into spherical harmonic coefficients.

        Parameters
        ----------
        sphv : SphericalVol-like object
            An object holding a 3D spherical volume. Must share matching `qmax`, 
            `qmin`, and `nq` configuration properties with this handler.

        Raises
        ------
        AssertionError
            If there is a dimension or spatial bounds mismatch between `sphv` and this handler.
        """
        assert sphv.qmax == self.qmax, 'IqlmHandler and SphericalVol have different qmax'
        assert sphv.qmin == self.qmin, 'IqlmHandler and SphericalVol have different qmin'
        assert sphv.nq == self.nq, 'IqlmHandler and SphericalVol have different nq'

        for iq, q_slice in enumerate(sphv.vol):
            pysh_grid = pysh.shclasses.DHRealGrid(q_slice)
            coeffs = pysh_grid.expand(csphase=1).coeffs[:, :self.nl, :self.nl]
            self.vals[iq] = coeffs

    def calc_knlmp(self, bl_l, nl=None):
        """Calculate and normalize modified k-space coefficients knlm'.

        Parameters
        ----------
        bl_l : numpy.ndarray
            Eigenvalues of the Blqq matrices indexed by `[q_ind, l]`.
        nl : int, optional
            The maximum degree index up to which the calculation is executed.
            If None, defaults to `self.nl`.
        """
        if nl is None:
            nl = self.nl

        for q_ind in range(self.nq):
            for l in range(0, nl):
                ned = bl_l[q_ind, l]
                km = np.abs(self.vals[q_ind, :, l, :])**2
                donk = np.sum(km)
                if donk == 0:
                    ned = 1
                    donk = 1
                self.vals[q_ind, :, l, :] *= np.sqrt(np.abs(ned / donk))

    def calc_knlm(self, bl_u, nl=None):
        """Transform spherical harmonics iqlm to k-space coefficients knlm via dot product projection.

        Parameters
        ----------
        bl_u : numpy.ndarray
            Eigenvectors of the Blqq matrices indexed by `[q, q_prime, l]`.
        nl : int, optional
            The maximum degree index up to which the calculation is executed.
            If None, defaults to `self.nl`.
        """
        new_vals = np.zeros((self.nq, 2, self.nl, self.nl))

        if nl is None:
            nl = self.nl

        for cs in range(0, 2):
            for l in range(0, nl):
                ul_nq = bl_u[:, :, l]
                for m in range(l + 1):
                    ilm_q = self.vals[:, cs, l, m]
                    x = np.dot(ilm_q, ul_nq)
                    new_vals[:, cs, l, m] = x
        self.vals = new_vals

    def calc_iqlmp(self, bl_u, nl=None):
        """Transform k-space coefficients knlm back into spherical harmonics iqlm.

        Parameters
        ----------
        bl_u : numpy.ndarray
            Eigenvectors of the Blqq matrices indexed by `[q, q_prime, l]`.
        nl : int, optional
            The maximum degree index up to which the calculation is executed.
            If None, defaults to `self.nl`.
        """
        new_vals = np.zeros((self.nq, 2, self.nl, self.nl))

        if nl is None:
            nl = self.nl

        for cs in range(0, 2):
            for l in range(0, nl):
                ul_nq = bl_u[:, :, l]
                for m in range(l + 1):
                    kp = self.vals[:, cs, l, m]
                    ku = np.dot(ul_nq, kp)
                    new_vals[:, cs, l, m] = ku
        self.vals = new_vals
