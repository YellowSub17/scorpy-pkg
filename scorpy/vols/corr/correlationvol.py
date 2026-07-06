from scipy import special
import numpy as np
import time

from ...utils.decorator_funcs import verbose_dec

from ..base.basevol import BaseVol
from .correlationvol_props import CorrelationVolProps
from .correlationvol_plot import CorrelationVolPlot
from .correlationvol_saveload import CorrelationVolSaveLoad
from .correlationvol_fill import CorrelationVolFill
from .correlationvol_corr import CorrelationVolCorr


class CorrelationVol(BaseVol,               #Parent Vol Class
                     CorrelationVolProps,   #Protected Properties
                     CorrelationVolSaveLoad,#Save and Load functionality
                     CorrelationVolPlot,    #Plotting
                     CorrelationVolFill,    #Fill from other objects
                     CorrelationVolCorr,     #Correlation scattering vectors
                    ):
    """
    A representation of the scattering correlation function.

    Attributes
    ----------
    nq : int
        Number of voxels in the q-axis directions.
    npsi : int
        Number of voxels in the psi-axis direction.
    qmax : float
        Maximum value of the q-axes.
    qmin : float
        Minimum value of the q-axes.
    dq : float
        Size of a voxel in the q-axis.
    dpsi : float
        Size of a voxel in the psi-axis.
    qpts : numpy.ndarray
        Array of sample points on the q-axis.
    psipts : numpy.ndarray
        Array of sample points on the psi-axis.

    Methods
    -------
    fill_from_cif(cif, nchunks=1, verbose=0)
        Fill the CorrelationVol from a CifData object.
    fill_from_blqq(blqq, inc_odds=True, verbose=0)
        Fill the CorrelationVol from a BlqqVol object.
    fill_from_peakdata(pk, verbose=0)
        Fill the CorrelationVol from a PeakData object.
    correlate_2D(q, t, I, verbose=0)
        Correlate a set of 2D (q, theta) scattering peaks.
    correlate_3D(xyz, I, nchunks=1, verbose=0)
        Correlate a set of 3D scattering vectors.
    plot_q1q2(...)
        Plot a q1-q2 slice of the correlation volume.
    """

    def __init__(self, nq=100, npsi=180, qmax=1, qmin=0, cos_sample=True,  path=None):
        """
        Initialize a CorrelationVol.

        Parameters
        ----------
        nq : int, optional
            Number of voxels in each q-axis direction (default 100).
            Ignored if ``path`` is given.
        npsi : int, optional
            Number of voxels in the psi-axis direction (default 180).
            Ignored if ``path`` is given.
        qmax : float, optional
            Maximum value of the q-axes (default 1). Ignored if ``path``
            is given.
        qmin : float, optional
            Minimum value of the q-axes (default 0). Ignored if ``path``
            is given.
        cos_sample : bool, optional
            Whether to sample the psi-axis in cosine space, i.e. from
            -1 to 1, rather than in radians from 0 to pi (default True).
            Ignored if ``path`` is given.
        path : str, optional
            Path to a saved CorrelationVol config to load from. If
            given, all other parameters are ignored (default None).
        """

        if path is not None:
            BaseVol.__init__(self, path=path)
        else:

            if cos_sample:
                BaseVol.__init__(self, nq, nq, npsi, qmin, qmin, -1, qmax, qmax, 1, False, False, False, comp=False, path=path)
            else:
                BaseVol.__init__(self, nq, nq, npsi, qmin, qmin, 0, qmax, qmax, np.pi, False, False, False, comp=False, path=path)

            self._cos_sample = cos_sample

        self.plot_q1q2 = self.plot_xy



    def rm_selfcorr(self):
        """
        Remove the self-correlation terms from the correlation volume.

        Zeros the ``self.vol`` entries where q1 == q2 and psi == 0 (or
        psi == 1 if ``cos_sample`` is True) for every q index.

        Returns
        -------
        None
            ``self.vol`` is updated in place.
        """
        nq_a = np.arange(0, self.nq)

        if self.cos_sample:
            self.vol[nq_a, nq_a, -1] = 0
        else:
            self.vol[nq_a, nq_a, 0] = 0


    def correction2d(self, times=True):
        """
        Apply (or remove) the 2D solid-angle correction factor to the volume.

        Multiplies (or divides) ``self.vol`` by ``sin(psi) * q1 * q2``
        at every voxel, computed from a meshgrid of the q and psi sample
        points.

        Parameters
        ----------
        times : bool, optional
            If True, multiply ``self.vol`` by the correction factor; if
            False, divide by it (default True).

        Returns
        -------
        None
            ``self.vol`` is updated in place.
        """

        q1q1, q2q2, psipsi = np.meshgrid(self.qpts, self.qpts, self.psipts)

        if self.cos_sample:
            factor = np.sin(np.arccos(psipsi))*q1q1*q2q2
        else:
            factor = np.sin(psipsi)*q1q1*q2q2

        if times:
            self.vol *=factor
        else:
            self.vol /=factor



    def qq_correction(self, times=True):
        """
        Apply (or remove) the q1*q2 correction factor to the volume.

        Multiplies (or divides) ``self.vol`` by ``q1 * q2`` at every
        voxel, computed from a meshgrid of the q sample points.

        Parameters
        ----------
        times : bool, optional
            If True, multiply ``self.vol`` by the correction factor; if
            False, divide by it (default True).

        Returns
        -------
        None
            ``self.vol`` is updated in place.
        """
        q1q1, q2q2, _  = np.meshgrid(self.qpts, self.qpts, self.psipts)

        if times:
            self.vol *= q1q1*q2q2
        else:
            self.vol /= q1q1*q2q2
