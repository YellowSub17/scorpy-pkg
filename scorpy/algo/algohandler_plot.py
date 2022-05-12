


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
    def plot_intensity_xy(self, sub_tag, color_by=(None,None), count=None, loc=None,n_intens=None, verbose=0, **new_kwargs):

        It, If, z = self.get_intensity(sub_tag, z=color_by[0], verbose=verbose-1, count=count, loc=loc)
        z *= 1/np.max(z)

        if n_intens is not None:

            temp = list(zip(It, If, z))
            np.random.shuffle(temp)
            It, If, z = temp[0, :n_intens], temp[1, :n_intens], temp[2, :n_intens]
            

        if color_by[0] is not None:
            col_map = cm.get_cmap(color_by[1])
            colors = col_map(z)[:,:-1]



            for i, (x,y, col) in enumerate(zip(It, If, colors)):
                print(i, end='\r')
                self._plot_errorbar(x/np.sum(It), y/np.sum(If), color=col, xlabel='Target Intensity (Norm.)',  ylabel='Algo Intensity (Norm.)', **new_kwargs)
        else:
            self._plot_errorbar(It/np.sum(It), If/np.sum(If),  xlabel='Target Intensity (Norm.)',  ylabel='Algo Intensity (Norm.)', **new_kwargs)





    def plot_bond_geometry_xy(self,sub_tag, count=None, geometry='distances', **new_kwargs):


        targ_vals, targ_errs = self.get_geometry_vals(sub_tag, count='targ', geometry=geometry)
        algo_vals, algo_errs = self.get_geometry_vals(sub_tag, count=count, geometry=geometry)

        self._plot_errorbar(targ_vals, algo_vals, targ_errs, algo_errs, **new_kwargs)
        plt.plot([np.min(targ_vals), np.max(targ_vals)], [np.min(targ_vals), np.max(targ_vals)], c=f'k')


