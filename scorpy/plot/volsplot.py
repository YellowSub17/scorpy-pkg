

from .baseplot import BasePlot


class VolPlot(BasePlot):

    def plot_xy(self, **new_kwargs):
        '''Plot the x=y plane of the volume.
        '''
        im = self.get_xy()

        if 'extent' not in new_kwargs.keys():
            extent=[self.zmin,self.zmax,self.xmin,self.xmax]
            new_kwargs.update({'extent':extent})

        self._plot_2D(im, **new_kwargs)



    def plot_sumax(self, axis, **new_kwargs):
        '''Sum the values through an axis and plot the image.
        Arguments:
            axis : int
                Axis through which to integrate through.
        '''
        im = self.vol.sum(axis=axis)


        if 'extent' not in new_kwargs.keys():
            if axis%3==0:
                extent=[self.zmin,self.zmax,self.xmin,self.xmax]
            if axis%3==1:
                extent=[self.zmin,self.zmax,self.xmin,self.xmax]
            if axis%3==2:
                extent=[self.zmin,self.zmax,self.xmin,self.xmax]
            new_kwargs.update({'extent':extent})


        self._plot_2D(im, **new_kwargs)


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
            extent=[self.zmin,self.zmax,self.ymin,self.ymax]
        if axis%3==1:
            im = self.vol[:,index,:]
            extent=[self.xmin,self.xmax,self.zmin,self.zmax]
        if axis%3==2:
            im = self.vol[:,:,index]
            extent=[self.xmin,self.xmax,self.ymin,self.ymax]

        if 'extent' not in new_kwargs.keys():
            new_kwargs.update({'extent':extent})

        self._plot_2D(im, extent_axis=axis, **new_kwargs)



