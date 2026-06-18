import numpy as np
import copy
import scipy
import matplotlib.pyplot as plt

from .basevol_props import BaseVolProps
from .basevol_saveload import BaseVolSaveLoad
from .basevol_plot import BaseVolPlot
from .basevol_proc import BaseVolProc
from ...utils.convert_funcs import index_xs


class BaseVol(BaseVolProps, BaseVolPlot, BaseVolSaveLoad, BaseVolProc):
    """A comprehensive representation of an arbitrary 3D volume or spatial function.

    Combines metadata management properties, mathematical processing operations,
    file I/O handlers, and 2D visualization pipelines.

    Parameters
    ----------
    nx, ny, nz : int, default 10
        Voxel resolution profile counts matching grid dimensions.
    xmin, ymin, zmin : float, default 0
        Minimum physical dimension boundaries tracking baseline configurations.
    xmax, ymax, zmax : float, default 1
        Maximum physical boundaries tracking grid coordinates.
    xwrap, ywrap, zwrap : bool, default False
        Periodic boundary wrapping status conditions indicators.
    comp : bool, default False
        If True, initializes internal data buffers using complex floating numbers.
    path : str or Path, optional
        Target tracking file destination to load and populating instances immediately.
    """

    def __init__(self, nx: int = 10, ny: int = 10, nz: int = 10,
                 xmin: float = 0, ymin: float = 0, zmin: float = 0,
                 xmax: float = 1, ymax: float = 1, zmax: float = 1,
                 xwrap: bool = False, ywrap: bool = False, zwrap: bool = False,
                 comp: bool = False, path=None):

        if path is not None:
            self._load(path)
        else:
            self._nx = nx
            self._ny = ny
            self._nz = nz

            self._xmin = xmin
            self._ymin = ymin
            self._zmin = zmin

            self._xmax = xmax
            self._ymax = ymax
            self._zmax = zmax

            self._xwrap = xwrap
            self._ywrap = ywrap
            self._zwrap = zwrap

            self._comp = comp

            if self.comp:
                self._vol = np.zeros((nx, ny, nz)).astype(np.complex64)
            else:
                self._vol = np.zeros((nx, ny, nz))

    def copy(self):
        """Generate an independent deep copy of the active volumetric object.

        Returns
        -------
        BaseVol
            A deep copy instance replica containing identical elements.
        """
        v = copy.deepcopy(self)
        return v

    def get_indices(self, pts: np.ndarray, axis: int = 0) -> np.ndarray:
        """Map raw coordinate points to their closest corresponding integer array grid indices.

        Parameters
        ----------
        pts : np.ndarray
            Target array pool matching spatial location components.
        axis : int, default 0
            Target tracking dimension reference identifier (0 for x, 1 for y, 2 for z).

        Returns
        -------
        np.ndarray
            Mapped integer index positions array pool records.
        """
        inds = index_xs(pts, self.mins[axis], self.maxs[axis], self.npts[axis], self.wraps[axis])
        return inds

    def sum_into_vol(self, x_inds: np.ndarray, y_inds: np.ndarray, z_inds: np.ndarray, vals: np.ndarray, sym: bool = False, verbose: int = 0):
        """Incorporate and accumulate external scattered values directly into the 3D grid.

        Parameters
        ----------
        x_inds : np.ndarray
            Array collection tracking grid offset indices along x.
        y_inds : np.ndarray
            Array collection tracking grid offset indices along y.
        z_inds : np.ndarray
            Array collection tracking grid offset indices along z.
        vals : np.ndarray
            Numeric components accumulation tracking data payloads.
        sym : bool, default False
            If True, applies duplicate operations to enforce symmetric accumulation behavior.
        verbose : int, default 0
            Controls console runtime print updates status settings.
        """
        for i, (x_ind, y_ind, z_ind, val) in enumerate(zip(x_inds, y_inds, z_inds, vals)):
            print(f'{i}', end='\r')
            self.vol[x_ind, y_ind, z_ind] += val
            if sym:
                self.vol[x_ind, y_ind, z_ind] += val

    def crop(self, xi: int, yi: int, zi: int, xf: int, yf: int, zf: int):
        """Extract a sub-volume box window and build a new scaled BaseVol object.

        Parameters
        ----------
        xi, yi, zi : int
            Lower coordinate bounds tracking start markers.
        xf, yf, zf : int
            Upper boundary offsets marking slicing terminations.

        Returns
        -------
        BaseVol
            A newly initialized BaseVol container managing the extracted sub-volume.
        """
        cropped_arr = self.vol[xi:xf, yi:yf, zi:zf]

        new_xmin, new_xmax = self.xpts[xi], self.xpts[xf]
        new_ymin, new_ymax = self.ypts[yi], self.ypts[yf]
        new_zmin, new_zmax = self.zpts[zi], self.zpts[zf]

        new_nx = xf - xi
        new_ny = yf - yi
        new_nz = zf - zi
        print(f'{new_nx=} {new_ny=} {new_nz=}')

        # FIXED: Changed dy/dz calculations to use respective spacing instead of hardcoded dx
        new_vol = BaseVol(new_nx, new_ny, new_nz,
                          new_xmin - self.dx / 2, new_ymin - self.dy / 2, new_zmin - self.dz / 2,
                          new_xmax - self.dx / 2, new_ymax - self.dy / 2, new_zmax - self.dz / 2,
                          False, False, False, self.comp)

        new_vol.vol = cropped_arr
        return new_vol

    def cosinesim(self, v) -> float:
        """Compute the Cosine Similarity metric against another matching volume array.

        Parameters
        ----------
        v : BaseVol
            Target volumetric object container used during matching checks.

        Returns
        -------
        float
            Computed similarity calculation values falling within [-1.0, 1.0].

        Raises
        ------
        AssertionError
            If comparing instances with mismatching shapes.
        """
        assert (self.nx, self.ny, self.nz) == (v.nx, v.ny, v.nz), 'Vols not the same shape.'
        v1f, v2f = self.vol.flatten(), v.vol.flatten()
        sim = np.dot(v1f, v2f) / (np.linalg.norm(v1f) * np.linalg.norm(v2f))
        return sim

    def get_eig(self, herm: bool = False, inc_odds: bool = True) -> tuple[np.ndarray, np.ndarray]:
        """Calculate eigenvectors and eigenvalues slice-by-slice along the z-axis.

        Parameters
        ----------
        herm : bool, default False
            If True, optimizes extraction targeting internal Hermitian matrix assumptions.
        inc_odds : bool, default True
            If False, skips every other odd z-slice index step.

        Returns
        -------
        lams : np.ndarray
            Matrix records holding real eigenvalue outputs tracker.
        us : np.ndarray
            Calculated array tracks mapping structural eigenvectors.
        """
        dtype, eig_fn = ((np.float64, np.linalg.eigh) if herm else (np.complex64, np.linalg.eig))
        zskip = 1 if inc_odds else 2

        lams = np.zeros((self.nx, self.nz), dtype=dtype)
        us = np.zeros((self.nx, self.ny, self.nz), dtype=dtype)

        for z in range(0, self.nz, zskip):
            lam, u = eig_fn(self.vol[..., z])
            lams[:, z] = lam
            us[:, :, z] = u
        return np.real(lams), np.real(us)

    def get_xy(self) -> np.ndarray:
        """Extract the structural diagonal x=y plane across the tracking spatial volume.

        Requires identical dimensions profiles along both x and y spatial parameters.

        Returns
        -------
        np.ndarray
            A 2D matrix projection containing extracted diagonal slices.

        Raises
        ------
        AssertionError
            If x and y grid boundaries or wrapping profiles are not identical.
        """
        assert self.nx == self.ny, 'vol.nx != vol.ny, cannot retrieve x=y plane of vol.'
        assert self.xmax == self.ymax, 'vol.xmax != vol.ymax, cannot retrieve x=y plane of vol.'
        assert self.xmin == self.ymin, 'vol.xmin != vol.ymin, cannot retrieve x=y plane of vol.'
        assert self.xwrap == self.ywrap, 'vol.xwrap != vol.ywrap, cannot retrieve x=y plane of vol.'

        xy = np.zeros((self.nx, self.nz))
        for xi in range(self.nx):
            xy[xi, :] = self.vol[xi, xi, :]
        return xy

    def get_index(self, x: float = None, y: float = None, z: float = None) -> int | None:
        """Find the closest integer coordinate grid index matching a physical coordinate value.

        Parameters
        ----------
        x : float, optional
            Physical lookup value target location tracking x components.
        y : float, optional
            Physical lookup value target location tracking y components.
        z : float, optional
            Physical lookup value target location tracking z components.

        Returns
        -------
        int or None
            The closest array index match found. Returns None if no input parameter is supplied.
        """
        if x is not None:
            xloc = np.where(np.abs(self.xpts - x) == np.min(np.abs(self.xpts - x)))
            return xloc[0][0]
        if y is not None:
            yloc = np.where(np.abs(self.ypts - y) == np.min(np.abs(self.ypts - y)))
            return yloc[0][0]
        if z is not None:
            zloc = np.where(np.abs(self.zpts - z) == np.min(np.abs(self.zpts - z)))
            return zloc[0][0]

        print('No value given')
        return None

    def get_integrated_xy_line(self, xy_lower: float | int, xy_upper: float | int, ind: bool = False) -> np.ndarray:
        """Extract a line projection across the diagonal x=y plane by integrating within bounds.

        Parameters
        ----------
        xy_lower : float or int
            Lower spatial boundary track or integer array index position.
        xy_upper : float or int
            Upper spatial boundary track or integer array index position.
        ind : bool, default False
            If True, treats the input bounds directly as integer indices instead of coordinates.

        Returns
        -------
        np.ndarray
            Integrated array values tracking line segments.
        """
        xy = self.get_xy()

        if not ind:
            xy_lower_ind = self.get_index(x=xy_lower)
            xy_upper_ind = self.get_index(x=xy_upper)
        else:
            xy_lower_ind = xy_lower
            xy_upper_ind = xy_upper

        inte = np.sum(xy[xy_lower_ind:xy_upper_ind, :], axis=0)
        return inte

    def ls_pts(self, thresh: float = 0.0, inds: bool = False) -> np.ndarray:
        """Filter and list data points that exceed a specified intensity threshold.

        Parameters
        ----------
        thresh : float, default 0.0
            Minimum intensity value used as a threshold filter.
        inds : bool, default False
            If True, the first three columns of the output will contain raw integer array indices.
            If False, columns contain converted physical spatial coordinates instead.

        Returns
        -------
        np.ndarray
            An N x 4 array. The first three columns represent positions (x, y, z),
            and the final column stores the signal intensity at that position.
        """
        loc = np.where(self.vol > thresh)
        npts = loc[0].size

        pts = np.zeros((npts, 4))
        pts[:, -1] = self.vol[loc]

        if not inds:
            pts[:, 0] = self.xpts[loc[0]]
            pts[:, 1] = self.ypts[loc[1]]
            pts[:, 2] = self.zpts[loc[2]]
        else:
            pts[:, 0] = loc[0].astype(int)
            pts[:, 1] = loc[1].astype(int)
            pts[:, 2] = loc[2].astype(int)

        return pts

    def integrate_region(self, ptx: float, pty: float, ptz: float, dx: float, dy: float, dz: float, shape: str = 'disk') -> tuple[float, tuple]:
        """Calculate spatial regional integrations inside shapes surrounding a target coordinate point.

        Parameters
        ----------
        ptx, pty, ptz : float
            Center coordinates of the targeted integration window.
        dx, dy, dz : float
            Symmetric spatial tracking range dimensions offsets profile radius scales.
        shape : {'disk', 'rect'}, default 'disk'
            The spatial profile shape geometry template to use for integration.

        Returns
        -------
        total_sum : float
            Accumulated regional intensity value summation.
        loc : tuple of np.ndarray
            Numpy index masking references tracking localized elements.
        """
        if shape == 'disk':
            xx, yy, zz = np.meshgrid(self.xpts, self.ypts, self.zpts)
            rxx, ryy, rzz = xx - ptx, yy - pty, np.abs(zz - ptz)
            rxy = np.sqrt(rxx**2 + ryy**2)
            loc = np.where(np.logical_and(rxy <= dx, rzz <= dz))

        if shape == 'rect':
            xx, yy, zz = np.meshgrid(self.xpts, self.ypts, self.zpts)
            rxx, ryy, rzz = np.abs(xx - ptx), np.abs(pty - pty), np.abs(zz - ptz)
            xandy = np.logical_and(rxx <= dx, ryy <= dy)
            loc = np.where(np.logical_and(xandy, rzz <= dz))

        return self.vol[loc].sum(), loc
