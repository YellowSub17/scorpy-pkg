import numpy as np
import matplotlib.pyplot as plt

from .readerspropertymixins import PeakDataProperties


class PeakData(PeakDataProperties):

    def __init__(self, df, geo, cxi_flag=True):
        '''
        handler for a peaks.txt file
        df: dataframe of the peak data, or str file path to txt
        geo: ExpGeom object associated to experiement geomtery
        qlist_flag: flag to generate qvector correlation list
                    dont waste time generateing calculating a list if we need
                    to split the frames and calc again anyway
        '''

        self._geo = geo  # ExpGeom object
        self._cxi_flag = cxi_flag

        # if df is str, read dataframe from file, else, assume df is array
        if type(df) == str:
            if cxi_flag:
                # 0: frameNumber, 6: peak_x_raw, 7: peak_y_raw, 12: total intens
                self._df = np.genfromtxt(
                    df, delimiter=', ', skip_header=1, usecols=(0, 6, 7, 12))
            else:
                self._df = np.genfromtxt(
                    df, delimiter=' ', skip_header=1, usecols=(0, 2, 1, 3))
        else:
            self._df = df


        # multiple frames can be in a single peak file, so list the unique frames
        self._frame_numbers = np.unique(self.df[:, 0])

        self._scat_sqr, self._scat_pol = self.get_scat()

        self._qmax = self.scat_pol.max(axis=0)[0]

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

    def get_scat(self):
        '''
        generate a list of important values to calculate from
        it's easier to work with arrays the panda dataframes
        '''

        fss_df = self.df[:, 1]  # 0-127, fs direction
        sss_df = self.df[:, 2]  # ss direction
        inten_df = self.df[:, 3]  # intensity

        pix_pos = self.geo.translate_pixels(
            sss_df, fss_df)  # x,y,z position [m]

        r_mag = np.hypot(pix_pos[:, 0], pix_pos[:, 1])

        polar_t = np.degrees(np.arctan2(pix_pos[:, 1], pix_pos[:, 0]))
        polar_t[np.where(polar_t < 0)] = polar_t[np.where(polar_t < 0)] + 360

        diffrat_t = np.degrees(np.arctan2(r_mag, pix_pos[:, 2]))
        q_mag = (2 * np.pi / self.geo.wavelength) * \
            np.sin(np.radians(diffrat_t)) / 1e10  # 1/A

        scat_sqr = np.array([pix_pos[:, 0], pix_pos[:, 1], inten_df]).T
        scat_pol = np.array([q_mag, polar_t, inten_df]).T

        return scat_sqr, scat_pol

    def crop_scat(self, qmax=None, Imax=None):

        if qmax is not None:
            le_qmax = np.where(self.scat_pol[:, 0] <= qmax)[0]
            self.scat_pol = self.scat_pol[le_qmax]
            self.scat_sqr = self.scat_sqr[le_qmax]

        if Imax is not None:
            le_Imax = np.where(self.scat_pol[:, -1] <= Imax)[0]
            self.scat_pol = self.scat_pol[le_Imax]
            self.scat_sqr = self.scat_sqr[le_Imax]

    def plot_peaks(self, cmap=None, new_fig=False):
        if new_fig:
            plt.figure()
        if cmap is not None:
            plt.scatter(self.scat_sqr[:,0], self.scat_sqr[:,1], c=self.scat_sqr[:,-1], s=1, cmap=cmap)
        else:
            plt.plot(self.scat_sqr[:, 0], self.scat_sqr[:, 1], '.')

