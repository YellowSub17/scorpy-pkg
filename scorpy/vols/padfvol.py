


from .vol import Vol
from .correlationvol import CorrelationVol
import os
import numpy as np

from .propertymixins import PadfVolProps


PADF_PADF = '/home/pat/Documents/cloudstor/phd/python_projects/padf/'


class PadfVol(Vol, PadfVolProps):

    def __init__(self,  nr = 100, npsi = 180, rmax = 5, \
                        nl = 10, wavelength = 1.33,
                        path = None):


        self._nl = nl
        self._wavelength = wavelength

        Vol.__init__(self,  nr, nr, npsi, \
                            rmax, rmax, 180, \
                            0, 0, 0, \
                            comp = False, path = path)


        self.plot_r1r2 = self.plot_xy

    def _save_extra(self, f):
        f.write('[padf]\n')
        f.write(f'rmax = {self.rmax}\n')
        f.write(f'psimax = {180}\n')
        f.write(f'nr = {self.nr}\n')
        f.write(f'npsi = {self.npsi}\n')
        f.write(f'dr = {self.dr}\n')
        f.write(f'dpsi = {self.dpsi}\n')
        f.write(f'nl = {self.nl}\n')
        f.write(f'wavelength = {self.wavelength}\n')

    def _load_extra(self, config):

        self._nl = float(config['padf']['nl'])
        self._wavelength = float(config['padf']['wavelength'])





    def fill_from_corr(self, corr_path):


        corr = CorrelationVol(path=corr_path)

        padf_config = open(f'{PADF_PADF}config.txt', 'w')
        padf_config.write(f'correlationfile = {corr_path}\n\n')

        os.system('mkdir /tmp/padf')
        padf_config.write(f'outpath = /tmp/padf\n\n')
        padf_config.write(f'wavelength = {self.wavelength*1e-10}\n\n')
        padf_config.write(f'nl = {self.nl}\n\n')
        padf_config.write(f'tag = bingbong\n\n')

        padf_config.write(f'qmax = {float(corr.qmax)/1e-10}\n\n')
        padf_config.write(f'nq = {corr.nq}\n\n')
        padf_config.write(f'nthq = {corr.npsi}\n\n')

        padf_config.write(f'rmax = {self.rmax*1e-10}\n\n')
        padf_config.write(f'nr = {self.nr}\n\n')
        # padf_config.write(f'nthr = {2*self.ntheta}\n\n')



        padf_config.close()

        cmd = f'{PADF_PADF}padf {PADF_PADF}config.txt'

        os.system(cmd)

        os.system(f'rm /tmp/padf/*r_vs_l*')
        os.system(f'rm /tmp/padf/*bl*')


        flatv = np.fromfile(f'/tmp/padf/bingbong_padf.dbin')

        v =  flatv.reshape(self.nr, self.nr, corr.npsi)

        self.vol = v[...,:self.npsi]



