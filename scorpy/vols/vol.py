import numpy as np
import copy
import scipy.signal as signal
import scipy
import configparser as cfp
from pathlib import Path
import matplotlib.pyplot as plt

from .propertymixins import VolProperties



class Vol(VolProperties):

    def __init__(self,  nx = None, ny = None, nz = None, \
                        xmax = None, ymax = None, zmax = None, \
                        xmin = None, ymin = None, zmin = None, \
                        comp = False, path = None):

        if not path is None:
            self.load_dbin(path)
        else:
            self._nx = nx
            self._ny = ny
            self._nz = nz
            self._xmax = xmax
            self._ymax = ymax
            self._zmax = zmax

            self._xmin = xmin
            self._ymin = ymin
            self._zmin = zmin

            self._comp = comp

            if self.comp:
                self._vol = np.zeros((nx,ny,nz)).astype(np.complex64)
            else:
                self._vol = np.zeros((nx,ny,nz))


    def load_dbin(self, path):

            if type(path) == str:
                path = Path(path)

            tag = path.stem
            config = cfp.ConfigParser()
            config.read(f'{path.parent}/{tag}_log.txt')

            self._nx = int(config['params']['nx'])
            self._ny = int(config['params']['ny'])
            self._nz = int(config['params']['nz'])

            self._xmin = float(config['params']['xmin'])
            self._ymin = float(config['params']['ymin'])
            self._zmin = float(config['params']['zmin'])

            self._xmax = float(config['params']['xmax'])
            self._ymax = float(config['params']['ymax'])
            self._zmax = float(config['params']['zmax'])

            self._comp = config.getboolean('params', 'comp')

            if self.comp:
                file_vol = np.fromfile(f'{path.parent}/{tag}.dbin', dtype=np.complex64)
            else:
                file_vol = np.fromfile(f'{path.parent}/{tag}.dbin')

            self._vol = file_vol.reshape((self.nx, self.ny, self.nz))





    def copy(self):
        return copy.deepcopy(self)



    def save_dbin(self, path):
        """
        Save the current Vol to a file.

        Args:
            path: path of the save location.

        """


        if type(path) == str:
            path = Path(path)

        tag = path.stem

        flat_vol= self.vol.flatten()
        flat_vol.tofile(f'{path.parent}/{tag}.dbin')

        f = open(f'{path.parent}/{tag}_log.txt', 'w')
        f.write('## Vol Log File\n\n')
        f.write('[params]\n')

        f.write(f'nx = {self.nx}\n')
        f.write(f'ny = {self.ny}\n')
        f.write(f'nz = {self.nz}\n')

        f.write(f'xmin = {self.xmin}\n')
        f.write(f'ymin = {self.ymin}\n')
        f.write(f'zmin = {self.zmin}\n')

        f.write(f'xmax = {self.xmax}\n')
        f.write(f'ymax = {self.ymax}\n')
        f.write(f'zmax = {self.zmax}\n')

        f.write(f'comp = {self.comp}\n')
        f.close()


    def get_eig(self, herm=True):

        if herm:
            lams = np.zeros( (self.nx, self.nz))
            us = np.zeros( (self.nx, self.ny, self.nz))
        else:
            lams = np.zeros( (self.nx, self.nz), dtype=np.complex64)
            us = np.zeros( (self.nx, self.ny, self.nz), dtype=np.complex64)

        for z in range(0, self.nz,2):
            if herm:
                lam, u = np.linalg.eigh(self.vol[...,z])
            else:
                lam, u = np.linalg.eig(self.vol[...,z])


            lams[:,z] = lam
            us[:,:,z] = u

        if not herm:
            if np.all(np.imag(lams)==0) and np.all(np.imag(us)==0):
                print('vol.get_eig(): lams and us are all real')
                lams = np.real(lams)
                us = np.real(us)
            else:
                print('vol.get_eig(): lams and us are NOT all real')
                print(f'max imag: lam: {np.max(np.imag(lams))}, us: {np.max(np.imag(us))}')
                lams = np.real(lams)
                us = np.real(us)


        return lams, us




    def convolve(self,  kern_L=2, kern_n =5, std_x = 1, std_y = 1,  std_z=1):
        """
        Convolve the current volume with a guassian kernel.


        Arguments:
            kern_L: +/- upper and lower limit of the kernel
            kern_n: number of pixels in the kernal matrix
            std_[x,y,z]: standard devieation of the guassian in each x,y,z direction

        """


        #make linear spaces and meshes for each kernel direction 
        x_space = np.linspace(-kern_L,kern_L, kern_n )
        y_space = np.linspace(-kern_L,kern_L, kern_n )
        z_space = np.linspace(-kern_L,kern_L, kern_n )
        x_mesh, y_mesh, z_mesh = np.meshgrid(x_space,y_space, z_space)

        #calculates the guassian kernel and convolve
        kern = np.exp(- ( x_mesh**2/(2*std_x**2) + y_mesh**2/(2*std_y**2) + z_mesh**2/(2*std_z**2)))
        blur = signal.fftconvolve(self.vol, kern)

        #bring the volume in by half the kernal window width (removes edge effects)
        kern_n_half = int((kern_n-1)/2)
        blur = blur[kern_n_half:-kern_n_half, kern_n_half:-kern_n_half, kern_n_half:-kern_n_half ]
        self.vol = blur




    def get_xy(self):
        assert self.nx==self.ny, 'vol.nx != vol.ny, cannot retrieve x=y plane of vol.'
        assert self.xmax==self.ymax, 'vol.xmax != vol.ymax, cannot retrieve x=y plane of vol.'

        im = np.zeros( (self.nx, self.nz))
        for xi in range(self.nx):
            im[xi,:] = self.vol[xi,xi,:]
        return im

    def plot_xy(self, new_fig=True, log=False, extent='default', aspect='auto'):
        '''
        Plot the x=y plane of the volume.

        Arguments:
            None

        Return:
            None
        '''
        if new_fig:
            plt.figure()
        im = self.get_xy()
        if log:
            im = np.log(np.abs(im)+1)
        plt.imshow(im, origin='lower', extent=[0, self.zmax, 0, self.xmax], aspect=aspect)
        if extent is None:
            plt.imshow(im, origin='lower',  aspect=aspect)

        if new_fig:
            plt.colorbar()


    def plot_sumax(self, axis=0, new_fig=True, extent='default', aspect='auto'):

        im = self.vol.sum(axis=axis)
        if new_fig:
            plt.figure()

        if extent is None:
            plt.imshow(im, origin='lower', aspect=aspect)
        else:
            plt.imshow(im, origin='lower', extent=self.get_extent(axis), aspect=aspect)

        if new_fig:
            plt.colorbar()


    def plot_slice(self,axis=0, index=0, new_fig=True, aspect='auto'):

        im = np.rollaxis(self.vol, axis)[index,...]
        if new_fig:
            plt.figure()

        if extent is None:
            plt.imshow(im, origin='lower', aspect=aspect)
        else:
            plt.imshow(im, origin='lower', extent=self.get_extent(axis), aspect=aspect)

        if new_fig:
            plt.colorbar()


    def plot_line(self,axis=0, in1=0, in2=0, new_fig=True):

        line = np.rollaxis(self.vol, axis)[in1,in2,...]
        if self.comp:
            line = np.abs(line)
        if new_fig:
            plt.figure()
        plt.plot(line)



    def get_extent(self,axis):
        if axis == 0:
            return [self.zmin, self.zmax, self.ymin, self.ymax]
        elif axis == 1:
            return [self.zmin, self.zmax, self.xmin, self.xmax]
        else:
            return [self.xmin, self.xmax, self.ymin, self.ymax]







    # def is_herm(self):

        # herm=True
        # for z in range(self.nz):
            # mat = np.matrix(self.vol[...,z])
            # if not np.allclose(mat, np.conj(mat.T)):
                # print('Vol not herm for z =',z)
                # herm = False
        # return herm

    # def is_sym(self):
        # sym=True
        # for z in range(self.nz):

            # mat1 = self.vol[...,z]
            # mat2 = self.vol[...,self.nz-z-1]

            # if not np.allclose(mat1,mat2):
                # print('Vol not sym for z =',z)
                # sym = False
                # # break
        # return sym




