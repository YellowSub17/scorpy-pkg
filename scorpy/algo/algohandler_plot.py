


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



    def plot_vs_count(self, sub_tag, y, count_min=1, count_max=None,  **new_kwargs): 

        if y =='rfs':
            vals = np.load(self.rfs_shelx_path(sub_tag))
        elif y=='mean_dxyzs':
            vals = np.load(self.mean_dxyzs_path(sub_tag))
        elif y=='min_dxyzs':
            vals = np.load(self.min_dxyzs_path(sub_tag))
        elif y=='max_dxyzs':
            vals = np.load(self.max_dxyzs_path(sub_tag))
        elif y=='std_dxyzs':
            vals = np.load(self.std_dxyzs_path(sub_tag))

        elif y=='mean_dangles':
            vals = np.load(self.mean_bond_angles_path(sub_tag))
        elif y=='min_dangles':
            vals = np.load(self.min_bond_angles_path(sub_tag))
        elif y=='max_dangles':
            vals = np.load(self.max_bond_angles_path(sub_tag))
        elif y=='std_dangles':
            vals = np.load(self.std_bond_angles_path(sub_tag))

        elif y=='mean_ddistances':
            vals = np.load(self.mean_bond_distances_path(sub_tag))
        elif y=='min_ddistances':
            vals = np.load(self.min_bond_distances_path(sub_tag))
        elif y=='max_ddistances':
            vals = np.load(self.max_bond_distances_path(sub_tag))
        elif y=='std_ddistances':
            vals = np.load(self.std_bond_distances_path(sub_tag))



        if count_max is None:
            count_max= len(vals)
        counts = np.arange(count_min,count_max)


        self._plot_errorbar(counts, vals[count_min:count_max],  **new_kwargs)




 

    # def plot_rfs(self, sub_tag, count_min=1, count_max=None, calc='shelx', **new_kwargs):
        # assert calc=='shelx' or 'inten', 'calc method must be shelx or inten'

        # if calc=='shelx':
            # rfs = np.load(self.rfs_shelx_path(sub_tag))
        # else:
            # rfs = np.load(self.rfs_inten_path(sub_tag))

        # if count_max is None:
            # count_max= len(rfs)
        # counts = np.arange(count_min,count_max)

        # self._plot_errorbar(counts, rfs[count_min:count_max],  **new_kwargs)







    # def plot_mean_dxyzs(self, sub_tag, count_min=1, count_max=None, plot_err=False, **new_kwargs):

        # mean_dxyzs = np.load(self.mean_dxyzs_path(sub_tag))

        # min_dxyzs = np.load(self.min_dxyzs_path(sub_tag))
        # max_dxyzs = np.load(self.max_dxyzs_path(sub_tag))
        # std_dxyzs = np.load(self.std_dxyzs_path(sub_tag))

        # if plot_err:
            # yerr = std_dxyzs[count_min:count_max]
        # else:
            # yerr=0


        # if count_max is None:
            # count_max= len(mean_dxyzs)
        # counts = np.arange(count_min,count_max)



        # self._plot_errorbar(counts, mean_dxyzs[count_min:count_max] ,yerr=yerr,  **new_kwargs)







    # def plot_mean_dgeom(self, sub_tag, count_min=1, count_max=None, geometry='distances',plot_err=False, **new_kwargs):
        # if geometry=='distances':
            # dgeom = np.load(self.mean_bond_distances_path(sub_tag))
            # min_dgeom = np.load(self.min_bond_distances_path(sub_tag))
            # max_dgeom = np.load(self.max_bond_distances_path(sub_tag))
            # std_dgeom = np.load(self.std_bond_distances_path(sub_tag))
        # else:
            # dgeom = np.load(self.mean_bond_angles_path(sub_tag))
            # min_dgeom = np.load(self.min_bond_angles_path(sub_tag))
            # max_dgeom = np.load(self.max_bond_angles_path(sub_tag))
            # std_dgeom = np.load(self.std_bond_angles_path(sub_tag))


        # if count_max is None:
            # count_max= len(dgeom)
        # counts = np.arange(count_min,count_max)
        # dgeom = dgeom[count_min:count_max]
        # if plot_err:
            # yerr = std_dgeom[count_min:count_max]
        # else:
            # yerr=0


        # self._plot_errorbar(counts, dgeom, yerr=yerr, **new_kwargs)












    @verbose_dec
    def plot_intensity_xy(self, sub_tag, color_by=(None,None), count=None,n_scats=10000, verbose=0, **new_kwargs):

        It, If, z = self.get_intensity(sub_tag, z=color_by[0], n_scats=n_scats, verbose=verbose-1, count=count)

        It *= 1/np.sum(It)
        If *= 1/np.sum(If)


        # It *= 1/np.max(It)
        # If *= 1/np.max(If)

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
                # plt.plot([0, 1], [0, 1], c=f'k')
        else:
            self._plot_errorbar(It, If,  xlabel='Target Intensity (Norm.)',  ylabel='Algo Intensity (Norm.)', **new_kwargs)
            # plt.plot([0, 1], [0, 1], c=f'k')






    def plot_bond_geometry_xy(self,sub_tag, count=None, geometry='distances', **new_kwargs):


        targ_vals, targ_errs = self.get_geometry_vals(sub_tag, count='targ', geometry=geometry)
        algo_vals, algo_errs = self.get_geometry_vals(sub_tag, count=count, geometry=geometry)

        if geometry=='distances':
            label_ps = 'Bond Length [A]'
        else:
            label_ps = 'Bond Angle [deg]'


        self._plot_errorbar(targ_vals, algo_vals, targ_errs, algo_errs,
                            xlabel=f'Target {label_ps}',  ylabel=f'Algo {label_ps}', **new_kwargs)
        # plt.plot([np.min(targ_vals), np.max(targ_vals)], [np.min(targ_vals), np.max(targ_vals)], c=f'k')


