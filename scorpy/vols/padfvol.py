


from .vol import Vol
from .correlationvol import CorrelationVol
import os
import numpy as np

from .propertymixins import PadfVolProps


PADF_PADF = '/home/pat/Documents/cloudstor/phd/python_projects/padf/'


class PadfVol(Vol, PadfVolProps):

    def __init__(self, nr=100, ntheta=180, rmax=10,  path=None):
        Vol.__init__(self, nx=nr,ny=nr,nz=ntheta,
                     xmax=rmax, ymax=rmax, zmax=180, 
                     xmin=0, ymin=0, zmin=0,
                     path=path)

        self.plot_r1r2 = self.plot_xy
        # self.ymax = self.xmax
        self.rmax = self.xmax

        # self.ny = self.nx
        self.nr = self.nx

        self.npsi = self.nz


    def fill_from_corr(self, corr_path, nl=37, wavelength=1e-10):


        corr = CorrelationVol(path=corr_path)

        padf_config = open(f'{PADF_PADF}config.txt', 'w')
        padf_config.write(f'correlationfile = {corr_path}\n\n')

        os.system('mkdir /tmp/padf')
        padf_config.write(f'outpath = /tmp/padf\n\n')
        padf_config.write(f'wavelength = {wavelength}\n\n')
        padf_config.write(f'nl = {nl}\n\n')
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



