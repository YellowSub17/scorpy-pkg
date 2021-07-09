import numpy as np
import matplotlib.pyplot as plt

from .readerspropertymixins import PeakDataProperties


class PeakData(PeakDataProperties):

    def __init__(self, df, geo, cxi_flag=True, qmax=None):
        '''
        handler for a peaks.txt file
        df: dataframe of the peak data, or str file path to txt
        geo: ExpGeom object associated to experiement geomtery
        '''

        self._geo = geo  # ExpGeom object
        # self._cxi_flag = cxi_flag

        self.read_df(df, cxi_flag)

        # multiple frames can be in a single peak file, so list the unique frames
        self._frame_numbers = np.unique(self.df[:, 0])

        self._scat_rect, self._scat_pol, self._scat_sph = self.get_scat(qmax=qmax)


        if qmax is not None:
            self._qmax = qmax
        else:
            self._qmax = self.scat_pol.max(axis=0)[0]

    def read_df(self, df, cxi_flag):
        # if df is str, read dataframe from file, else, assume df is array
        if type(df) == str:
            if df[-3:] =='txt':
                if cxi_flag:
                    # 0: frameNumber, 6: peak_x_raw, 7: peak_y_raw, 12: total intens
                    self._df = np.genfromtxt(
                        df, delimiter=', ', skip_header=1, usecols=(0, 6, 7, 12))
                else:
                    self._df = np.genfromtxt(
                        df, delimiter=' ', skip_header=1, usecols=(0, 2, 1, 3))
            elif df[-2:] == 'h5':
                self._df = 0
                assert False, 'ERROR: h5 to pk not implemented'
        else:
            self._df = df


    def split_frames(self):
        '''
        return a list of PeakData objects, where each PeakData object on has a
        single frame of data
        '''

        frames = []  # init list of frames
        for fn in self.frame_numbers:  # for each frame number
            # get the peaks from this frame number
            frame_df = self.df[np.where(self.df[:, 0] == fn)]
            # make the Peak data object and append
            frames.append(PeakData(frame_df, self.geo))
        return frames  # return the list of appended peak datas

    def get_scat(self, qmax=None):
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

        scat_pol = np.zeros( (nscats, 3) )
        scat_pol[:,0] = q_mag
        scat_pol[:,1] = pol_phi
        scat_pol[:,-1] = inten_df

        # scat_pol = np.array([q_mag, pol_phi, inten_df]).T


        # saldin_sph_theta = np.pi/2 - np.arcsin((q_mag)/(2*self.geo.k))


        sph_theta = 0.5*(np.pi + theta1)
        scat_sph = np.zeros( ( nscats, 4))
        scat_sph[:,0] = q_mag
        scat_sph[:,1] = sph_theta
        scat_sph[:,2] = pol_phi
        scat_sph[:,-1] = inten_df

        if qmax is not None:
            loc = np.where(q_mag <= qmax)
            scat_sph = scat_sph[loc]
            scat_rect = scat_rect[loc]
            scat_pol = scat_pol[loc]


        return scat_rect, scat_pol, scat_sph


    def plot_peaks(self, cmap=None, new_fig=False, s=100):
        if new_fig:
            plt.figure()
        if cmap is not None:
            plt.scatter(self.scat_rect[:, 0], self.scat_rect[:, 1], \
                        c=self.scat_rect[:, -1], s=s*self.scat_rect[:,-1,]/self.scat_rect[:,-1].max(), cmap=cmap)
        else:
            plt.plot(self.scat_rect[:, 0], self.scat_rect[:, 1], '.', ms=s*self.scat_rect[:,-1,]/self.scat_rect[:,-1].max(),)
