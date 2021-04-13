


from .vol import Vol
from .correlationvol import CorrelationVol
import os


PADF_PADF = '/home/pat/Documents/cloudstor/phd/python_projects/padf/'


class PadfVol(Vol):

    def __init__(self, nr=100, ntheta=180, rmax=10,  path=None):
        Vol.__init__(self, nr,nr,ntheta, rmax, rmax, 180, path=path)

        self.plot_r1r2 = self.plot_xy
        # self.ymax = self.xmax
        self.rmax = self.xmax

        # self.ny = self.nx
        self.nr = self.nx

        self.ntheta = self.nz


    def fill_from_corr(self, cor_path, nl=37, wavelength=1e-10):


        corr = CorrelationVol(path=cor_path)

        padf_config = open(f'{PADF_PADF}config.txt', 'w')
        padf_config.write(f'correlationfile = {os.getcwd()}/{cor_path}\n\n')
        padf_config.write(f'outpath = /tmp/padf\n\n')
        padf_config.write(f'wavelength = {wavelength}\n\n')
        padf_config.write(f'tag = bingbong\n\n')
        padf_config.write(f'nthq = {corr.ntheta}\n\n')
        padf_config.write(f'nq = {corr.nq}\n\n')
        padf_config.write(f'nthr = {self.ntheta}\n\n')
        padf_config.write(f'nr = {self.nr}\n\n')
        padf_config.write(f'nl = {nl}\n\n')
        padf_config.write(f'qmax = {float(corr.qmax)/1e-10}\n\n')
        padf_config.write(f'rmax = {self.rmax*1e-10}\n\n')


        padf_config.close()

        cmd = f'{PADF_PADF}padf {PADF_PADF}config.txt'

        os.system(f'{PADF_PADF}padf {PADF_PADF}config.txt')

        os.system(f'rm /tmp/padf/*r_vs_l*')
        os.system(f'rm /tmp/padf/*bl*')
        
