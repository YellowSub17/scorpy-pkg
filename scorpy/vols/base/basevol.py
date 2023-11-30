import numpy as np
import copy
import scipy.signal as signal
import scipy
import matplotlib.pyplot as plt

from .basevol_props import BaseVolProps
from .basevol_saveload import BaseVolSaveLoad
from .basevol_plot import BaseVolPlot

from ...utils.utils import index_x



class BaseVol(BaseVolProps, BaseVolPlot, BaseVolSaveLoad):
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

    def crop(self, xi, yi, zi, xf, yf, zf):

        cropped_arr = self.vol[xi:xf, yi:yf, zi:zf]

        new_xmin, new_xmax = self.xpts[xi], self.xpts[xf]
        new_ymin, new_ymax = self.ypts[yi], self.ypts[yf]
        new_zmin, new_zmax = self.zpts[zi], self.zpts[zf]

        new_nx = xf-xi
        new_ny = yf-yi
        new_nz = zf-zi
        print(f'{new_nx=} {new_ny=} {new_nz=}')

        new_vol = BaseVol(new_nx, new_ny, new_nz, 
                        new_xmin-self.dx/2, new_ymin-self.dx/2, new_zmin-self.dx/2,
                        new_xmax-self.dx/2, new_ymax-self.dx/2, new_zmax-self.dx/2,

                        False, False, False, self.comp)

        new_vol.vol = cropped_arr

        return new_vol





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
        return np.real(lams), np.real(us)

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





    def normalize(self):
        self.vol -=self.vol.min()
        self.vol *=1/self.vol.max()

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


    def evaluate(self, xval, yval, zval):
        '''
        give x,y,z coords between return the intensity value there
        '''

        xind = index_x(xval, self.xmin, self.xmax, self.nq, self.xwrap)
        yind = index_x(yval, self.ymin, self.ymax, self.nq, self.ywrap)
        zind = index_x(zval, self.zmin, self.zmax, self.nq, self.zwrap)

        return self.vol[xind, yind, zind]




    def get_index(self, x=None, y=None, z=None):
        '''

        give eitehr x, y or z, and get the index closest to that value

        '''
        xloc = None
        yloc = None
        yloc = None

        if x is not None:
            xloc = np.where(np.abs(self.xpts-x)==np.min(np.abs(self.xpts-x)))
            return xloc[0][0]
        if y is not None:
            yloc = np.where(np.abs(self.ypts-y)==np.min(np.abs(self.ypts-y)))
            return yloc[0][0]
        if z is not None:
            zloc = np.where(np.abs(self.zpts-z)==np.min(np.abs(self.zpts-z)))
            return zloc[0][0]

        print('No value given')
        return None





    def get_integrated_xy_line(self, xy_lower, xy_upper):
        xy = self.get_xy()

        xy_lower_ind = self.get_index(x=xy_lower)
        xy_upper_ind = self.get_index(x=xy_upper)


        inte = np.sum(xy[xy_lower_ind:xy_upper_ind, :], axis=0)

        return inte











    def ls_pts(self, thresh=0, inds=False):
        '''
	scorpy.Vol.ls_pts():
            List the points of intensity in the volume above a treshold.
        Arguments:
            thresh : float
                Threshold value
            inds : bool
                flag for providing array indices or point values

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

        if not inds:
            pts[:,0] = self.xpts[loc[0]]
            pts[:,1] = self.ypts[loc[1]]
            pts[:,2] = self.zpts[loc[2]]
        else:
            pts[:,0] = loc[0].astype(int)
            pts[:,1] = loc[1].astype(int)
            pts[:,2] = loc[2].astype(int)

        return pts



    def make_mask(self):

        loc = np.where(self.vol != 0)
        self.vol[loc] = 1




    def integrate_region(self, ptx, pty, ptz, dx, dy, dz, shape='disk'):




        if shape=='disk':
            xx, yy, zz = np.meshgrid(self.xpts, self.ypts, self.zpts)


            rxx, ryy, rzz = xx-ptx, yy-pty, np.abs(zz-ptz)

            rxy = np.sqrt(rxx**2 + ryy**2)

            loc = np.where( np.logical_and(rxy <= dx,rzz <=dz) )

        if shape=='rect':

            xx, yy, zz = np.meshgrid(self.xpts, self.ypts, self.zpts)
            rxx, ryy, rzz = np.abs(xx-ptx), np.abs(yy-pty), np.abs(zz-ptz)

            xandy = np.logical_and( rxx <= dx, ryy <=dy)

            loc = np.where(np.logical_and( xandy, rxx <= dz))




        return self.vol[loc].sum(), loc



    def integrate_peaks(self, mask_vol, dpix, sin_correction=True):

        new_vol = np.zeros(self.vol.shape)
        for xi, yi, zi, I in mask_vol.ls_pts(inds=True):
            xul = int(xi-dpix), int(xi+dpix+1)
            yul = int(yi-dpix), int(yi+dpix+1)
            zul = int(zi-dpix), int(zi+dpix+1)

            if sin_correction:
                sf = np.sin(self.zpts[int(yi)])
            else:
                sf = 1

            # intenI = self.vol[ xul[0]:xul[1], yul[0]:yul[1], zul[0]:zul[1] ].sum()*sf

            intenI = 0
            if zul[1]>self.nz:
                intenI +=self.vol[ xul[0]:xul[1], yul[0]:yul[1], zul[0]:zul[1] ].sum()*sf
                intenI +=self.vol[ xul[0]:xul[1], yul[0]:yul[1], 0:zul[1]-self.nz].sum()*sf

            elif zul[0] < 0:
                intenI +=self.vol[xul[0]:xul[1], yul[0]:yul[1], zul[0]].sum()*sf
                intenI +=self.vol[ xul[0]:xul[1], yul[0]:yul[1], 0:zul[1]].sum()*sf
            else:
                intenI = self.vol[ xul[0]:xul[1], yul[0]:yul[1], zul[0]:zul[1] ].sum()*sf


            new_vol[int(xi), int(yi), int(zi)] += intenI



        self.vol = new_vol



    def zmean_subtraction(self):
        ## add option to excluce theta=0

        print(self.vol.shape)
        vol_aligned = np.swapaxes(self.vol, 0,2)
        print(vol_aligned.shape)

        zmean = np.mean(vol_aligned, axis=0)
        
        vol_aligned -= zmean

        self.vol = np.swapaxes(vol_aligned, 0, 2)

        # return zmean








