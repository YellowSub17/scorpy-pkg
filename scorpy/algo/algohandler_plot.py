


from ..utils.baseplot import BasePlot
from ..utils.utils import strerr2floaterrr

from ..vols.sphv.sphericalvol import SphericalVol
from ..read.cifs.cifdata import CifData
import CifFile as pycif
import matplotlib.pyplot as plt
import numpy as np



class AlgoHandlerPlot(BasePlot):




    def intensity_xy_plot(self, sub_tag, count=None, loc=None, **new_kwargs):



        It, If = self.get_intensity(sub_tag, count=count, loc=loc)

        self._plot_errorbar(It/np.sum(It), If/np.sum(If), xlabel='Target Intensity (Norm.)',  ylabel='Algo Intensity (Norm.)', **new_kwargs)






    def plot_rfs(self, sub_tag, calc='shelx', **new_kwargs):
        assert calc=='shelx' or 'inten', 'calc method must be shelx or inten'

        if calc=='shelx':
            rfs = np.load(self.rfs_shelx_path(sub_tag))
        else:
            rfs = np.load(self.rfs_inten_path(sub_tag))

        counts = np.arange(0, len(rfs))

        self._plot_errorbar(counts, rfs,  **new_kwargs)








    def bond_distances_xy_plot(self,sub_tag, count=None, **new_kwargs):


        targ_vals, targ_errs = self.get_geometry_vals(sub_tag, count='targ', geometry='distances')
        algo_vals, algo_errs = self.get_geometry_vals(sub_tag, count=count, geometry='distances')

        self._plot_errorbar(targ_vals, algo_vals, targ_errs, algo_errs, **new_kwargs)
        plt.plot([np.min(targ_vals), np.max(targ_vals)], [np.min(targ_vals), np.max(targ_vals)], c=f'k')


    def bond_angles_xy_plot(self,sub_tag, count=None, **new_kwargs):


        targ_vals, targ_errs = self.get_geometry_vals(sub_tag, count='targ', geometry='angles')
        algo_vals, algo_errs = self.get_geometry_vals(sub_tag, count=count, geometry='angles')

        self._plot_errorbar(targ_vals, algo_vals, targ_errs, algo_errs, **new_kwargs)
        plt.plot([np.min(targ_vals), np.max(targ_vals)], [np.min(targ_vals), np.max(targ_vals)], c=f'k')






