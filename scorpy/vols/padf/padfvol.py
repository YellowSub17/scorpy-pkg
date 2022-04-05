
import os
import numpy as np

from ..base.basevol import BaseVol
from ..corr.correlationvol import CorrelationVol
from .padfvol_props import PadfVolProps
from ...utils.env import PADF_PADF






class PadfVol(BaseVol, PadfVolProps):

    def __init__(self, nr=100, npsi=180, rmax=5, nl=10, wavelength=1.33, path=None):

        self._nl = nl
        self._wavelength = wavelength

        BaseVol.__init__(self, nr, nr, npsi,
                     0, 0, 0,
                     rmax, rmax, np.pi,
                     False, False, True,
                     comp=False, path=path)

        self.plot_r1r2 = self.plot_xy

    def _save_extra(self, f):
        f.write('[padf]\n')
        f.write(f'rmax = {self.rmax}\n')
        f.write(f'psimax = {np.pi}\n')
        f.write(f'nr = {self.nr}\n')
        f.write(f'npsi = {self.npsi}\n')
        f.write(f'dr = {self.dr}\n')
        f.write(f'dpsi = {self.dpsi}\n')
        f.write(f'nl = {self.nl}\n')
        f.write(f'wavelength = {self.wavelength}\n')

    def _load_extra(self, config):

        self._nl = float(config['padf']['nl'])
        self._wavelength = float(config['padf']['wavelength'])

    def fill_from_corr(self, corr, log='/tmp/padf.log', theta0=True):


        os.system('rm -rf /tmp/padf')
        os.system('mkdir /tmp/padf')

        if not theta0:
            corr.vol[:,:,0] = 0
        corr.save('/tmp/padf/corr.dbin')


        padf_config = open(f'{scorpy.PADFDIR}config.txt', 'w')
        
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

        cmd = f'{scorpy.PADFDIR}padf {scorpy.PADFDIR}config.txt'

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