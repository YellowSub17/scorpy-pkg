
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
                    'suptitle':'',
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
        kwargs['fig'].suptitle(kwargs['ylabel'])



    def plot_qharms(self, q_ind, axespos=None, axesneg=None, **new_kwargs):

        impos = self.vals[q_ind, 0, :, :]
        imneg = self.vals[q_ind, 1, :, :]

        if 'fig' not in new_kwargs.keys():
            if axespos is not None or axesneg is not None:
                print('Warning: axespos or axesneg is not None but fig not given, ignoring axes given')
            fig, axes = plt.subplots(2,1)
            axespos = axes[0]
            axesneg = axes[1]

            new_kwargs['fig'] = fig

        else:
            assert axespos is not None and axesneg is not None, 'If fig is given, axespos and axesneg are required'

        self._plot_2D(impos, axes=axespos,
                      extent=[0, self.nl,  0, self.nl], **new_kwargs)

        self._plot_2D(imneg, axes=axesneg,  origin='upper',
                      extent=[0, self.nl, self.nl, 0], **new_kwargs)




    def plot_lq(self, l, axespos=None, axesneg=None, **new_kwargs):

        impos = self.vals[:, 0, l, :]
        imneg = self.vals[:, 1, l, :]

        if 'fig' not in new_kwargs.keys():
            if axespos is not None or axesneg is not None:
                print('Warning: axespos or axesneg is not None but fig not given, ignoring axes given')
            fig, axes = plt.subplots(2,1)
            axespos = axes[0]
            axesneg = axes[1]

            new_kwargs['fig'] = fig

        else:
            assert axespos is not None and axesneg is not None, 'If fig is given, axespos and axesneg are required'

        self._plot_2D(impos.T, axes=axespos,
                      extent=[0, self.qmax,  0, self.nl], ylabel='M+',
                      xlabel='q [\u00c5]', **new_kwargs)



        self._plot_2D(imneg.T, axes=axesneg,  origin='upper', ylabel='M-', xlabel='q [\u00c5]',
                      extent=[0, self.qmax, self.nl, 0], **new_kwargs)









