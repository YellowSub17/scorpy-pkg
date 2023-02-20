import numpy as np
import matplotlib.pyplot as plt
import h5py
from ..geom.expgeom import ExpGeom
from ...utils.env import DATADIR
from ...utils.utils import index_x

from .peakdata_props import PeakDataProperties
from .peakdata_plot import PeakDataPlot




class PSPeakData(PeakDataProperties, PeakDataPlot):

    def __init__(self, path, geom=None):
        '''
        handler for a peaks.txt file
        df: dataframe of the peak data, or str file path to txt
        geo: ExpGeom object associated to experiement geomtery
        '''

        self._path=path
        self._geom=geom

        with h5py.File(self.path) as h5file:
            data = h5file['/entry_1/instrument_1/detector_1/data'][:]

        data_loc =  np.where(data>0) # fs is the cols

        self._df = np.zeros( (len(data_loc[0]), 3) )


        self._df[:, 0] = data_loc[1] #fs
        self._df[:, 1] = data_loc[0] #ss
        self._df[:,2] = data[data_loc[0], data_loc[1]]

        if self.geom is not None:
            pix_pos = self.geom.translate_pixels(self._df)


        nscats = self._df.shape[0]
        scat_rect = np.zeros( (nscats, 4) )
        scat_rect[:,0:3] = pix_pos
        scat_rect[:,3] = self._df[:,-1]




        pol_r_mag = np.hypot(pix_pos[:, 0], pix_pos[:, 1]) #distance in meters from detector center to pixel
        pol_phi = np.arctan2(pix_pos[:, 1], pix_pos[:, 0]) # angular polar coordinate of pixel
        pol_phi[np.where(pol_phi < 0)] = pol_phi[np.where(pol_phi < 0)] + 2*np.pi #angle measures from 0 to 2pi radians


        theta_scatter_angle = np.arctan2(pol_r_mag, pix_pos[:, 2])

        q_mag = 2*self.geom.k*np.sin(0.5*theta_scatter_angle)

        saldin_sph_theta = np.pi/2 - np.arcsin((q_mag)/(2*self.geom.k))
        # my_sph_theta = 0.5*(np.pi + theta1)


        #flat ewald sphere approx
        scat_pol = np.zeros( (nscats, 3) )
        scat_pol[:,0] = q_mag
        scat_pol[:,1] = pol_phi
        scat_pol[:,2] = self._df[:,-1]



        #curved ewald sphere
        scat_sph = np.zeros( ( nscats, 4))
        scat_sph[:,0] = q_mag
        scat_sph[:,1] = saldin_sph_theta
        scat_sph[:,2] = pol_phi
        scat_sph[:,3] = self._df[:,-1]




        self._scat_rect = scat_rect
        self._scat_pol = scat_pol
        self._scat_sph = scat_sph




    def make_im(self, npix, r, bool_inten=False, fname=None):

        im = np.zeros( (npix,npix) )

        loc = np.where(np.linalg.norm(self.scat_rect[:,0:2], axis=1)<r)[0]

        ite = np.ones( len(loc))

        xinds = map(index_x, self.scat_rect[loc,0], -r*ite, r*ite, ite*npix)
        yinds = map(index_x, self.scat_rect[loc,1], -r*ite, r*ite, ite*npix)

     

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











