import h5py
import numpy as np
import matplotlib.pyplot as plt






class MaskData:

    def __init__(self, fname, geo, mask_value=0):
        self.fname = fname
        self.mask_value=mask_value
        self.geo = geo
        self.h5 = h5py.File(self.fname, 'r')
        self.data = np.array(h5py.File(self.fname, 'r')['data']['data'])
        self.qlist = self.gen_qlist()


    def gen_qlist(self):
        loc = np.where(self.data==self.mask_value)

        fss_df = loc[1]
        sss_df = loc[0]
        inten_df = np.ones(len(fss_df))

        pix_pos = self.geo.translate_pixels(sss_df, fss_df) #x,y,z position [m]

        # r_mag = np.sqrt( pix_pos[:,0]**2 + pix_pos[:,1]**2)
        r_mag = np.hypot( pix_pos[:,0], pix_pos[:,1])

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




