


from ..utils.baseplot import BasePlot
from ..utils.utils import strerr2floaterrr

from ..vols.sphv.sphericalvol import SphericalVol
from ..read.cifs.cifdata import CifData
import CifFile as pycif
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from ..utils.utils import verbose_dec



class AlgoHandlerPlot(BasePlot):




 

    def plot_rfs(self, sub_tag, count_min=1, count_max=None, calc='shelx', **new_kwargs):
        assert calc=='shelx' or 'inten', 'calc method must be shelx or inten'

        if calc=='shelx':
            rfs = np.load(self.rfs_shelx_path(sub_tag))
        else:
            rfs = np.load(self.rfs_inten_path(sub_tag))

        if count_max is None:
            count_max= len(rfs)
        counts = np.arange(count_min,count_max)

        self._plot_errorbar(counts, rfs[count_min:count_max],  **new_kwargs)





    def plot_mean_dxyzs(self, sub_tag, count_min=1, count_max=None, **new_kwargs):

        mean_dxyzs = np.load(self.mean_dxyzs_path(sub_tag))


        if count_max is None:
            count_max= len(mean_dxyzs)
        counts = np.arange(count_min,count_max)



        self._plot_errorbar(counts, mean_dxyzs[count_min:count_max] ,  **new_kwargs)







    def plot_mean_dgeom(self, sub_tag, count_min=1, count_max=None, geometry='distances', **new_kwargs):
        if geometry=='distances':
            dgeom = np.load(self.mean_bond_distances_path(sub_tag))
            min_dgeom = np.load(self.min_bond_distances_path(sub_tag))
            max_dgeom = np.load(self.max_bond_distances_path(sub_tag))
            std_dgeom = np.load(self.std_bond_distances_path(sub_tag))
        else:
            dgeom = np.load(self.mean_bond_angles_path(sub_tag))
            min_dgeom = np.load(self.min_bond_angles_path(sub_tag))
            max_dgeom = np.load(self.max_bond_angles_path(sub_tag))
            std_dgeom = np.load(self.std_bond_angles_path(sub_tag))


        if count_max is None:
            count_max= len(dgeom)
        counts = np.arange(count_min,count_max)
        dgeom = dgeom[count_min:count_max]
        yerr = std_dgeom[count_min:count_max]


        self._plot_errorbar(counts, dgeom, yerr=yerr, **new_kwargs)












    @verbose_dec
    def plot_intensity_xy(self, sub_tag, color_by=(None,None), count=None,n_scats=10000, verbose=0, **new_kwargs):

        It, If, z = self.get_intensity(sub_tag, z=color_by[0], n_scats=n_scats, verbose=verbose-1, count=count)

        It *= 1/np.sum(It)
        If *= 1/np.sum(If)


        It *= 1/np.max(It)
        If *= 1/np.max(If)

        if z is not None:
            z -=np.min(z)
            z *= 1/np.max(z)



        if color_by[0] is not None:
            col_map = cm.get_cmap(color_by[1])
            colors = col_map(z)[:,:-1]


            print('## algo.plot_intensity_xy: Plotting Point')
            for i, (x,y, col) in enumerate(zip(It, If, colors)):
                print(f'{i}/{n_scats}', end='\r')
                self._plot_errorbar(x, y, color=col, xlabel='Target Intensity (Norm.)',  ylabel='Algo Intensity (Norm.)', **new_kwargs)
        else:
            self._plot_errorbar(It, If,  xlabel='Target Intensity (Norm.)',  ylabel='Algo Intensity (Norm.)', **new_kwargs)






    def plot_bond_geometry_xy(self,sub_tag, count=None, geometry='distances', **new_kwargs):


        targ_vals, targ_errs = self.get_geometry_vals(sub_tag, count='targ', geometry=geometry)
        algo_vals, algo_errs = self.get_geometry_vals(sub_tag, count=count, geometry=geometry)

        self._plot_errorbar(targ_vals, algo_vals, targ_errs, algo_errs, **new_kwargs)
        plt.plot([np.min(targ_vals), np.max(targ_vals)], [np.min(targ_vals), np.max(targ_vals)], c=f'k')


