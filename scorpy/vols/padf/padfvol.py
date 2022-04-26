
import os
import numpy as np

from ..base.basevol import BaseVol
from ..corr.correlationvol import CorrelationVol
from .padfvol_props import PadfVolProps
from .padfvol_plot import PadfVolPlot
from .padfvol_saveload import PadfVolSaveLoad
from ...utils.env import PADFDIR






class PadfVol(BaseVol, PadfVolProps, PadfVolPlot, PadfVolSaveLoad):

    def __init__(self, nr=100, npsi=180, rmax=5, nl=10, wavelength=1.33, path=None):

        self._nl = nl
        self._wavelength = wavelength

        BaseVol.__init__(self, nr, nr, npsi,
                     0, 0, 0,
                     rmax, rmax, np.pi,
                     False, False, True,
                     comp=False, path=path)

        self.plot_r1r2 = self.plot_xy



    def fill_from_corr(self, corr, log='/tmp/padf.log', theta0=True):


        os.system('rm -rf /tmp/padf')
        os.system('mkdir /tmp/padf')

        if not theta0:
            corr.vol[:,:,0] = 0
        corr.save('/tmp/padf/corr.dbin')


        padf_config = open(f'{PADFDIR}config.txt', 'w')
        padf_config.write(f'correlationfile = /tmp/padf/corr.dbin\n\n')

        padf_config.write('outpath = /tmp/padf\n\n')
        padf_config.write(f'wavelength = {self.wavelength*1e-10}\n\n')
        padf_config.write(f'nl = {self.nl}\n\n')
        padf_config.write('tag = bingbong\n\n')

        padf_config.write(f'qmax = {float(corr.qmax)/1e-10}\n\n')
        padf_config.write(f'nq = {corr.nq}\n\n')
        padf_config.write(f'nthq = {corr.npsi}\n\n')

        padf_config.write(f'rmax = {self.rmax*1e-10}\n\n')
        padf_config.write(f'nr = {self.nr}\n\n')
        # padf_config.write(f'nthr = {2*self.npsi}\n\n')

        padf_config.close()

        cmd = f'{PADFDIR}padf {PADFDIR}config.txt'

        if log is None:
            os.system(cmd)
        else:
            print('Running padfcorr')
            os.system(f'{cmd} >{log} 2>&1')

        os.system('rm /tmp/padf/*r_vs_l*')
        os.system('rm /tmp/padf/*bl*')

        flatv = np.fromfile('/tmp/padf/bingbong_padf.dbin')

        v = flatv.reshape(self.nr, self.nr, corr.npsi)

        self.vol = v[..., :self.npsi]
