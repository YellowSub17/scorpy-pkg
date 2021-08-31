import numpy as np


class VolPlot:

    def _setup_fig(self, new_fig, title, xlabel, ylabel):
        plt.figure()
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)


    def plot_xy(self, new_fig=True, log=False, extent='default', aspect='auto', title=''):
        '''scorpy.Vol.plot_xy()
        Plot the x=y plane of the volume.

        Arguments:
        '''
        if new_fig:
            plt.figure()
        im = self.get_xy()
        if log:
            im = np.log(np.abs(im) + 1)
        plt.imshow(im, origin='lower', extent=[
                   self.zmin, self.zmax, self.xmin, self.xmax], aspect=aspect)
        if extent is None:
            plt.imshow(im, origin='lower', aspect=aspect)

        if new_fig:
            plt.colorbar()
        plt.title(f'{title}')

    def plot_sumax(self, axis=0, new_fig=True, aspect='auto', extent=True, cmap='viridis', log=False, title=''):

        im = self.vol.sum(axis=axis)

        if log:
            im = np.log(np.abs(im) + 1)

        if new_fig:
            plt.figure()

        if extent:
            plt.imshow(im, origin='lower', extent=self.get_extent(
                axis), aspect=aspect, cmap=cmap)
        else:
            plt.imshow(im, origin='lower', aspect=aspect, cmap=cmap)

        if new_fig:
            plt.colorbar()
        plt.title(f'{title}')

    def plot_slice(self, axis=0, index=0, new_fig=True, aspect='auto', extent=True, cmap='viridis', log=False):

        im = np.rollaxis(self.vol, axis)[index, ...]

        if log:
            im = np.log(np.abs(im) + 1)
        if new_fig:
            plt.figure()

        if extent:
            plt.imshow(im, origin='lower',
                       extent=self.get_extent(axis), aspect=aspect, cmap=cmap)
        else:
            plt.imshow(im, origin='lower', aspect=aspect)

        if new_fig:
            plt.colorbar()

    def plot_line(self, axis=0, in1=0, in2=0, new_fig=True):

        line = np.rollaxis(self.vol, axis)[in1, in2, ...]
        if self.comp:
            line = np.abs(line)
        if new_fig:
            plt.figure()
        plt.plot(line)

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



