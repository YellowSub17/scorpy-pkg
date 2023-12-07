import numpy as np
import matplotlib.pyplot as plt
import h5py
import os
import scipy as sp

from ...utils.convert_funcs import index_x_nowrap, convert_rect2pol


from .peakdata_props import PeakDataProperties
from .peakdata_plot import PeakDataPlot
from .expgeom import ExpGeom




class PeakData(PeakDataProperties, PeakDataPlot, ExpGeom):

    def __init__(self, datapath, geompath, data=None):
        '''
        handler for a peaks.txt file
        df: dataframe of the peak data, or str file path to txt
        geo: ExpGeom object associated to experiement geomtery
        '''

        self._geompath = geompath

        self.geom_params = self.parse_geom_file()


        self._datapath = datapath

        if type(datapath) is list:

            print('Loading list of npz.')

            data_coo = sp.sparse.load_npz(datapath[0])
            data_shape = data_coo.toarray().shape
            data = np.zeros(data_shape)


            for i,datapathf in enumerate(self.datapath):
                print(f'{i}/{len(self.datapath)}', end='\r')
                data_coo = sp.sparse.load_npz(datapathf)
                data += data_coo.toarray()
                # print( i, len(datapathf), end='\r' )


            ss_pixels, fs_pixels =  np.where(data>0) # fs is the cols
            intens = data[ss_pixels, fs_pixels]
            scat_fs_ss = np.array([ fs_pixels, ss_pixels, intens]).T
            xyz_pixel = self.fsss2xyz(scat_fs_ss)
            self.calc_scat(xyz_pixel, intens)



            


        elif type(datapath) is str:

            if self.datapath[-3:]=='.h5':
                with h5py.File(self.datapath) as h5file:
                    data = h5file[self.geom_params['data']][:]
                ss_pixels, fs_pixels =  np.where(data>0) # fs is the cols
                intens = data[ss_pixels, fs_pixels]
                scat_fs_ss = np.array([ fs_pixels, ss_pixels, intens]).T
                xyz_pixel = self.fsss2xyz(scat_fs_ss)
                self.calc_scat(xyz_pixel, intens)


            elif self.datapath[-4:]=='.npz':
                data_coo = sp.sparse.load_npz(self.datapath)
                data = data_coo.toarray()
                ss_pixels, fs_pixels =  np.where(data>0) # fs is the cols
                intens = data[ss_pixels, fs_pixels]
                scat_fs_ss = np.array([ fs_pixels, ss_pixels, intens]).T
                xyz_pixel = self.fsss2xyz(scat_fs_ss)
                self.calc_scat(xyz_pixel, intens)



            elif self.datapath[-4:]=='.npy':
                scat_fs_ss = np.load(self.datapath)
                xyz_pixel = self.fsss2xyz(scat_fs_ss)
                self.calc_scat(xyz_pixel, scat_fs_ss[:,-1])




        else:
            return None






    def calc_scat(self, xyz_pixel, intens):


        rphi = convert_rect2pol(xyz_pixel[:,0:2])

        diff_cone_angle = np.arctan2(rphi[:,0], xyz_pixel[:, 2])
        q_mag = 2*self.k*np.sin(0.5*diff_cone_angle)

        saldin_sph_theta = np.pi/2 - np.arcsin((q_mag)/(2*self.k))





        self._scat_rect = np.array([ xyz_pixel[:,0], xyz_pixel[:,1], xyz_pixel[:,2], intens]).T

        self._scat_rpol = np.array([ rphi[:,0], rphi[:,1], intens ]).T

        self._scat_tpol = np.array([diff_cone_angle, rphi[:,1], intens ]).T

        self._scat_qpol = np.array([q_mag , rphi[:,1], intens ]).T

        self._scat_sph = np.array([q_mag, saldin_sph_theta, rphi[:,1], intens ]).T



    def convert_r2q(self, r):
        theta = np.arctan2(r, self.clen)
        return 2*self.k*np.sin(theta/2)

    def convert_q2r(self, q):
        arcs = np.arcsin(q/(2*self.k))
        return np.tan(2*arcs)*self.clen












    def make_im(self, npix, r, bool_inten=False, fname=None):

        im = np.zeros( (npix,npix) )

        loc = np.where(np.linalg.norm(self.scat_rect[:,0:2], axis=1)<r)[0]

        ite = np.ones( len(loc))

        xinds = map(index_x_nowrap, self.scat_rect[loc,0], -r*ite, r*ite, ite*npix)
        yinds = map(index_x_nowrap, self.scat_rect[loc,1], -r*ite, r*ite, ite*npix)

     

        for xind, yind, inten in zip(xinds, yinds, self.scat_rect[loc,-1]):
            im[xind, yind] += inten

        if bool_inten:
            im[im>0] = 1
            im[im<0] = 0

        if fname is not None:
            flat_im = im.flatten()
            flat_im.tofile(fname)

        return im.T





    def integrate_peaks(self, r):

        pixels = self.scat_rect[self.scat_rect[:, -1].argsort()]

        pixel_averaged_bool = np.zeros(pixels.shape[0])

        pixels = pixels[::-1]

        integrated_peaks_list = []

        for i, pixel in enumerate(pixels):

            if pixel_averaged_bool[i] ==1:
                continue

            dxypixels = pixels - pixel

            dr = np.linalg.norm(dxypixels[:,0:2], axis=1)
            loc = np.where(dr<r)
            pixel_averaged_bool[loc] = 1

            if loc[0].shape[0] ==1:
                integrated_peaks_list.append(pixel)
                continue
            else:
                peak = np.average(pixels[loc], axis=0, weights=pixels[loc,-1].flatten())
                peak[-1] = np.sum(pixels[loc], axis=0)[-1]
                integrated_peaks_list.append(peak)



        return np.array(integrated_peaks_list)






