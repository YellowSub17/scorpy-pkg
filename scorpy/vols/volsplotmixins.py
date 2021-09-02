import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
import matplotlib.cm as cm
from matplotlib.colors import Normalize


class VolPlot:



    def _plot_2D(self, im, **new_kwargs):
        '''scorpy.Vol._plot_2D()
        Plot the 2D get_image.

        ...
        Arguments:
            im : numpy.ndarray
                2D array to be plotted

        Keyword Arguments:
            extent_axis : int
                axis perpendicular to the image plane.

            fig : matplotlib.figure.Figure
                Figure to plot on. Default None will make a new figure.

            axes : matplotlib.axes._subplot.AxesSubplot
                Axes to plot on. Used for subplots.

            log : bool
                Flag for plotting log10(|x|+1) instead of x.

            cmap : str | matplotlib.colors.LinearSegmentedColormap
                Colourmap of the plot.

            cb : bool
                Flag for plotting colourbar beside plot

            vminmax : tuple
                Upper and lower bounds of colour limits. Use None on either
                bound to specify min or max value of image.
        ...
        '''
        kwargs = {  'extent_axis':1,
                    'fig':None,
                    'axes':None,
                    'log':False,
                    'cmap':'viridis',
                    'cb':True,
                    'vminmax':(None, None), 
                    'title':'',
                    'xlabel':'',
                    'ylabel':'',}

        kwargs.update(new_kwargs)


        # Make figure if none given
        if kwargs['fig'] is None:
            kwargs['fig'] = plt.figure()
            kwargs['axes'] = plt.gca()

        #Preprocessing: log intensity scale
        if kwargs['log']:
            im = np.log10(np.abs(im)+1)

        if kwargs['extent_axis']== 0:
            extent = [self.zmin, self.zmax, self.ymin, self.ymax]
        elif kwargs['extent_axis']== 1:
            extent = [self.zmin, self.zmax, self.xmin, self.xmax]
        else:
            extent = [self.xmin, self.xmax, self.ymin, self.ymax]

        kwargs['axes'].imshow(im, origin='lower', extent=extent, aspect='auto', cmap=kwargs['cmap'])

        # Postprocessing: colorscale limits
        vmin, vmax = kwargs['vminmax']
        if vmin is None:
            vmin = im.min()
        if vmax is None:
            vmax = im.max()


        #TODO: why is colorbar incorrect when min=max?
        if vmax==vmin:
            print('Warning: Image has uniform intensity, so colorbar will be incorrect. Turning off colourbar.')
            kwargs['cb']=False

        # Add colorbar
        if kwargs['cb']:
            norm = Normalize(vmin, vmax, clip=False)
            kwargs['fig'].colorbar(ScalarMappable(norm, cmap=kwargs['cmap']), ax=kwargs['axes'])

        # Set colorlimits
        for axes_im in kwargs['axes'].get_images():
            axes_im.set_clim(vmin,vmax)

        kwargs['axes'].set_title(kwargs['title'])
        kwargs['axes'].set_xlabel(kwargs['xlabel'])
        kwargs['axes'].set_ylabel(kwargs['ylabel'])




    def plot_xy(self, **new_kwargs):
        '''scorpy.Vol.plot_xy()
        Plot the x=y plane of the volume.

        ...
        Extra Keyword Arguments:
            See scorpy.Vol._plot_2D.__doc__
        '''
        im = self.get_xy()
        self._plot_2D(im, **new_kwargs)




    def plot_sumax(self, axis, **new_kwargs):
        '''scorpy.Vol.plot_sumax()
        Sum the values through an axis and plot the image.

        ...
        Arguments:
            axis : int
                Axis through which to integrate through.

        Extra Keyword Arguments:
            See scorpy.Vol._plot_2D.__doc__
        ...
        '''
        im = self.vol.sum(axis=axis)
        self._plot_2D(im, extent_axis=axis,**new_kwargs)


    def plot_slice(self, axis, index, **new_kwargs):
        '''scorpy.Vol.plot_slice()
        Extract a slice of the volume (plane perpendicular to an axis) and plot the image.

        ...
        Arguments:
            axis : int
                Axis perpendicular to slice.

            index : int
                Index of the slice to extract.

        Extra Keyword Arguments:
            See scorpy.Vol._plot_2D.__doc__
        ...
        '''

        if axis%3==0:
            im = self.vol[index,:,:]
        if axis%3==1:
            im = self.vol[:,index,:]
        if axis%3==2:
            im = self.vol[:,:,index]

        self._plot_2D(im, extent_axis=axis, **new_kwargs)




