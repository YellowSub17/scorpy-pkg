import numpy as np
import matplotlib.pyplot as plt
import os
import h5py

from scorpy.env import DATADIR


from ..utils import to_polar





class XfmH5s:

    def __init__(self, group, run, nx=1062, ny=1028, radius=514,  image_center=(518, 528),
                 pix_size=75e-6, cam_length=0.692, wavelength=0.67018e-10):


        self.group = group
        self.run = run
        self.dpath = DATADIR+f'asci/data/xfm/17635/raw/eiger/{self.group}/{self.run}/'

        self.nx = nx
        self.ny = ny
        self.radius = radius
        self.image_center = image_center
        self.pix_size = pix_size
        self.cam_length = cam_length
        self.wavelength = wavelength

        self.qpts, self.tpts, self.spts = self.calc_pts()



    def calc_pts(self):

        basepts = np.arange(1024)

        a = np.arctan( ( basepts*self.pix_size) / self.cam_length)
        q = ( (4*np.pi)/ self.wavelength) *np.sin( a/2) *1e-10
        s = (2 / self.wavelength ) * np.sin(a/2)
        t = np.degrees(a)

        return q, t, s






    def ls_h5s(self):
        h5_fnames = os.listdir(self.dpath)
        h5_fnames.sort()
        return h5_fnames[:-1]



    def extract_array(self, fname):
        print(self.dpath+fname)

        with h5py.File(self.dpath+fname, 'r') as f:
            d = np.array(f['entry/data/data/'])
        return d


    def full_unwrap(self, d):
        ite = np.ones( d.shape[0])
        m = map( to_polar, d, ite*self.radius,
                        ite*self.image_center[0], ite*self.image_center[1])

        return np.stack(list(m))



    # def full_unwrap(self,):








#     def polar_angular_correlation(self, polar, polar2=None):
        # fpolar = np.fft.fft( polar, axis=1 )

        # if polar2 != None:
            # fpolar2 = np.fft.fft( polar2, axis=1)
            # out = np.fft.ifft( fpolar2.conjugate() * fpolar, axis=1 )
        # else:
            # out = np.fft.ifft( fpolar.conjugate() * fpolar, axis=1 )
        # return np.real(out)






















