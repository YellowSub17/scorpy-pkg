import numpy as np
import scipy.signal as signal
import configparser as cfp
from pathlib import Path
import matplotlib.pyplot as plt




class Vol:

    def __init__(self,  nx=None, ny=None, nz=None, \
                        xmax=None, ymax=None, zmax=None, \
                        fromfile=False, path=None):

        if fromfile:
            assert type(path)==str, 'Please provide an fname to read from file'

            bigPATH = Path(path)

            self.fname = bigPATH.stem


            config = cfp.ConfigParser()
            config.read(f'{bigPATH.parent}/{self.fname}_log.txt')

            self.nx = int(config['params']['nx'])
            self.ny = int(config['params']['ny'])
            self.nz = int(config['params']['nz'])

            self.xmax = float(config['params']['xmax'])
            self.ymax = float(config['params']['ymax'])
            self.zmax = float(config['params']['zmax'])
            file_vol = np.fromfile(f'{bigPATH.parent}/{self.fname}.dbin')
            self.vol = file_vol.reshape((self.nx, self.ny, self.nz))


        else:
            self.nx = nx
            self.ny = ny
            self.nz = nz
            self.xmax = xmax
            self.ymax = ymax
            self.zmax = zmax
            self.vol = np.zeros((nx,ny,nz))




    def save_dbin(self, path):
        """
        Save the current Vol to a file.

        Args:
            path: path of the save location.

        """

        assert type(path)==str, 'Please provide a string path to save dbin'

        bigPATH = Path(path)

        self.fname = bigPATH.stem


        flat_vol= self.vol.flatten()
        flat_vol.tofile(f'{bigPATH.parent}/{self.fname}.dbin')

        f = open(f'{bigPATH.parent}/{self.fname}_log.txt', 'w')
        f.write('## Vol Log File\n\n')
        f.write('[params]\n')
        f.write(f'fname = {self.fname}\n')

        f.write(f'nx = {self.nx}\n')
        f.write(f'ny = {self.ny}\n')
        f.write(f'nz = {self.nz}\n')

        f.write(f'xmax = {self.xmax}\n')
        f.write(f'ymax = {self.ymax}\n')
        f.write(f'zmax = {self.zmax}\n')
        f.close()



    def convolve(self,  kern_L=2, kern_n =5, std_x = 1, std_y = 1,  std_z=1):
        """
        Convolve the current volume with a guassian kernel.

        Args:
            kern_L: +/- upper and lower limit of the kernel
            kern_n: number of pixels in the kernal matrix
            std_[x,y,z]: standard devieation of the guassian in each x,y,z direction


        Returns:
            blur: numpy array of the self.vol convolved with a gaussian kernal. 
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
        return blur


    def get_xy(self):
        assert self.nx==self.ny, 'vol.nx !=vol.ny, cannot retreive x=y plane of vol'

        im = np.zeros( (self.nx, self.nz))
        for xi in range(self.nx):
            im[xi,:] = self.vol[xi,xi,:]
        return im

    def plot_xy(self):
        plt.figure()
        im = self.get_xy()
        plt.imshow(im)



