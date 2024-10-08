import numpy as np
import matplotlib.pyplot as plt
import h5py
import os
import scipy as sp

from ...utils.convert_funcs import index_x_nowrap, convert_rect2pol, convert_sph2rect


from .peakdata_props import PeakDataProperties
from .peakdata_plot import PeakDataPlot
from .expgeom import ExpGeom




class PeakData(PeakDataProperties, PeakDataPlot, ExpGeom):

    def __init__(self, datapath, geompath, data=None, clen_sf=1, pe_sf=1):
        '''
        handler for a peaks.txt file
        df: dataframe of the peak data, or str file path to txt
        geo: ExpGeom object associated to experiement geomtery
        '''

        self._geompath = geompath

        self.geom_params = self.parse_geom_file()
        self.clen_sf = clen_sf
        self.pe_sf = pe_sf


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



    # def wavelength(self):
        # return (4.135667e-15 * 2.99792e8 *1e10) / self.photon_energy  # A

    # def k(self):
        # return (2 * np.pi) / self.wavelength # 1/A





    def calc_scat(self, xyz_pixel, intens):



        # rphi = convert_rect2pol(xyz_pixel[:,0:2])
        # diff_cone_angle = np.arctan2(rphi[:,0], xyz_pixel[:, 2])
        # q_mag = 2*self.k*np.sin(0.5*diff_cone_angle)
        # saldin_sph_theta = np.pi/2 - np.arcsin((q_mag)/(2*self.k))



        xyz_pixel[:,2] *=self.clen_sf
        p_e =self.photon_energy*self.pe_sf
        rphi = convert_rect2pol(xyz_pixel[:,0:2])
        diff_cone_angle = np.arctan2(rphi[:,0], xyz_pixel[:, 2])

        lam = (4.135667e-15 * 2.99792e8 *1e10) / p_e # A
        k =  (2 * np.pi) / lam # 1/A

        print(f'{k=}')

        q_mag = 2*k*np.sin(0.5*diff_cone_angle)


        saldin_sph_theta = np.pi/2 - np.arcsin((q_mag)/(2*k))




        self._scat_rect = np.array([ xyz_pixel[:,0], xyz_pixel[:,1], xyz_pixel[:,2], intens]).T

        self._scat_rpol = np.array([ rphi[:,0], rphi[:,1], intens ]).T

        self._scat_tpol = np.array([diff_cone_angle, rphi[:,1], intens ]).T

        self._scat_qpol = np.array([q_mag , rphi[:,1], intens ]).T

        self._scat_sph = np.array([q_mag, saldin_sph_theta, rphi[:,1], intens ]).T

        qxyzi = np.zeros( (q_mag.shape[0], 4) )
        qxyzi[:,:-1] = convert_sph2rect(self.scat_sph[:,:-1])
        qxyzi[:,-1] = self.scat_sph[:,-1]
        
        self._scat_qxyz = qxyzi



    def convert_r2q(self, r):
        theta = np.arctan2(r, self.clen*self.clen_sf)
        return 2*self.k*np.sin(theta/2)

    def convert_q2r(self, q):

        p_e =self.pe_sf*self.photon_energy
        lam = (4.135667e-15 * 2.99792e8 *1e10) / p_e # A
        k =  (2 * np.pi) / lam # 1/A
        # print(q/(2*k))
        arcs = np.arcsin(q/(2*k))
        return np.tan(2*arcs)*( self.clen *self.clen_sf)

        # p_e =1.6*self.photon_energy
        # lam = (4.135667e-15 * 2.99792e8 *1e10) / p_e # A
        # k =  (2 * np.pi) / lam # 1/A
        # arcs = np.arcsin(q/(2*k))
        # return np.tan(2*arcs)*( self.clen -0.2)

        # p_e =0.3*self.photon_energy
        # lam = (4.135667e-15 * 2.99792e8 *1e10) / p_e # A
        # k =  (2 * np.pi) / lam # 1/A
        # arcs = np.arcsin(q/(2*k))
        # return np.tan(2*arcs)*( self.clen +2)

        # arcs = np.arcsin(q/(2*self.k))
        # return np.tan(2*arcs)*self.clen












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






