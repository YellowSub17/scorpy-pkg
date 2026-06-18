import numpy as np


class BaseVolProps:
    """Properties and geometric descriptors for a 3D volumetric dataset.

    This class provides properties to read shape dimensions, spatial boundaries,
    voxel resolution, coordinate grids, and wrapping configurations for a 3D volume.
    """

    @property
    def nx(self) -> int:
        """Number of voxels in the x-axis direction.

        Returns
        -------
        int
            Voxel count along x.
        """
        return int(self._nx)

    @property
    def ny(self) -> int:
        """Number of voxels in the y-axis direction.

        Returns
        -------
        int
            Voxel count along y.
        """
        return int(self._ny)

    @property
    def nz(self) -> int:
        """Number of voxels in the z-axis direction.

        Returns
        -------
        int
            Voxel count along z.
        """
        return int(self._nz)

    @property
    def npts(self) -> tuple[int, int, int]:
        """Shape profile grid size across all dimensions.

        Returns
        -------
        tuple of int
            Grid dimensions ordered as (nx, ny, nz).
        """
        return (self.nx, self.ny, self.nz)

    @property
    def xmin(self) -> float:
        """Minimum physical boundary coordinate of the x-axis.

        Returns
        -------
        float
            Minimum value of x.
        """
        return self._xmin

    @property
    def ymin(self) -> float:
        """Minimum physical boundary coordinate of the y-axis.

        Returns
        -------
        float
            Minimum value of y.
        """
        return self._ymin

    @property
    def zmin(self) -> float:
        """Minimum physical boundary coordinate of the z-axis.

        Returns
        -------
        float
            Minimum value of z.
        """
        return self._zmin

    @property
    def mins(self) -> tuple[float, float, float]:
        """Minimum physical bounds across all dimensions.

        Returns
        -------
        tuple of float
            Minimum boundary values ordered as (xmin, ymin, zmin).
        """
        return (self.xmin, self.ymin, self.zmin)

    @property
    def xmax(self) -> float:
        """Maximum physical boundary coordinate of the x-axis.

        Returns
        -------
        float
            Maximum value of x.
        """
        return self._xmax

    @property
    def ymax(self) -> float:
        """Maximum physical boundary coordinate of the y-axis.

        Returns
        -------
        float
            Maximum value of y.
        """
        return self._ymax

    @property
    def zmax(self) -> float:
        """Maximum physical boundary coordinate of the z-axis.

        Returns
        -------
        float
            Maximum value of z.
        """
        return self._zmax

    @property
    def maxs(self) -> tuple[float, float, float]:
        """Maximum physical bounds across all dimensions.

        Returns
        -------
        tuple of float
            Maximum boundary values ordered as (xmax, ymax, zmax).
        """
        return (self.xmax, self.ymax, self.zmax)

    @property
    def xwrap(self) -> bool:
        """Indicates if the x-axis boundary configuration is periodic.

        Returns
        -------
        bool
            True if periodic/wrapped, False otherwise.
        """
        return self._xwrap

    @property
    def ywrap(self) -> bool:
        """Indicates if the y-axis boundary configuration is periodic.

        Returns
        -------
        bool
            True if periodic/wrapped, False otherwise.
        """
        return self._ywrap

    @property
    def zwrap(self) -> bool:
        """Indicates if the z-axis boundary configuration is periodic.

        Returns
        -------
        bool
            True if periodic/wrapped, False otherwise.
        """
        return self._zwrap

    @property
    def wraps(self) -> tuple[bool, bool, bool]:
        """Periodic wrapping status profile across all dimensions.

        Returns
        -------
        tuple of bool
            Wrapping statuses ordered as (xwrap, ywrap, zwrap).
        """
        return (self.xwrap, self.ywrap, self.zwrap)

    @property
    def dx(self) -> float:
        """Voxel stride grid spacing size along the x-axis.

        Returns
        -------
        float
            Grid interval scale size along x.
        """
        return np.abs((self.xmax - self.xmin) / (self.nx))

    @property
    def dy(self) -> float:
        """Voxel stride grid spacing size along the y-axis.

        Returns
        -------
        float
            Grid interval scale size along y.
        """
        return np.abs((self.ymax - self.ymin) / (self.ny))

    @property
    def dz(self) -> float:
        """Voxel stride grid spacing size along the z-axis.

        Returns
        -------
        float
            Grid interval scale size along z.
        """
        return np.abs((self.zmax - self.zmin) / (self.nz))

    @property
    def ds(self) -> tuple[float, float, float]:
        """Resolution delta grid intervals across all dimensions.

        Returns
        -------
        tuple of float
            Spatial voxel resolutions ordered as (dx, dy, dz).
        """
        return (self.dx, self.dy, self.dz)

    @property
    def xpts(self) -> np.ndarray:
        """Array of physical sample coordinates along the x-axis.

        The location spacing matches centered coordinates depending on wrapping conditions.

        Returns
        -------
        np.ndarray
            1D array of sample location points.
        """
        if self.xwrap:
            return np.linspace(self.xmin, self.xmax, self.nx, endpoint=False)
        else:
            return np.linspace(self.xmin, self.xmax, self.nx + 1, endpoint=True)[:-1] + self.dx / 2

    @property
    def ypts(self) -> np.ndarray:
        """Array of physical sample coordinates along the y-axis.

        The location spacing matches centered coordinates depending on wrapping conditions.

        Returns
        -------
        np.ndarray
            1D array of sample location points.
        """
        if self.ywrap:
            return np.linspace(self.ymin, self.ymax, self.ny, endpoint=False)
        else:
            return np.linspace(self.ymin, self.ymax, self.ny + 1, endpoint=True)[:-1] + self.dy / 2

    @property
    def zpts(self) -> np.ndarray:
        """Array of physical sample coordinates along the z-axis.

        The location spacing matches centered coordinates depending on wrapping conditions.

        Returns
        -------
        np.ndarray
            1D array of sample location points.
        """
        if self.zwrap:
            return np.linspace(self.zmin, self.zmax, self.nz, endpoint=False)
        else:
            return np.linspace(self.zmin, self.zmax, self.nz + 1, endpoint=True)[:-1] + self.dz / 2

    @property
    def comp(self) -> bool:
        """Indicates whether the data buffer uses complex elements.

        Returns
        -------
        bool
            True if complex type arrays are declared, False if standard real floating point.
        """
        return self._comp

    @property
    def vol(self) -> np.ndarray:
        """The core internal numeric array storage block.

        Returns
        -------
        np.ndarray
            The 3D volume numpy array dataset.
        """
        return self._vol

    @vol.setter
    def vol(self, new_vol: np.ndarray):
        """Replaces the internal matrix with another array buffer block.

        Parameters
        ----------
        new_vol : np.ndarray
            Target incoming dataset replacement buffer.

        Raises
        ------
        AssertionError
            If dimensions profile shapes do not match current instance settings.
        """
        assert new_vol.shape == self.vol.shape, f'Cannot replace vols with different shapes\n{new_vol.shape}, {self.vol.shape}'
        self._vol = new_vol
