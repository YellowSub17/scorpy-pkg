import numpy as np
import matplotlib.pyplot as plt


class PeakData:

    def __init__(self, df, geo, qlist_flag=True, rpf_flag=False):
        '''
        handler for a peaks.txt file
        df: dataframe of the peak data, or str file path to txt
        geo: ExpGeom object associated to experiement geomtery
        qlist_flag: flag to generate qvector correlation list
                    dont waste time generateing calculating a list if we need
                    to split the frames and calc again anyway
        '''

        self.geo = geo  #ExpGeom object
        self.rpf_flag = rpf_flag

        #if df is str, read dataframe from file, else, assume df is dataframe
        if type(df)==str:

            #use cols: frameNUmebr, photon energy (ev), wavelngth, GMD,
            #peak index, peak_x_raw, peak_y_raw, peak_r_assembled,_peak_q,
            #peak_resA, npix, total intens, max intens, sigmaBG, SNR

            # self.df = np.genfromtxt(df, delimiter=', ', skip_header=1, usecols=(0,2,3,4,5,6,7,8,9,10,11,12,13,14,15))

            if self.rpf_flag:
                self.df = np.genfromtxt(df, delimiter=' ')
            else:
                self.df = np.genfromtxt(df, delimiter=', ', skip_header=1, usecols=(0,6,7,12))
        else:
            self.df = df

        #multiple frames can be in a single peak file, so list the unique frames
        self.frameNumbers = np.unique(self.df[:,0])
        self.qlist_flag=qlist_flag
        if self.qlist_flag:
            self.qlist = self.gen_qlist()
            self.qmax = np.max(self.qlist[:,5])

    def split_frames(self):
        '''
        return a list of PeakData objects, where each PeakData object on has a
        single frame of data
        '''
        if len(self.frameNumbers)<=1:       #check if we can actually split this data frame
            print('This PeakData object contains one frame, cannot split frames')
            return None                 #should this just return itself?
        else:
            frames = []                                 #init list of frames
            for fn in self.frameNumbers:                    #for each frame number
                frame_df = self.df[np.where(self.df[:,0]==fn)]  #get the peaks from this frame number
                frames.append(PeakData(frame_df, self.geo))     #make the Peak data object and append
            return frames                           #return the list of appended peak datas



    def gen_qlist(self):
        '''
        generate a list of important values to calculate from
        it's easier to work with arrays the panda dataframes
        '''

        # fss_df = self.df[:,5]    #0-127, fs direction
        # sss_df = self.df[:,6]    #ss direction
        # inten_df = self.df[:,11] #intensity

        fss_df = self.df[:,1]    #0-127, fs direction
        sss_df = self.df[:,2]    #ss direction
        inten_df = self.df[:,3] #intensity

        pix_pos = self.geo.translate_pixels(sss_df, fss_df) #x,y,z position [m]

        # r_mag = np.sqrt( pix_pos[:,0]**2 + pix_pos[:,1]**2)
        r_mag = np.hypot(pix_pos[:,0], pix_pos[:,1])

        polar_t = np.degrees(np.arctan2(pix_pos[:,1], pix_pos[:,0]))
        polar_t[np.where(polar_t <0)] = polar_t[np.where(polar_t <0)] +360

        diffrat_t = np.degrees(np.arctan2(r_mag, pix_pos[:,2]))
        q_mag = (2*np.pi/self.geo.wavelength) * np.sin(np.radians(diffrat_t))/1e10 #1/A
        qlist = np.array([pix_pos[:,0], pix_pos[:,1], pix_pos[:,2], r_mag, diffrat_t, q_mag, polar_t, inten_df])

        return qlist.T





    def plot_peaks(self, cmap='viridis'):

        if type(cmap) != type('x'):
            plt.plot(self.qlist[:,0], self.qlist[:,1], '.')
        else:
            plt.scatter(self.qlist[:,0], self.qlist[:,1], s=20, c=self.qlist[:, -1],  cmap=cmap)
            plt.colorbar()



