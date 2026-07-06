
class CorrelationVolProps:
    """
    Mixin class providing convenience properties for CorrelationVol.

    Exposes the underlying ``BaseVol`` x/z-axis attributes under names
    specific to the correlation volume's q and psi axes.
    """

    @property
    def nq(self):
        """
        Number of voxels in the q-axis directions.

        Returns
        -------
        int
            Number of voxels along each q-axis.
        """
        return self.nx

    @property
    def npsi(self):
        """
        Number of voxels in the psi-axis direction.

        Returns
        -------
        int
            Number of voxels along the psi-axis.
        """
        return self.nz

    @property
    def qmax(self):
        """
        Maximum value of the q-axes.

        Returns
        -------
        float
            Maximum q value.
        """
        return self.xmax

    @property
    def qmin(self):
        """
        Minimum value of the q-axes.

        Returns
        -------
        float
            Minimum q value.
        """
        return self.xmin

    @property
    def psimax(self):
        """
        Maximum value of the psi axis.

        Returns
        -------
        float
            Maximum psi value.
        """
        return self.zmax

    @property
    def psimin(self):
        """
        Minimum value of the psi axis.

        Returns
        -------
        float
            Minimum psi value.
        """
        return self.zmin



    @property
    def dq(self):
        """
        Size of a voxel in the q-axis.

        Returns
        -------
        float
            Voxel size along the q-axis.
        """
        return self.dx

    @property
    def dpsi(self):
        """
        Size of a voxel in the psi-axis.

        Returns
        -------
        float
            Voxel size along the psi-axis.
        """
        return self.dz

    @property
    def qpts(self):
        """
        Sample points on the q-axis.

        Returns
        -------
        numpy.ndarray
            Array of sample points along the q-axis.
        """
        return self.xpts

    @property
    def psipts(self):
        """
        Sample points on the psi-axis.

        Returns
        -------
        numpy.ndarray
            Array of sample points along the psi-axis.
        """
        return self.zpts

    @property
    def cos_sample(self):
        """
        Whether the psi-axis is sampled in cosine space.

        Returns
        -------
        bool
            True if psi is sampled as cos(psi), False if sampled as psi
            in radians.
        """
        return self._cos_sample

    @property
    def inc_self_corr(self):
        """
        Whether self-correlation (q1 == q2, psi == 0) terms are included.

        Returns
        -------
        bool
            True if self-correlation terms are included.
        """
        return self._inc_self_corr
