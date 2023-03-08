


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
import matplotlib.cm as cm
from matplotlib.colors import Normalize




from scipy.ndimage.filters import gaussian_filter

class BasePlot:

    def _plot_2D(self, im, **new_kwargs):
        '''Plot a 2D image.
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
        kwargs ={   'extent':None,
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
                    'ticks':True,
                    'norm':False,
                    'subtmean':False,
                    'blur':False,
                    'save':None,
                    'xticks': True,
                    'yticks': True,
                }

        kwargs.update(new_kwargs)


        # Make figure if none given
        if kwargs['fig'] is None:
            kwargs['fig'] = plt.figure()
            kwargs['axes'] = plt.gca()

        #Preprocessing: log intensity scale
        if kwargs['log']:
            im = np.log10(np.abs(im)+1)

        if kwargs['norm']:
            im -= im.min()
            im *= 1/im.max()

        if kwargs['subtmean']:
            means = im.mean(axis=1)
            xx, yy = np.meshgrid(np.ones(self.nz), means)
            im -= yy

        if kwargs['blur']:
            im = gaussian_filter(im,  sigma=kwargs['blur'])





        kwargs['axes'].imshow(im, origin=kwargs['origin'], extent=kwargs['extent'], aspect='auto', cmap=kwargs['cmap'])

        # Postprocessing: colorscale limits
        vmin, vmax = kwargs['vminmax']
        if vmin is None:
            vmin = im.min()
        if vmax is None:
            vmax = im.max()


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

        if type(kwargs['xticks']) is list:
            kwargs['axes'].set_xticks(kwargs['xticks'])

        if type(kwargs['yticks']) is list:
            kwargs['axes'].set_yticks(kwargs['yticks'])


        if kwargs['save'] is not None:
            print('saving image')
            plt.savefig(kwargs['save'])




    def _plot_errorbar(self, x,y, xerr=0,yerr=0, **new_kwargs):

        kwargs ={'fig':None,
                'axes':None,
                'cmap':'viridis',
                'cb':True,
                'xlabel':'',
                'ylabel':'',
                'title':'',
                'save':None,
                'label':'',
                'marker':'.',
                'markersize':5,
                'linestyle': '',
                'logy': False,
                'color':(0,0,0),
                'ecolor':(0,0,0),
                'dx':0,
                'dy':0,
                'elinewidth':None,
                'capsize':0,
                'errsf': 1,
                }

        kwargs.update(new_kwargs)

        # Make figure if none given
        if kwargs['fig'] is None:
            kwargs['fig'] = plt.figure()
            kwargs['axes'] = plt.gca()

        if kwargs['logy']:
            y = np.log10(np.abs(y)+1)
            yerr = None


        if yerr is None and xerr is None:

            kwargs['axes'].plot(x+kwargs['dx'],y+kwargs['dy'],
                                    marker=kwargs["marker"], linestyle=kwargs["linestyle"],
                                    label=kwargs['label'], color=kwargs['color'], markersize=kwargs['markersize'])

        else:


            kwargs['axes'].errorbar(x+kwargs['dx'],y+kwargs['dy'],
                                    xerr=kwargs['errsf']*xerr, yerr = kwargs['errsf']*yerr,
                                    marker=kwargs["marker"], linestyle=kwargs["linestyle"],
                                    label=kwargs['label'], color=kwargs['color'], ecolor=kwargs['ecolor'],
                                    elinewidth=kwargs['elinewidth'], capsize=kwargs['capsize'], markersize=kwargs['markersize'])


        kwargs['axes'].set_title(kwargs['title'])
        kwargs['axes'].set_xlabel(kwargs['xlabel'])
        kwargs['axes'].set_ylabel(kwargs['ylabel'])

        if kwargs['save'] is not None:
            plt.savefig(kwargs['save'])






