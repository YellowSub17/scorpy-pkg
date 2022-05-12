
import os
import shutil
import numpy as np

from ..base.basevol import BaseVol
from ..corr.correlationvol import CorrelationVol
from .padfvol_props import PadfVolProps
from .padfvol_plot import PadfVolPlot
from .padfvol_saveload import PadfVolSaveLoad
from ...utils.env import PADFDIR
from ...utils.utils import verbose_dec

import time






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



    @verbose_dec
    def fill_from_corr(self, corr, theta0=True, sf=1, tag='bingbong', verbose=0):



        print('Filling PadfVol from CorrelationVol')
        print(f'Started: {time.asctime()}')

        if os.path.exists(f'/tmp/padf/{tag}'):
            shutil.rmtree(f'/tmp/padf/{tag}')

        if not os.path.exists('/tmp/padf/'):
            os.mkdir(f'/tmp/padf/')

        os.mkdir(f'/tmp/padf/{tag}')

        if not theta0:
            corr.vol[:,:,0] = 0
        corr.save(f'/tmp/padf/{tag}/{tag}_corr.dbin')


        padf_config = open(f'{PADFDIR}/config.txt', 'w')
        padf_config.write(f'correlationfile = /tmp/padf/{tag}/{tag}_corr.dbin\n\n')

        padf_config.write(f'outpath = /tmp/padf/{tag}/\n\n')
        # padf_config.write(f'wavelength = {self.wavelength*1e-10}\n\n')
        padf_config.write('wavelength = %8.2g\n\n' % (self.wavelength*1e-10))
        padf_config.write(f'nl = {self.nl}\n\n')
        padf_config.write(f'tag = {tag}\n\n')

        # padf_config.write(f'qmax = {sf*float(corr.qmax)/1e-10}\n\n')
        padf_config.write('qmax = %8.2g\n\n' % (sf*float(corr.qmax)/1e-10))

        padf_config.write(f'nq = {corr.nq}\n\n')
        padf_config.write(f'nthq = {corr.npsi}\n\n')

        padf_config.write('rmax = %8.2g\n\n' % (self.rmax*1e-10))
        # padf_config.write(f'rmax = {self.rmax*1e-10}\n\n')
        padf_config.write(f'nr = {self.nr}\n\n')

        padf_config.close()

        cmd = f'{PADFDIR}/padf {PADFDIR}/config.txt'

    # line = '%4d%4d%4d%8.2f%8.2f\n' % (round(bragg_pt[0]), round(bragg_pt[1]), round(bragg_pt[2]), bragg_pt[3], 0)


        # os.system(f'{cmd} >/tmp/padf/{tag}/padf_{tag}_output.log 2>&1')
        print('')
        print('##################')
        os.system(f'{cmd}')
        print('##################')
        print('')


        flatv = np.fromfile(f'/tmp/padf/{tag}/{tag}_padf.dbin')

        v = flatv.reshape(self.nr, self.nr, corr.npsi)

        self.vol = v[..., :self.npsi]

        print(f'Finished: {time.asctime()}')




