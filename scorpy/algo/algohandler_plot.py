


from ..utils.baseplot import BasePlot
from ..utils.utils import strerr2floaterrr

from ..vols.sphv.sphericalvol import SphericalVol
from ..read.cifs.cifdata import CifData
import CifFile as pycif
import matplotlib.pyplot as plt
import numpy as np



class AlgoHandlerPlot(BasePlot):




    def intensity_xy_plot(self, sub_tag, count=None, **new_kwargs):



        It, If = self.get_intensity(sub_tag, count=count)

        self._plot_2D_scatter(It/np.sum(It), If/np.sum(If),xlabel='Target Intensity (Norm.)',  ylabel='Algo Intensity (Norm.)', **new_kwargs)










    def bond_distance_xy_plot(self,sub_tag, count=None, **new_kwargs):


        targ_vals, targ_errs = self.get_bond_distances(sub_tag, count='targ')
        algo_vals, algo_errs = self.get_bond_distances(sub_tag, count=count)

        self._plot_errorbar(targ_vals, algo_vals, targ_errs, algo_errs, **new_kwargs)
        plt.plot([np.min(targ_vals), np.max(targ_vals)], [np.min(targ_vals), np.max(targ_vals)], c=f'k')


    def bond_angle_xy_plot(self,sub_tag, count=None, **new_kwargs):


        targ_vals, targ_errs = self.get_bond_angles(sub_tag, count='targ')
        algo_vals, algo_errs = self.get_bond_angles(sub_tag, count=count)

        self._plot_errorbar(targ_vals, algo_vals, targ_errs, algo_errs, **new_kwargs)
        plt.plot([np.min(targ_vals), np.max(targ_vals)], [np.min(targ_vals), np.max(targ_vals)], c=f'k')






