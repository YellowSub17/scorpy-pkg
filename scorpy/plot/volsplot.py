

from .baseplot import BasePlot


class VolPlot(BasePlot):

    def plot_xy(self, **new_kwargs):
        '''Plot the x=y plane of the volume.
        '''
        im = self.get_xy()
        self._plot_2D(im, **new_kwargs)



    def plot_sumax(self, axis, **new_kwargs):
        '''Sum the values through an axis and plot the image.
        Arguments:
            axis : int
                Axis through which to integrate through.
        '''
        im = self.vol.sum(axis=axis)
        self._plot_2D(im, extent_axis=axis,**new_kwargs)


    def plot_slice(self, axis, index, **new_kwargs):
        '''Extract a slice of the volume (plane perpendicular to an axis) and plot the image.
        Arguments:
            axis : int
                Axis perpendicular to slice.
            index : int
                Index of the slice to extract.
        '''
        if axis%3==0:
            im = self.vol[index,:,:]
        if axis%3==1:
            im = self.vol[:,index,:]
        if axis%3==2:
            im = self.vol[:,:,index]

        self._plot_2D(im, extent_axis=axis, **new_kwargs)



