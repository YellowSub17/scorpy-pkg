
import numpy as np
from ..utils.baseplot import BasePlot

class IqlmHandlerPlot(BasePlot):
    """Plotting utilities for the IQLM data structure."""

    def plot_q(self, q_ind, cs=None, **new_kwargs):
        """Plot the data at a specific q-index as a 2D image over L and M.

        Parameters
        ----------
        q_ind : int
            The index along the q-axis to plot.
        cs : int, optional
            The component index (e.g., 0 for cosine, 1 for sine). If None, 
            combines positive and negative components along the M-axis.
        **new_kwargs : dict, optional
            Additional keyword arguments to override or complement the default 
            plotting parameters (`xlabel`, `ylabel`, `extent`).
        """
        kwargs = {  'xlabel':'M',
                    'ylabel':'L',
                    'extent':[-self.nl, self.nl, 0,  self.nl]}
        kwargs.update(new_kwargs)

        if cs is not None:
            im = self.vals[q_ind, cs, :, :]
            self._plot_2D(im, **new_kwargs)
        else:
            impos = self.vals[q_ind, 0, :, :]
            imneg = self.vals[q_ind, 1, :, :0:-1]
            im = np.concatenate([imneg, impos], 1)
            self._plot_2D(im, **kwargs)

    def plot_l(self, l, cs=None, **new_kwargs):
        """Plot the data at a specific l-degree as a 2D image over q and M.

        Parameters
        ----------
        l : int
            The degree index along the l-axis to plot.
        cs : int, optional
            The component index (e.g., 0 for cosine, 1 for sine). If None, 
            combines positive and negative components along the M-axis.
        **new_kwargs : dict, optional
            Additional keyword arguments to override or complement the default 
            plotting parameters (`xlabel`, `ylabel`, `extent`).
        """
        kwargs = {  'xlabel':'M',
                    'ylabel':'q',
                    'extent':[-self.nl, self.nl, 0,  self.qmax]}
        kwargs.update(new_kwargs)

        if cs is not None:
            im = self.vals[:, cs, l,  :]
            self._plot_2D(im.T, **kwargs)
        else:
            impos = self.vals[:, 0, l, :]
            imneg = self.vals[:, 1, l, :0:-1]
            im = np.concatenate([imneg.T, impos.T], 0)
            self._plot_2D(im.T, **kwargs)
