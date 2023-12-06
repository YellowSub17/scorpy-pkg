from scipy import special
import numpy as np
import time

from ...utils.utils import angle_between_pol, angle_between_sph, angle_between_rect, index_x, verbose_dec

from ..base.basevol import BaseVol
from .correlationvol_props import CorrelationVolProps
from .correlationvol_plot import CorrelationVolPlot
from .correlationvol_saveload import CorrelationVolSaveLoad
from .correlationvol_fill import CorrelationVolFill
from .correlationvol_corr import CorrelationVolCorr


class CorrelationVol(BaseVol,               #Parent Vol Class
                     CorrelationVolProps,   #Protected Properties
                     CorrelationVolSaveLoad,#Save and Load functionality
                     CorrelationVolPlot,    #Plotting
                     CorrelationVolFill,    #Fill from other objects
                     CorrelationVolCorr     #Correlation scattering vectors
                    ):


    """scorpy.CorrelationVol:
    A representaion of the scattering correlation function.
    Attributes:
        nq, npsi : int
        qmax : float
        dq,dpsi : float
        qpts,psipts : numpy.array
    Methods:
        CorrelationVol.fill_from_cif()
        CorrelationVol.fill_from_blqq()
        CorrelationVol.fill_from_peakdata()
        CorrelationVol.correlate_scat_rect()
        CorrelationVol.correlate_scat_pol()
        CorrelationVol.correlate_scat_sph()
        CorrelationVol.plot_q1q2()
    """

    def __init__(self, nq=100, npsi=180, qmax=1, qmin=0, cos_sample=True,  path=None):

        if path is not None:
            BaseVol.__init__(self, path=path)
        else:

            if cos_sample:
                BaseVol.__init__(self, nq, nq, npsi, qmin, qmin, -1, qmax, qmax, 1, False, False, False, comp=False, path=path)
            else:
                BaseVol.__init__(self, nq, nq, npsi, qmin, qmin, 0, qmax, qmax, np.pi, False, False, False, comp=False, path=path)

            self._cos_sample = cos_sample

        self.plot_q1q2 = self.plot_xy



    def qpsi_correction(self):

        q1q1, q2q2, psipsi = np.meshgrid(self.qpts, self.qpts, self.psipts)

        self.vol *= np.sin(psipsi)
        self.vol *= (q1q1*q2q2)

















