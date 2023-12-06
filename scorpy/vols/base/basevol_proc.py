


import numpy as np

import scipy.signal as signal









class BaseVolProc:


    def make_mask(self):
        loc = np.where(self.vol != 0)
        self.vol[loc] = 1

    def normalize_01(self):
        self.vol -=self.vol.min()
        self.vol *=1/self.vol.max()

    def normalize_sum(self):
        self.vol *=1/self.vol.sum()


    def zmean_subtraction(self):
        ## add option to excluce theta=0

        # print(self.vol.shape)
        vol_aligned = np.swapaxes(self.vol, 0,2)
        print(vol_aligned.shape)

        zmean = np.mean(vol_aligned, axis=0)

        vol_aligned -= zmean

        self.vol = np.swapaxes(vol_aligned, 0, 2)


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
        return kern


    def convolve_tophat(self, kern_L=2, kern_n=5, lim_x=1, lim_y=1, lim_z=1):
        '''
	scorpy.Vol.convolve_tophat():
            Convolve the current vol with a tophat kernel and replace it.
        Arguments:
            kern_L : int
                +/- upper and lower limit of the kernel.
            kern_n : int
                number of pixels in the kernel matrix.
            lim_x, lim_y, lim_z : float
                limits of the tophat in each x,y,z axis.
        '''
        # make linear spaces and meshes for each kernel direction
        x_space = np.linspace(-kern_L, kern_L, kern_n)
        y_space = np.linspace(-kern_L, kern_L, kern_n)
        z_space = np.linspace(-kern_L, kern_L, kern_n)


        x_mesh, y_mesh, z_mesh = np.meshgrid(x_space, y_space, z_space)

        x_cond =  np.abs(x_mesh) <= lim_x
        y_cond =  np.abs(y_mesh) <= lim_y
        z_cond =  np.abs(z_mesh) <= lim_z


        xy_cond = np.logical_and(x_cond, y_cond)
        xyz_cond = np.logical_and(xy_cond, z_cond)




        # calculates the  kernel and convolve
        kern = np.zeros( (kern_n, kern_n, kern_n) )
        kern[np.where(xyz_cond)] = 1
        # kern[x_loc, y_loc, z_loc] = 1


        blur = signal.fftconvolve(self.vol, kern)

        # bring the volume in by half the kernal window width (removes edge effects)
        kern_n_half = int((kern_n - 1) / 2)
        blur = blur[kern_n_half:-kern_n_half, kern_n_half:-kern_n_half, kern_n_half:-kern_n_half]
        self.vol = blur
        return kern


    def convolve2D(self,  kern_L=2, kern_n=5, std_y=1, std_z=1):

        y_space = np.linspace(-kern_L, kern_L, kern_n)
        z_space = np.linspace(-kern_L, kern_L, kern_n)

        y_mesh, z_mesh = np.meshgrid( y_space, z_space)

        kern = np.exp(- ( y_mesh ** 2 / (2 * std_y**2) + z_mesh**2 / (2 * std_z**2)))
        kern_n_half = int((kern_n - 1) / 2)
        blur = np.zeros(self.vol.shape)
        for i, yz in enumerate(self.vol):
            blur2D = signal.fftconvolve(yz, kern)
            blur[i] = blur2D[kern_n_half:-kern_n_half, kern_n_half:-kern_n_half]

        self.vol = blur



