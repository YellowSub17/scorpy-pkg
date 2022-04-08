


from ..utils.baseplot import BasePlot

from ..vols.sphv.sphericalvol import SphericalVol
import matplotlib.pyplot as plt



class AlgoHandlerPlot(BasePlot):


    def inspect_support(self,qq):


        sphv_supp = SphericalVol(path=f'{self.path}/sphv_{self.tag}_supp.dbin')


        plt.figure()
        plt.plot(sphv_supp.vol.sum(axis=-1).sum(axis=-1))




