import numpy as np
from ...utils.baseplot import BasePlot


class BaseVolPlot(BasePlot):
    """Visualization utilities for extracting and plotting 2D projections of 3D volumes."""

    def plot_xy(self, **new_kwargs):
        """Plot the x=y cross-section plane profile of the volume matrix.

        Extracts the explicit diagonal profile slice passing through equivalent
        x and y indices across the z dimensions.

        Parameters
        ----------
        **new_kwargs : dict
            Optional visualization styling and execution keyword pass-through configuration.
        """
        im = self.get_xy()

        if 'extent' not in new_kwargs.keys():
            extent = [self.zmin, self.zmax, self.xmin, self.xmax]
            new_kwargs.update({'extent': extent})

        self._plot_2D(im, **new_kwargs)

    def plot_sumax(self, axis: int, nansum: bool = False, **new_kwargs):
        """Integrate data along a designated dimension axis and display the 2D projection.

        Parameters
        ----------
        axis : int
            The coordinate dimension index to compress/integrate along (0, 1, or 2).
        nansum : bool, default False
            If True, uses `np.nansum` to safely ignore NaN values during integration.
            If False, falls back to traditional sum behaviors.
        **new_kwargs : dict
            Optional configuration styling dictionary sent downstream into renderer.
        """
        if nansum:
            im = np.nansum(self.vol, axis=axis)
        else:
            if np.isnan(self.vol).any():
                print('plot_sumax: warning, nan is in vol')
            im = np.sum(self.vol, axis=axis)

        if 'extent' not in new_kwargs.keys():
            if axis % 3 == 0:
                extent = [self.zmin, self.zmax, self.xmin, self.xmax]
            elif axis % 3 == 1:
                extent = [self.zmin, self.zmax, self.xmin, self.xmax]
            else:
                extent = [self.zmin, self.zmax, self.xmin, self.xmax]
            new_kwargs.update({'extent': extent})

        self._plot_2D(im, **new_kwargs)

    def plot_slice(self, axis: int, index: int, **new_kwargs):
        """Extract a single orthogonal slice slice perpendicular to an axis and plot it.

        Parameters
        ----------
        axis : int
            Dimension array indicator perpendicular to target window (0, 1, or 2).
        index : int
            Voxel offset reference point marking location on targeted plane.
        **new_kwargs : dict
            Optional visualization keyword dictionary pass-through.
        """
        if axis % 3 == 0:
            im = self.vol[index, :, :]
            extent = [self.zmin, self.zmax, self.ymin, self.ymax]
        elif axis % 3 == 1:
            im = self.vol[:, index, :]
            extent = [self.xmin, self.xmax, self.zmin, self.zmax]
        else:
            im = self.vol[:, :, index]
            extent = [self.xmin, self.xmax, self.ymin, self.ymax]

        if 'extent' not in new_kwargs.keys():
            new_kwargs.update({'extent': extent})

        self._plot_2D(im, extent_axis=axis, **new_kwargs)
