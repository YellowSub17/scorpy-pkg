import numpy as np
import matplotlib.pyplot as plt


class PeakData:

    def __init__(self, df, geo ):
        '''
        handler for a peaks.txt file
        df: dataframe of the peak data, or str file path to txt
        geo: ExpGeom object associated to experiement geomtery
        qlist_flag: flag to generate qvector correlation list
                    dont waste time generateing calculating a list if we need
                    to split the frames and calc again anyway
        '''

        self.geo = geo  #ExpGeom object

        #if df is str, read dataframe from file, else, assume df is array
        if type(df)==str:
            #use cols: 
            #0: frameNumber, 6: peak_x_raw, 7: peak_y_raw, 12: total intens
            self.df = np.genfromtxt(df, delimiter=', ', skip_header=1, usecols=(0,6,7,12))
        else:
            self.df = df

        #multiple frames can be in a single peak file, so list the unique frames
        self.frame_numbers = np.unique(self.df[:,0])


        if len(self.frame_numbers)==1:
            self.scat_sqr, self.scat_pol = self.get_scat()



    def split_frames(self):
        '''
        return a list of PeakData objects, where each PeakData object on has a
        single frame of data
        '''
        assert len(self.frame_numbers)>1, "Cannot split frames for for unique frame."

        frames = []                                 #init list of frames
        for fn in self.frame_numbers:                    #for each frame number
            frame_df = self.df[np.where(self.df[:,0]==fn)]  #get the peaks from this frame number
            frames.append(PeakData(frame_df, self.geo))     #make the Peak data object and append
        return frames                           #return the list of appended peak datas



    def get_scat(self):
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

        r_mag = np.hypot(pix_pos[:,0], pix_pos[:,1])

        polar_t = np.degrees(np.arctan2(pix_pos[:,1], pix_pos[:,0]))
        polar_t[np.where(polar_t <0)] = polar_t[np.where(polar_t <0)] +360

        diffrat_t = np.degrees(np.arctan2(r_mag, pix_pos[:,2]))
        q_mag = (2*np.pi/self.geo.wavelength) * np.sin(np.radians(diffrat_t))/1e10 #1/A


        scat_sqr = np.array( [pix_pos[:,0], pix_pos[:,1], inten_df]).T
        scat_pol = np.array( [q_mag, polar_t, inten_df]).T


        return scat_sqr, scat_pol





    def plot_peaks(self, cmap='viridis'):
        plt.plot(self.scat_sqr[:,0], self.scat_sqr[:,1], '.')



