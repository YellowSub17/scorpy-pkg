import numpy as np
import matplotlib.pyplot as plt
import h5py
from .expgeom import ExpGeom
from ..env import DATADIR
from ..utils import index_x

from .readersprops import PeakDataProperties

DEFAULT_GEO = ExpGeom(f'{DATADIR}/geoms/agipd_2304_vj_opt_v4.geom')
# DEFAULT_GEO = ExpGeom(f'{DATADIR}/geoms/xx.geom')

class PeakData(PeakDataProperties):

    def __init__(self, df, geo=DEFAULT_GEO, cxi_flag=True, qmax=None, qmin=0, mask_flag=False):
        '''
        handler for a peaks.txt file
        df: dataframe of the peak data, or str file path to txt
        geo: ExpGeom object associated to experiement geomtery
        '''

        self._geo = geo  # ExpGeom object
        # self._cxi_flag = cxi_flag
        self._mask_flag = mask_flag

        if type(df)==str:
            self._df = self.read_file(df, cxi_flag)
        else:
            self._df = df

        self._frame_numbers = np.unique(self.df[:, 0])


        self._scat_rect, self._scat_pol, self._scat_sph = self.get_scat(qmax=qmax, qmin=qmin)


        if qmax is not None:
            self._qmax = round(qmax, 14)
        else:
            self._qmax = round(self.scat_pol.max(axis=0)[0],14)

        if qmin is not None:
            self._qmin = round(qmin, 14)
        else:
            self._qmin = round(self.scat_pol.min(axis=0)[0],14)






    def read_file(self, fname, cxi_flag):
        if cxi_flag:
            # 0: frameNumber, 6: peak_x_raw, 7: peak_y_raw, 12: total intens
            delim, cols = ', ', (0,6,7,12)
        else:
            delim, cols = ' ', (0,2,1,3)

        if fname[-3:] == 'txt':
            df = np.genfromtxt(fname, delimiter=delim, skip_header=1, usecols=cols)

        elif fname[-2:] == 'h5':
            h5f = h5py.File(fname, 'r')
            if self.mask_flag:
                data = h5f['data/data'][:]
            else:
                data = h5f['entry_1/instrument_1/detector_1/data'][:]
                # self.datah5 = data
            h5f.close()

            loc = np.where(data > 0)
            df = np.zeros( (len(loc[0]), 4))
            df[:,1] = loc[1]
            df[:,2] = loc[0]
            df[:,3] = data[loc[0], loc[1]]
        return df



    def get_scat(self, qmax=None, qmin=None):
        '''
        generate a list of important values to calculate from
        it's easier to work with arrays the panda dataframes
        '''

        fss_df = self.df[:, 1]  # 0-127, fs direction
        sss_df = self.df[:, 2]  # ss direction
        inten_df = self.df[:, 3]  # intensity

        nscats = inten_df.size

        pix_pos = self.geo.translate_pixels(
            sss_df, fss_df)  # x,y,z position [m]





        scat_rect = np.zeros( (nscats, 4) )
        scat_rect[:,:3] = pix_pos
        scat_rect[:,-1] = inten_df


        pol_r_mag = np.hypot(pix_pos[:, 0], pix_pos[:, 1]) #distance in meters from detector center to pixel
        pol_phi = np.arctan2(pix_pos[:, 1], pix_pos[:, 0]) # angular polar coordinate of pixel
        pol_phi[np.where(pol_phi < 0)] = pol_phi[np.where(pol_phi < 0)] + 2*np.pi #angle measures from 0 to 360 degrees


        theta1 = np.arctan2(pol_r_mag, pix_pos[:, 2])

        # q_mag = (self.geo.k) * np.sin(theta1)  # 1/A
        q_mag = 2*self.geo.k*np.sin(0.5*theta1)

        #flat ewald sphere approx
        scat_pol = np.zeros( (nscats, 3) )
        scat_pol[:,0] = q_mag
        scat_pol[:,1] = pol_phi
        scat_pol[:,-1] = inten_df

        # scat_pol = np.array([q_mag, pol_phi, inten_df]).T


        saldin_sph_theta = np.pi/2 - np.arcsin((q_mag)/(2*self.geo.k))
        my_sph_theta = 0.5*(np.pi + theta1)

        scat_sph = np.zeros( ( nscats, 4))
        scat_sph[:,0] = q_mag
        scat_sph[:,1] = saldin_sph_theta
        scat_sph[:,2] = pol_phi
        scat_sph[:,-1] = inten_df

        if qmax is not None:
            loc = np.where(scat_pol[:, 0] <= qmax)
            scat_sph = scat_sph[loc]
            scat_rect = scat_rect[loc]
            scat_pol = scat_pol[loc]

        if qmin is not None:
            loc = np.where(scat_pol[:, 0] > qmin)
            scat_sph = scat_sph[loc]
            scat_rect = scat_rect[loc]
            scat_pol = scat_pol[loc]


        return scat_rect, scat_pol, scat_sph

    def split_frames(self, npeakmax=-1):
        '''
        return a list of PeakData objects, where each PeakData object on has a
        single frame of data
        '''

        frames = []  # init list of frames
        for fn in self.frame_numbers:  # for each frame number
            # get the peaks from this frame number
            frame_df = self.df[np.where(self.df[:, 0] == fn)]
            if npeakmax==-1 or frame_df.shape[0] <=npeakmax:
                # make the Peak data object and append
                frames.append(PeakData(frame_df, geo=self.geo, qmax=self.qmax, qmin=self.qmin))
        return frames  # return the list of appended peak datas



    def make_im(self, npix=500, r=0.055, bool_inten=False, fname=None):

        im = np.zeros( (npix,npix) )

        ite = np.ones( self.scat_rect.shape[0])

        xinds = map(index_x, self.scat_rect[:,0], -r*ite, r*ite, ite*npix)
        yinds = map(index_x, self.scat_rect[:,1], -r*ite, r*ite, ite*npix)

        for xind, yind, inten in zip(xinds, yinds, self.scat_rect[:,-1]):
            im[xind, yind] += inten

        if bool_inten:
            im[im>0] = 1
            im[im<0] = 0

        if fname is not None:
            flat_im = im.flatten()
            flat_im.tofile(fname)

        return im





    def integrate_peaks(self, r):

        # print(self.scat_rect[:25])
        # print()
        pixels = self.scat_rect[self.scat_rect[:, -1].argsort()]
        # print(pixels)
        # print()

        pixel_averaged_bool = np.zeros(pixels.shape[0])

        # peaks = peaks[::-1]

        integrated_peaks_list = []

        for i, pixel in enumerate(pixels):

            # print(pixel_averaged_bool)
            # print()
            if pixel_averaged_bool[i] ==1:
                print('skipping', i)
                continue

            dxypixels = pixels - pixel
            # print('dxy', dxypixels)

            dr = np.linalg.norm(dxypixels[:,:2], axis=1)
            # print('dr', dr)
            loc = np.where(dr<r)
            # print(loc)
            pixel_averaged_bool[loc] = 1

            if loc[0].shape[0] ==1:
                integrated_peaks_list.append(pixel)
                continue
            else:

         

                peak = np.average(pixels[loc], axis=0, weights=pixels[loc,-1].flatten())
                integrated_peaks_list.append(peak)







        self.scat_recti = np.array(integrated_peaks_list)

        # return dr, loc






    def plot_peaks(self, scatter=False, cmap=None, sizes=None, integrated=False,  newfig=True):

        if newfig:
            plt.figure()
        self.geo.plot_panels()



        if integrated:
            x = self.scat_recti[:,0]
            y = self.scat_recti[:,1]
            colors = self.scat_recti[:,-1]
            marker = 'x'
        else:
            x = self.scat_rect[:,0]
            y = self.scat_rect[:,1]
            colors = self.scat_rect[:,-1]
            marker = 'o'


        if sizes is not None:
            sizes = (np.max(sizes)-np.min(sizes))*(colors-colors.min())/(colors.max()-colors.min()) + np.min(sizes)
        else:
            sizes = 15

        plt.scatter(x, y, c=colors, s=sizes, cmap=cmap, marker=marker)
        plt.colorbar()










    def plot_inten_hist(self, bins=100, log=False):
        plt.figure()
        if log:
            plt.hist(np.log10(np.abs(self.scat_rect[:,-1])+1),bins=bins)
        else:
            plt.hist(self.scat_rect[:,-1],bins=bins)


