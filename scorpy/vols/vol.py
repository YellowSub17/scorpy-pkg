import numpy as np
import copy
import scipy.signal as signal
import scipy
import configparser as cfp
from pathlib import Path
import matplotlib.pyplot as plt

from .volspropertymixins import VolProps
from .volsplotmixins import VolPlot

from datetime import datetime


class Vol(VolProps, VolPlot):
    """
        scorpy.Vol:
            A class to describe an arbitrary volume or 3D function.
        Attributes:
            nx,ny,nz : int
            xmin,ymin,zmin : float
            xmax,ymax,zmax : float
            dx,dy,dz : float
            xpts,ypts,zpts : numpy.array
            xwrap, ywrap, zwrap : bool
            comp : bool
vol : numpy.ndarray
        Methods:
            Vol.save()
            Vol.copy()
            Vol.get_eig()
            Vol.convolve()
            Vol.get_xy()
            Vol.ls_pts()
            Vol.plot_xy()
            Vol.plot_slice()
            Vol.plot_sumax()
    """

    def __init__(self, nx=10, ny=10, nz=10,
                 xmin=0, ymin=0, zmin=0,
                 xmax=1, ymax=1, zmax=1,
                 xwrap=False, ywrap=False, zwrap=False,
                 comp=False, path=None):

        if path is not None:
            self._load(path)
        else:
            self._nx = nx
            self._ny = ny
            self._nz = nz

            self._xmin = xmin
            self._ymin = ymin
            self._zmin = zmin

            self._xmax = xmax
            self._ymax = ymax
            self._zmax = zmax

            self._xwrap = xwrap
            self._ywrap = ywrap
            self._zwrap = zwrap

            self._comp = comp

            if self.comp:
                self._vol = np.zeros((nx, ny, nz)).astype(np.complex64)
            else:
                self._vol = np.zeros((nx, ny, nz))

    def _load(self, path):
        '''
	scorpy.Vol._load(path):
            Loads a Vol object from dbin and log file.
        Arguments:
            path : str
                path to files to be loaded. The filename should exclude filetype.
        '''
        assert type(path) == str, 'Argument "path" must be string'
        path = Path(path)

        #check if path exists
        assert Path(f'{path}_log.txt').is_file(), f'ERROR: file {path} not found'


        tag = path.stem
        config = cfp.ConfigParser()
        config.read(f'{path.parent}/{tag}_log.txt')


        self._nx = int(config['vol']['nx'])
        self._ny = int(config['vol']['ny'])
        self._nz = int(config['vol']['nz'])

        self._xmin = float(config['vol']['xmin'])
        self._ymin = float(config['vol']['ymin'])
        self._zmin = float(config['vol']['zmin'])

        self._xmax = float(config['vol']['xmax'])
        self._ymax = float(config['vol']['ymax'])
        self._zmax = float(config['vol']['zmax'])

        self._xwrap = config.getboolean('vol', 'xwrap')
        self._ywrap = config.getboolean('vol', 'ywrap')
        self._zwrap = config.getboolean('vol', 'zwrap')

        self._comp = config.getboolean('vol', 'comp')
        if self.comp:
            file_vol = np.fromfile(f'{path.parent}/{tag}.dbin', dtype=np.complex64)
        else:
            file_vol = np.fromfile(f'{path.parent}/{tag}.dbin')

        self._vol = file_vol.reshape((self.nx, self.ny, self.nz))

        self._load_extra(config)

    def save(self, path):
        """
        scorpy.Vol.save(path):
            Save the current Vol to a dbin and log file.
        Arguments:
            path: path of the save location with file tag. The filename should exclude filetype.
        """

        assert type(path) == str,  'Argument "path" must be string'
        path = Path(path)
        tag = path.stem

        # write dbin
        flat_vol = self.vol.flatten()
        flat_vol.tofile(f'{path.parent}/{tag}.dbin')

        # write log
        f = open(f'{path.parent}/{tag}_log.txt', 'w')
        f.write('##Scorpy Config File\n')
        f.write(f'## Created: {datetime.now().strftime("%Y/%m/%d %H:%M")}\n\n')
        f.write('[vol]\n')
        f.write(f'nx = {self.nx}\n')
        f.write(f'ny = {self.ny}\n')
        f.write(f'nz = {self.nz}\n')
        f.write(f'xmin = {self.xmin}\n')
        f.write(f'ymin = {self.ymin}\n')
        f.write(f'zmin = {self.zmin}\n')
        f.write(f'xmax = {self.xmax}\n')
        f.write(f'ymax = {self.ymax}\n')
        f.write(f'zmax = {self.zmax}\n')
        f.write(f'xwrap = {self.xwrap}\n')
        f.write(f'ywrap = {self.ywrap}\n')
        f.write(f'zwrap = {self.zwrap}\n')
        f.write(f'dx = {self.dx}\n')
        f.write(f'dy = {self.dy}\n')
        f.write(f'dz = {self.dz}\n')
        f.write(f'comp = {self.comp}\n')
        f.write('\n')
        self._save_extra(f)
        f.close()

    def _save_extra(self, f):
        """
        scorpy.Vol._save_extra(f):
            Used by children classes to save extra information to log files.
        Arguments:
            f : _io.TestIOWrapper
                file object of log file, to write extra info.
        """
        pass

    def _load_extra(self, config):
        """
        scorpy.Vol._load_extra(f):
            Used by children classes to load extra information from log files.
        Arguments:
            config : configparser.Configparser
                configparser object to load extra information from.
        """
        pass

    def copy(self):
        '''
	scorpy.Vol.copy():
            Make a copy of the Vol, while keeping the original.
        Returns:
            v :  scorpy.Vol
                Copy of this volume object
        '''
        v = copy.deepcopy(self)
        return v

    def get_eig(self, herm=False, inc_odds=True):
        '''
	scorpy.Vol.get_eig():
            Calcualte the eigenvectors and eigenvalues of the x and y axes.
        Arguments:
            herm : bool
                Flag for calculating on hermitian matrices.
            inc_odds : bool
                Flag for including odd z slices
        Returns:
            lams : numpy.ndarray
                nx by nz array of eigenvalues. zth column of lams are the
                eigenvalues for the zth slice of the vol.
            us : numpy.ndarray
                nx by ny by nz array of eigenvectors. yth column of the zth slice
                of us is the eigen vector associated with the eigenvalue of the zth column in lams.
        '''
        if herm:
            dtype = np.float64
            eig_fn = np.linalg.eigh
        else:
            dtype = np.complex64
            eig_fn = np.linalg.eig

        if inc_odds:
            zskip=1
        else:
            zskip=2

        lams = np.zeros((self.nx, self.nz), dtype=dtype)
        us = np.zeros((self.nx, self.ny, self.nz), dtype=dtype)

        for z in range(0, self.nz, zskip):
            lam, u = eig_fn(self.vol[..., z])

            lams[:, z] = lam
            us[:, :, z] = u
        return lams, us

    def convolve(self, kern_L=2, kern_n=5, std_x=1, std_y=1, std_z=1):
        '''
	scorpy.Vol.convolve():
            Convolve the current vol with a guassian kernel and replace it.
        Arguments:
            kern_L : int
                +/- upper and lower limit of the kernel.
            kern_n : int
                number of pixels in the kernel matrix.
            std_x, std_y, std_z : float
                standard deviation of the guassian in each x,y,z axis.
        '''
        # make linear spaces and meshes for each kernel direction
        x_space = np.linspace(-kern_L, kern_L, kern_n)
        y_space = np.linspace(-kern_L, kern_L, kern_n)
        z_space = np.linspace(-kern_L, kern_L, kern_n)
        x_mesh, y_mesh, z_mesh = np.meshgrid(x_space, y_space, z_space)

        # calculates the guassian kernel and convolve
        kern = np.exp(- (x_mesh**2 / (2 * std_x**2) + y_mesh ** 2 / (2 * std_y**2) + z_mesh**2 / (2 * std_z**2)))
        blur = signal.fftconvolve(self.vol, kern)

        # bring the volume in by half the kernal window width (removes edge effects)
        kern_n_half = int((kern_n - 1) / 2)
        blur = blur[kern_n_half:-kern_n_half, kern_n_half:-kern_n_half, kern_n_half:-kern_n_half]
        self.vol = blur

    def get_xy(self):
        '''
	scorpy.Vol.get_xy():
            Extract diagonal x=y plane through vol. Only possible if x and y axes are identical.
        Returns:
            xy : numpy.ndarray
                nx by nz array of values in the x=y plane through the volume.
        '''
        assert self.nx == self.ny, 'vol.nx != vol.ny, cannot retrieve x=y plane of vol.'
        assert self.xmax == self.ymax, 'vol.xmax != vol.ymax, cannot retrieve x=y plane of vol.'
        assert self.xmin == self.ymin, 'vol.xmin != vol.ymin, cannot retrieve x=y plane of vol.'
        assert self.xwrap == self.ywrap, 'vol.xwrap != vol.ywrap, cannot retrieve x=y plane of vol.'

        xy = np.zeros((self.nx, self.nz))
        for xi in range(self.nx):
            xy[xi, :] = self.vol[xi, xi, :]
        return xy


    def ls_pts(self, thresh=0):
        '''
	scorpy.Vol.ls_pts():
            List the points of intensity in the volume above a treshold.
        Arguments:
            thresh : float
                Threshold value
        Returns:
            pts : numpy.ndarray
                n by 4 array of n points in the volume that are above the threshold.
                first three columns are the x,y, and z axis positions (according to
                xpts, ypts, zpts), last column is the intensity value at that position.
        '''
        loc = np.where(self.vol >thresh)
        npts = loc[0].size

        pts = np.zeros( ( npts, 4))
        pts[:,-1] = self.vol[loc]

        pts[:,0] = self.xpts[loc[0]]
        pts[:,1] = self.ypts[loc[1]]
        pts[:,2] = self.zpts[loc[2]]

        pts = pts[pts[:, 2].argsort()]
        pts = pts[pts[:, 1].argsort(kind='mergesort')]
        pts = pts[pts[:, 0].argsort(kind='mergesort')]
        return pts


    def make_mask(self):

        loc = np.where(self.vol != 0)
        self.vol[loc] *= 1/self.vol[loc]




