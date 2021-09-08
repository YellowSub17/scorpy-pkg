
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
import matplotlib.cm as cm
from matplotlib.colors import Normalize


class IqlmHandlerPlot:


    def _plot_2D(self, im, **new_kwargs):
        '''scorpy.IqlmHandlerPlot._plot_2D()
        Plot the 2D get_image.
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
        '''
        kwargs = {  'extent':None,
                    'fig':None,
                    'axes':None,
                    'log':False,
                    'cmap':'viridis',
                    'cb':True,
                    'vminmax':(None, None),
                    'xlabel':'',
                    'ylabel':'',
                    'title':'',
                    'origin':'lower',
                 }

        kwargs.update(new_kwargs)


        # Make figure if none given
        if kwargs['fig'] is None:
            kwargs['fig'] = plt.figure()
            kwargs['axes'] = plt.gca()

        #Preprocessing: log intensity scale
        if kwargs['log']:
            im = np.log10(np.abs(im)+1)


        kwargs['axes'].imshow(im, origin=kwargs['origin'], extent=kwargs['extent'], aspect='auto', cmap=kwargs['cmap'])

        # Postprocessing: colorscale limits
        vmin, vmax = kwargs['vminmax']
        if vmin is None:
            vmin = im.min()
        if vmax is None:
            vmax = im.max()


        # why is colorbar incorrect when min=max?
        if vmax==vmin:
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



    def plot_q(self, q_ind, cs=None, **new_kwargs):

        if cs is not None:
            im = self.vals[q_ind, cs, :, :]
            self._plot_2D(im, **new_kwargs)

        else:
            impos = self.vals[q_ind, 0, :, :]
            imneg = self.vals[q_ind, 1, :, :0:-1]
            im = np.concatenate([imneg, impos], 1)
            self._plot_2D(im, **new_kwargs)





    def plot_l(self, l, cs=None, **new_kwargs):

        if cs is not None:
            im = self.vals[:, cs, l,  :]
            self._plot_2D(im.T, **new_kwargs)

        else:
            impos = self.vals[:, 0, l, :]
            imneg = self.vals[:, 1, l, :0:-1]
            im = np.concatenate([imneg.T, impos.T], 0)
            self._plot_2D(im.T, **new_kwargs)





