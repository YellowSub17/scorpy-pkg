import numpy as np
import copy
import scipy
import matplotlib.pyplot as plt

from .basevol_props import BaseVolProps
from .basevol_saveload import BaseVolSaveLoad
from .basevol_plot import BaseVolPlot
from .basevol_proc import BaseVolProc

from ...utils.convert_funcs import index_xs



class BaseVol(BaseVolProps, BaseVolPlot, BaseVolSaveLoad, BaseVolProc):
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

    def get_indices(self, pts, axis=0):

        inds = index_xs(pts, self.mins[axis], self.maxs[axis], self.npts[axis], self.wraps[axis])

        return inds



    def sum_into_vol(self, x_inds, y_inds, z_inds, vals, sym=False, verbose=0):

        # print(f'Summing {len(x_inds)} points.')
        for i, (x_ind, y_ind, z_ind, val) in enumerate(zip(x_inds, y_inds, z_inds, vals)):
            print(f'{i}', end='\r')
            self.vol[x_ind, y_ind, z_ind] += val
            if sym:
                self.vol[x_ind, y_ind, z_ind] += val





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


    def cosinesim(self, v):

        assert (self.nx, self.ny, self.nz)==(v.nx, v.ny, v.nz), 'Vols not the same shape.'
        v1f, v2f = self.vol.flatten(), v.vol.flatten()
        sim = np.dot(v1f, v2f)/ (np.linalg.norm(v1f) * np.linalg.norm(v2f))
        return sim



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
        dtype, eig_fn = (  (np.float64, np.linalg.eigh) if herm else (np.complex64, np.linalg.eig) )

        zskip = 1 if inc_odds else 2


        lams = np.zeros((self.nx, self.nz), dtype=dtype)
        us = np.zeros((self.nx, self.ny, self.nz), dtype=dtype)

        for z in range(0, self.nz, zskip):
            lam, u = eig_fn(self.vol[..., z])
            lams[:, z] = lam
            us[:, :, z] = u
        return np.real(lams), np.real(us)




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









