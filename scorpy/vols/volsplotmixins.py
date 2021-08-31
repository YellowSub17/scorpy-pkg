import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
import matplotlib.cm as cm
from matplotlib.colors import Normalize


class VolPlot:

    def get_extent(self, axis):
        '''scorpy.Vol.get_extent():
        When plotting a slice of the volume, get the bounds of the figure.

        ...
        Arguments:
            axis : int
                The axis perpendicular to plot slice.
        Returns:
            extents : list
                List of lower vertical, upper vertical, lower horizontal,
                higher horizontal bounds for the plot.
        ...
        '''
        if axis == 0:
            return [self.zmin, self.zmax, self.ymin, self.ymax]
        elif axis == 1:
            return [self.zmin, self.zmax, self.xmin, self.xmax]
        else:
            return [self.xmin, self.xmax, self.ymin, self.ymax]



    # def _plot_2D(self, im, fig=None, axes=None, log=False, cmap='viridis', cb=True, cminmax=(None, None)):


        # if log:
            # im = np.log10(np.abs(im)+1)

        # if fig is None:
            # fig = plt.figure()
            # axes = plt.gca()

        # axes.imshow(im, origin='lower', extent=self.get_extent(axis), aspect='auto', cmap=cmap)

        # vmin, vmax = vminmax
        # if vmin is None:
            # vmin = im.min()
        # if vmax is None:
            # vmax = im.max()

        # if cb:
            # norm = Normalize(vmin, vmax, clip=True)
            # fig.colorbar(ScalarMappable(norm), ax=axes)

        # for im in axes.get_images():
            # im.set_clim(vmin,vmax)








    def plot_xy(self, fig=None, axes=None, log=False, cmap='viridis', cb=True):
        '''scorpy.Vol.plot_xy()
        Plot the x=y plane of the volume.

        ...
        Arguments:
            fig : matplotlib.figure.Figure
                Figure to plot on. Default None will make a new figure.

            axes : matplotlib.axes._subplot.AxesSubplot
                Axes to plot on. Used for subplots.

            log : bool
                Flag for plotting log10(|x|+1) instead of x.

            cmap : str | matplotlib.colors.LinearSegmentedColormap
                Colourmap of the plot.

            cb : bool
                Flag for plott colourbar beside plot
        ...
        '''
        im = self.get_xy()
        if log:
            im = np.log10(np.abs(im)+1)

        if fig is None:
            fig = plt.figure()
            axes = plt.gca()

        axes.imshow(im, origin='lower', extent=self.get_extent(1), aspect='auto', cmap=cmap)
        if cb:

            norm = Normalize(im.min(), im.max())
            fig.colorbar(ScalarMappable(norm), ax=axes)


    def plot_sumax(self, axis=1, fig=None, axes=None, log=False, cmap='viridis', cb=True, vminmax=(None, None)):
        '''scorpy.Vol.plot_sumax()
        Plot the sum of values through an axis of the volume.

        ...
        Arguments:
            axis : int
                Axis through which to integrate through.

            fig : matplotlib.figure.Figure
                Figure to plot on. Default None will make a new figure.

            axes : matplotlib.axes._subplot.AxesSubplot
                Axes to plot on. Used for subplots.

            log : bool
                Flag for plotting log10(|x|+1) instead of x.

            cmap : str | matplotlib.colors.LinearSegmentedColormap
                Colourmap of the plot.

            cb : bool
                Flag for plott colourbar beside plot
        ...
        '''

        im = self.vol.sum(axis=axis)
        if log:
            im = np.log10(np.abs(im)+1)

        if fig is None:
            fig = plt.figure()
            axes = plt.gca()

        axes.imshow(im, origin='lower', extent=self.get_extent(axis), aspect='auto', cmap=cmap)

        vmin, vmax = vminmax
        if vmin is None:
            vmin = im.min()
        if vmax is None:
            vmax = im.max()

        if cb:
            norm = Normalize(vmin, vmax, clip=True)
            fig.colorbar(ScalarMappable(norm), ax=axes)

        for im in axes.get_images():
            im.set_clim(vmin,vmax)




    # def plot_slice(self, axis=0, index=0, new_fig=True, aspect='auto', extent=True, cmap='viridis', log=False):

        # im = np.rollaxis(self.vol, axis)[index, ...]

        # if log:
            # im = np.log(np.abs(im) + 1)
        # if new_fig:
            # plt.figure()

        # if extent:
            # plt.imshow(im, origin='lower',
                       # extent=self.get_extent(axis), aspect=aspect, cmap=cmap)
        # else:
            # plt.imshow(im, origin='lower', aspect=aspect)

        # if new_fig:
            # plt.colorbar()

    # def plot_line(self, axis=0, in1=0, in2=0, new_fig=True):

        # line = np.rollaxis(self.vol, axis)[in1, in2, ...]
        # if self.comp:
            # line = np.abs(line)
        # if new_fig:
            # plt.figure()
        # plt.plot(line)





